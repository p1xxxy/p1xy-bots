import aiosqlite
from datetime import datetime

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
        
async def add_client(name: str, phone: str, email:str | None) -> None:
    async with aiosqlite.connect(DB_PATH) as conn:
        await conn.execute(
            "INSERT INTO clients (name, phone, email, created_at) VALUES (?, ?, ?, ?)",
            (name, phone, email, datetime.now().isoformat())
        )
        await conn.commit()
        
async def get_all_clients() -> list:
    async with aiosqlite.connect(DB_PATH) as conn:
         cursor = await conn.execute("SELECT * FROM clients")
         rows = await cursor.fetchall()
         return rows


