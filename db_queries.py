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
async def get_categories(pool):
    async with pool.acquire() as conn:
        rows = await conn.fetch(
            "SELECT id, name FROM categories"
        )
        return [dict(row) for row in rows]
async def get_goodname_by_catid(pool,cat):
    async with pool.acquire() as conn:
        rows = await conn.fetch(
            "SELECT name FROM goods WHERE category='$1'",
            cat
        )
        names=[row["name"] for row in rows]
        return names
async def get_good_by_name(pool,name):
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT name, description, amount, price WHERE NAME = $1",
            name
        )
        return row
async def insert_good(pool,name,desc,amount,price,category):
    async with pool.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO goods (name,description,amount,price,category)
                VALUES ($1,$2,$3,$4,$5)
                """,
                name,desc,amount,price,category
            )
async def insert_category(pool,name,emoji) -> None:
    async with pool.acquire() as conn:
        await conn.execute(
            """
            INSERT INTO categories (name,emoji)
            VALUES ($1,$2)
            """,
            name,emoji
        )