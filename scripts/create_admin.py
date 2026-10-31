"""Create the first StudyFlow API administrator or promote an existing user.

Example:
    python scripts/create_admin.py --email admin@example.com --name Administrator

The password can be supplied through ADMIN_PASSWORD or entered interactively.
"""

import argparse
import asyncio
import getpass
import os
import selectors
import sys
from pathlib import Path

from pydantic import ValidationError

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from core.database import AsyncSessionLocal
from services.users import user_service


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a StudyFlow API administrator.",
    )
    parser.add_argument(
        "--email",
        default=os.getenv("ADMIN_EMAIL"),
        help="Administrator email (or ADMIN_EMAIL).",
    )
    parser.add_argument(
        "--name",
        default=os.getenv("ADMIN_NAME", "Administrator"),
        help="Administrator name (or ADMIN_NAME).",
    )
    parser.add_argument(
        "--password",
        default=os.getenv("ADMIN_PASSWORD"),
        help=(
            "Password (or ADMIN_PASSWORD). "
            "Avoid passing passwords on the command line in production."
        ),
    )
    return parser.parse_args()


def read_password(args: argparse.Namespace) -> str:
    password = args.password
    if password is None:
        password = getpass.getpass("Admin password: ")
        confirmation = getpass.getpass("Repeat password: ")
        if password != confirmation:
            raise SystemExit("Passwords do not match.")

    if len(password) < 8:
        raise SystemExit("Password must be at least 8 characters long.")
    return password


async def create_admin(email: str, name: str, password: str) -> None:
    async with AsyncSessionLocal() as db:
        try:
            _, created = await user_service.create_or_promote_admin(
                db,
                email=email,
                name=name,
                password=password,
            )
        except ValidationError as exc:
            raise SystemExit(f"Invalid input: {exc}") from exc

        if created:
            print(f"Admin {email} created.")
        else:
            print(f"User {email} promoted to admin.")


def run(coro) -> None:
    if sys.platform == "win32":
        loop_factory = lambda: asyncio.SelectorEventLoop(  # noqa: E731
            selectors.SelectSelector()
        )
        with asyncio.Runner(loop_factory=loop_factory) as runner:
            runner.run(coro)
        return

    asyncio.run(coro)


def main() -> None:
    args = parse_args()
    if not args.email:
        raise SystemExit("Specify --email or the ADMIN_EMAIL environment variable.")
    if len(args.name.strip()) < 2:
        raise SystemExit("Name must be at least 2 characters long.")

    run(
        create_admin(
            email=args.email.strip().lower(),
            name=args.name.strip(),
            password=read_password(args),
        )
    )


if __name__ == "__main__":
    main()
