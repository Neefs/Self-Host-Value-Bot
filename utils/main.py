import mystbin
import aiosqlite
from sqlite import read_data

async def post_code(code, lang=None) -> str:
    if not lang:
        lang='python'
    client = mystbin.Client()
    returned = await client.post(code, lang)
    client.close()
    return returned
    

async def init_db():
    db = await aiosqlite.connect('data/database.db')
    cur = await db.cursor()
    await cur.execute("CREATE TABLE IF NOT EXISTS banks(user INT, amount INT)")
    await db.commit()
    await db.close()


async def cache_bank(bot):
    dbbank = await read_data(database='banks', tables=['*'])
    for user, amount in dbbank:
        bot.banks[user] = amount
    try: del dbbank, user, amount
    except UnboundLocalError: pass

