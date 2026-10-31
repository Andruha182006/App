"""Створює першого адміністратора або підвищує існуючого користувача.

Приклад:
    python scripts/create_admin.py --email admin@example.com --name Admin

Пароль можна передати через ``ADMIN_PASSWORD`` або ввести інтерактивно.
"""

import argparse
import asyncio
import getpass
import os
import selectors
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from core.database import AsyncSessionLocal
from core.enums import UserRole
from core.security import get_password_hash
from repository.users import user_repository


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Створити адміністратора StudyFlow API.",
    )
    parser.add_argument(
        "--email",
        default=os.getenv("ADMIN_EMAIL"),
        help="Email адміністратора (або ADMIN_EMAIL).",
    )
    parser.add_argument(
        "--name",
        default=os.getenv("ADMIN_NAME", "Administrator"),
        help="Ім'я адміністратора (або ADMIN_NAME).",
    )
    parser.add_argument(
        "--password",
        default=os.getenv("ADMIN_PASSWORD"),
        help=(
            "Пароль (або ADMIN_PASSWORD). "
            "Не передавайте пароль у командному рядку на production."
        ),
    )
    return parser.parse_args()


def read_password(args: argparse.Namespace) -> str:
    password = args.password
    if password is None:
        password = getpass.getpass("Пароль адміністратора: ")
        confirmation = getpass.getpass("Повторіть пароль: ")
        if password != confirmation:
            raise SystemExit("Паролі не збігаються.")

    if len(password) < 8:
        raise SystemExit("Пароль має містити щонайменше 8 символів.")
    return password


async def create_admin(email: str, name: str, password: str) -> None:
    async with AsyncSessionLocal() as db:
        existing = await user_repository.get_by_email(db, email=email)

        if existing is not None:
            await user_repository.update(
                db,
                user=existing,
                update_data={
                    "role": UserRole.admin,
                    "is_active": True,
                },
            )
            print(f"Користувача {email} підвищено до адміністратора.")
            return

        await user_repository.create(
            db,
            email=email,
            name=name,
            hashed_password=get_password_hash(password),
            role=UserRole.admin,
        )
        print(f"Адміністратора {email} створено.")


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
        raise SystemExit("Вкажіть --email або змінну оточення ADMIN_EMAIL.")
    if len(args.name.strip()) < 2:
        raise SystemExit("Ім'я має містити щонайменше 2 символи.")

    run(
        create_admin(
            email=args.email.strip().lower(),
            name=args.name.strip(),
            password=read_password(args),
        )
    )


if __name__ == "__main__":
    main()
