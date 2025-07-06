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
async def alter_table(pool):
    async with pool.acquire() as conn:
        await conn.execute(
            """
            

            """
        )
async def main():
    pool= await get_pool()
    await alter_table(pool)
    await pool.close()
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
