from discord.ext import commands
from discord import Embed
from discord.ext.commands.core import Command
from utils.main import post_code
import traceback as tb

class CommandError(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        ignored = (commands.CommandNotFound,)
        if isinstance(error, ignored):
            return
        else:
            traceback = (
                "".join(tb.format_exception(type(error), error, error.__traceback__))
                )
            if len(traceback) >= 2000:
                traceback = f'Error too long use the link provided below.'
            await ctx.send(embed=Embed(title='Error', color=0xff0000, description=f'There has been an error:\n```py\n{traceback}```\nError also located here: {await post_code(traceback,"bash")}'))
            print('Ignoring exception in command {}:'.format(ctx.command))
            tb.print_exception(type(error), error, error.__traceback__)


def setup(bot):
    bot.add_cog(CommandError(bot))