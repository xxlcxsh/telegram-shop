async def get_balance(pool, t_id):
    async with pool.acquire() as conn:
        balance = await conn.fetchval(
                """
                SELECT balance FROM users WHERE t_id = $1
                """,
                t_id
            )
        return balance
async def get_spent(pool,t_id):
    async with pool.acquire() as conn:
        spent = await conn.fetchval(
                """
                SELECT spent FROM users WHERE t_id = $1
                """,
                t_id
            )
        return spent
async def get_time_created(pool,t_id):
    async with pool.acquire() as conn:
        created = await conn.fetchval(
                """
                SELECT created FROM users WHERE t_id = $1
                """,
                t_id
            )
        return created
async def create_user(pool,t_id):
    async with pool.acquire() as conn:
        await conn.execute(
            """
            INSERT INTO users (t_id)
            VALUES ($1)
            ON CONFLICT (t_id) DO NOTHING
            """,
            t_id
        )
async def get_is_admin(pool,t_id):
    async with pool.acquire() as conn:
        is_admin= await conn.fetchval(
            """
            SELECT is_admin FROM users WHERE t_id=$1
            """,
            t_id
        )
        return is_admin