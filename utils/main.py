import json
import re

import aiosqlite
import mystbin
from discord.ext import commands
from sqlite import read_data

with open('config.json', 'r+') as outfile:
    config = json.loads(outfile.read())

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

async def server_balance(bot):
    bal = 0
    for i in bot.banks.values(): bal+=i
    return bal


async def cache_bank(bot):
    dbbank = await read_data(database='banks', tables=['*'])
    for user, amount in dbbank:
        bot.banks[user] = amount
    try: del dbbank, user, amount
    except UnboundLocalError: pass

def value_manager():
    async def predicate(ctx):
        role = ctx.guild.get_role(config['value']['role'])
        if not role:
            raise commands.BadArgument('The role defined in the config could not be found in this guild. Please change the role in config then try again.')
        if role in ctx.author.roles:
            return True
        raise commands.MissingRole(role)
    return commands.check(predicate)
        
