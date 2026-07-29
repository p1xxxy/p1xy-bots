import aiosqlite

DB_PATH = "clients.db"


async def init_db():
    """Создаёт таблицу clients, если её ещё нет."""
    async with aiosqlite.connect(DB_PATH) as conn:
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS clients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                email TEXT,
                created_at TEXT NOT NULL
            )
        """)
        await conn.commit()