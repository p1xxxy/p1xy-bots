import aiosqlite
from datetime import datetime

DB_PATH = "clients.db"

async def init_db():
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

async def init_roles():
    """Добавляет роли в базу данных, если их ещё нет."""
    async with aiosqlite.connect(DB_PATH) as conn:
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS roles (
                user_id INTEGER PRIMARY KEY,
                role_name TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT
            )""")
        await conn.commit()
        
async def init_pending_operators():
    """Создаёт таблицу для хранения ожидающих операторов, если её ещё нет."""
    async with aiosqlite.connect(DB_PATH) as conn:
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS pending_operators (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                full_name TEXT NOT NULL,
                created_at TEXT NOT NULL
            )""")
        await conn.commit()
        
async def add_pending_request(user_id: int, username: str | None, full_name: str) -> bool:
    """Добавляет запрос на роль оператора в базу данных.
    
    Возвращает True, если запрос был успешно добавлен, иначе False.
    """
    async with aiosqlite.connect(DB_PATH) as conn:
        try:
            await conn.execute(
                "INSERT INTO pending_operators (user_id, username, full_name, created_at) VALUES (?, ?, ?, ?)",
                (user_id, username, full_name, datetime.now().isoformat())
            )
            await conn.commit()
            return True
        except aiosqlite.IntegrityError:
            # Если пользователь уже есть в таблице pending_operators
            return False
        except Exception as e:
            print(f"Unexpected error in add_pending_request: {e}")
            raise
        
async def remove_pending_request(user_id: int) -> None:
    """Удаляет запрос на роль оператора из базы данных."""
    async with aiosqlite.connect(DB_PATH) as conn:
        await conn.execute(
            "DELETE FROM pending_operators WHERE user_id = ?",
            (user_id,)
        )
        await conn.commit()
        
async def add_client(name: str, phone: str, email:str | None) -> None:
    async with aiosqlite.connect(DB_PATH) as conn:
        await conn.execute(
            "INSERT INTO clients (name, phone, email, created_at) VALUES (?, ?, ?, ?)",
            (name, phone, email, datetime.now().isoformat())
        )
        await conn.commit()

async def add_role(user_id: int, role_name: str) -> None:
    async with aiosqlite.connect(DB_PATH) as conn:
        now = datetime.now().isoformat()
        await conn.execute(
            "INSERT INTO roles (user_id, role_name, created_at, updated_at) VALUES (?, ?, ?, NULL)"
            " ON CONFLICT(user_id) DO UPDATE SET role_name=excluded.role_name, updated_at=?",
            (user_id, role_name, now, now)
        )
        await conn.commit()

async def get_role(user_id: int) -> str | None:
    async with aiosqlite.connect(DB_PATH) as conn:
        cursor = await conn.execute(
            "SELECT role_name FROM roles WHERE user_id = ?",
            (user_id,)
        )
        row = await cursor.fetchone()
        return row[0] if row else None

async def get_all_clients() -> list:
    async with aiosqlite.connect(DB_PATH) as conn:
         cursor = await conn.execute("SELECT * FROM clients")
         rows = await cursor.fetchall()
         return rows


