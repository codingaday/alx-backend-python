import asyncio
import aiosqlite

# Async function to fetch all users from DB
async def async_fetch_users():
    async with aiosqlite.connect("users.db") as db:
        cursor = await db.execute("SELECT * FROM users")
        users = await cursor.fetchall()
        print("All users:")
        for user in users:
            print(user)

# Async function to fetch users older than 40
async def async_fetch_older_users():
    async with aiosqlite.connect("users.db") as db:
        cursor = await db.execute("SELECT * FROM users WHERE age > 40")
        older_users = await cursor.fetchall()
        print("\nUsers older than 40:")
        for user in older_users:
            print(user)

# This function runs both fetch functions at the same time
async def fetch_concurrently():
    await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

# Main entry point: kicks off the concurrent tasks
if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
