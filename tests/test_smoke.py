from sqlalchemy import select

from models.users import User


async def test_sqlite_engine_registers_all_tables(db_engine):
    async with db_engine.connect() as conn:
        tables = await conn.run_sync(lambda sync_conn: sync_conn.dialect.get_table_names(sync_conn))
    assert {"students", "teachers", "courses", "tasks", "schedules", "users"} <= set(tables)


async def test_client_can_reach_app(client):
    response = await client.get("/students/")
    assert response.status_code == 200
    assert response.json() == []


async def test_pg_uuid_roundtrip(db_session):
    user = User(email="smoke@example.com", hashed_password="x", is_active=True)
    db_session.add(user)
    await db_session.commit()

    result = await db_session.execute(select(User).where(User.email == "smoke@example.com"))
    saved = result.scalar_one()
    assert saved.id is not None
    assert isinstance(saved.id, type(user.id))
