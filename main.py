import asyncio
from utils.main import cache_bank, init_db
from discord.ext import commands
import json, discord, os

async def main():
    with open('config.json', 'r+') as outfile:
        config = json.loads(outfile.read())

    bot = commands.Bot(command_prefix=config["bot"]["prefix"], intents=discord.Intents.all(), owner_id=723386696007155763)
    bot.config = config
    bot.banks = {}

    @bot.event
    async def on_ready():
        print('Bot is ready')


    async def getcogs(folder):
        try:
            for filename in os.listdir(folder):
                if filename.endswith(".py") and not filename.startswith("_"):
                    await bot.load_extension(f"{folder}.{filename[:-3]}")
        except FileNotFoundError: print(str(folder)+' Could not be found')
            

    async def activate_cogs():
        await getcogs('commands')
        await getcogs('events')
        await bot.load_extension('jishaku')



    await activate_cogs()
    await init_db()
    await cache_bank(bot)

    await bot.start(config["bot"]["token"])

asyncio.run(main())