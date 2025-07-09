import asyncpg
import asyncio
import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)  
async def get_pool():
    return await asyncpg.create_pool(
        user='projuser',
        password='mypassword',
        database='ttest',
        host='localhost',
        port=5432
    )
async def tables_create(pool):
    async with pool.acquire() as conn:
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                t_id BIGINT UNIQUE NOT NULL,
                balance INT DEFAULT 0,
                spent INT DEFAULT 0,
                created TIMESTAMP DEFAULT NOW(),
                is_admin BOOLEAN DEFAULT FALSE
            )
            """
        )
        logging.info("Таблица users создана")
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS goods (
                id SERIAL PRIMARY KEY,
                name VARCHAR(50) NOT NULL UNIQUE,
                description TEXT NOT NULL,
                amount INT,
                price INT NOT NULL,
                purchase_data TEXT,
                category VARCHAR(50) NOT NULL
            )
            """
        )
        logging.info("Таблица goods создана")
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS orders (
                id SERIAL PRIMARY KEY,
                user_id INT REFERENCES users(id),
                good_id INT REFERENCES goods(id),
                created TIMESTAMP DEFAULT NOW()
            )
            """
        )
        logging.info("Таблица orders создана")
async def main():
    pool= await get_pool()
    await tables_create(pool)
    await pool.close()
if __name__ == "__main__":
    asyncio.run(main())
