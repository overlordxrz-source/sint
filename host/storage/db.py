import aiosqlite
import os

DB_PATH = "data/sensing.db"

async def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    async with aiosqlite.connect(DB_PATH) as db:
        schema_path = os.path.join(os.path.dirname(__file__), "schema.sql")
        with open(schema_path, "r") as f:
            await db.executescript(f.read())
        await db.commit()

def get_db():
    return aiosqlite.connect(DB_PATH)
