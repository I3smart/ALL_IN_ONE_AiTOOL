import aiosqlite
from config import DATABASE_PATH, FREE_TRIAL_LIMIT

async def init_db():
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                free_generations INTEGER DEFAULT 0,
                is_paid INTEGER DEFAULT 0,
                credits INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS payments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                telegram_payment_charge_id TEXT,
                amount INTEGER,
                currency TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.commit()

async def get_or_create_user(user_id: int, username: str):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute("SELECT user_id, free_generations, is_paid, credits FROM users WHERE user_id = ?", (user_id,)) as cursor:
            row = await cursor.fetchone()
            if row:
                return {"user_id": row[0], "free_generations": row[1], "is_paid": bool(row[2]), "credits": row[3]}
        
        await db.execute("INSERT INTO users (user_id, username) VALUES (?, ?)", (user_id, username))
        await db.commit()
        return {"user_id": user_id, "free_generations": 0, "is_paid": False, "credits": 0}

async def check_and_consume_credit(user_id: int) -> bool:
    """Atomic check and increment to prevent race condition trial abuse."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute("SELECT free_generations, is_paid, credits FROM users WHERE user_id = ?", (user_id,)) as cursor:
            row = await cursor.fetchone()
            if not row:
                return False
            
            free_gen, is_paid, credits = row[0], bool(row[1]), row[2]

            if is_paid or credits > 0:
                if credits > 0 and not is_paid:
                    await db.execute("UPDATE users SET credits = credits - 1 WHERE user_id = ?", (user_id,))
                    await db.commit()
                return True
            
            if free_gen < FREE_TRIAL_LIMIT:
                await db.execute("UPDATE users SET free_generations = free_generations + 1 WHERE user_id = ?", (user_id,))
                await db.commit()
                return True
            
            return False

async def add_credits(user_id: int, credits_to_add: int):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("UPDATE users SET credits = credits + ? WHERE user_id = ?", (credits_to_add, user_id))
        await db.commit()

async def record_payment(user_id: int, charge_id: str, amount: int, currency: str):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            "INSERT INTO payments (user_id, telegram_payment_charge_id, amount, currency) VALUES (?, ?, ?, ?)",
            (user_id, charge_id, amount, currency)
        )
        await db.execute("UPDATE users SET is_paid = 1 WHERE user_id = ?", (user_id,))
        await db.commit()
