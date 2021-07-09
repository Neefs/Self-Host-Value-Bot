from discord.ext import commands
import json, discord, os

with open('config.json', 'r+') as outfile:
    config = json.loads(outfile.read())

bot = commands.Bot(command_prefix=config["bot"]["prefix"], intents=discord.Intents.all())

@bot.event
async def on_ready():
    print('Bot is ready')


def getcogs(folder):
    try:
        for filename in os.listdir(folder):
            if filename.endswith(".py") and not filename.startswith("_"):
                bot.load_extension(f"{folder}.{filename[:-3]}")
    except FileNotFoundError: print(str(folder)+' Could not be found')
        


if __name__ == "__main__":
    getcogs('commands')
    getcogs('events')
    bot.load_extension('jishaku')


bot.run(config["bot"]["token"])