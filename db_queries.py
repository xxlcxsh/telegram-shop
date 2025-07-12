from aiocache import cached
async def get_balance(pool, t_id) -> int:
    async with pool.acquire() as conn:
        balance = await conn.fetchval(
                """
                SELECT balance FROM users WHERE t_id = $1
                """,
                t_id
            )
        return balance
async def get_spent(pool,t_id) -> int:
    async with pool.acquire() as conn:
        spent = await conn.fetchval(
                """
                SELECT spent FROM users WHERE t_id = $1
                """,
                t_id
            )
        return spent
async def get_time_created(pool,t_id) -> str:
    async with pool.acquire() as conn:
        created = await conn.fetchval(
                """
                SELECT created FROM users WHERE t_id = $1
                """,
                t_id
            )
        return created
async def create_user(pool,t_id) -> None:
    async with pool.acquire() as conn:
        await conn.execute(
            """
            INSERT INTO users (t_id)
            VALUES ($1)
            ON CONFLICT (t_id) DO NOTHING
            """,
            t_id
        )
async def get_all_users_id(pool) -> list[int]:
    async with pool.acquire() as conn:
        rows = await conn.fetch(
            """
            SELECT t_id FROM users
            """
        )
        res = [row["t_id"] for row in rows]
        return res
@cached(ttl=1200)
async def get_is_admin(pool,t_id) -> bool:
    async with pool.acquire() as conn:
        is_admin= await conn.fetchval(
            """
            SELECT is_admin FROM users WHERE t_id=$1
            """,
            t_id
        )
        return is_admin
@cached(ttl=600)
async def get_categories(pool) -> list[dict[str: int | str]]:
    async with pool.acquire() as conn:
        rows = await conn.fetch(
            "SELECT id, name, emoji FROM categories"
        )
        return [dict(row) for row in rows]
@cached(ttl=600)
async def get_goods_by_catid(pool,cat) -> list[dict[str: int | str]]:
    async with pool.acquire() as conn:
        rows = await conn.fetch(
            "SELECT id,name FROM goods WHERE category=$1",
            cat
        )
        goods = [dict(row) for row in rows]
        return goods
@cached(ttl=600)
async def get_good_by_name(pool,name) -> dict:
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT name, description, amount, price FROM goods WHERE name = $1",
            name
        )
        return row
@cached(ttl=600)
async def get_good_by_id(pool,id) -> dict:
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT name, description, amount, price FROM goods WHERE id = $1",
            id
        )
        return dict(row)
async def insert_good(pool,name,desc,amount,price,category) -> dict:
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