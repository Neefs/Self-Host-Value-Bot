from discord.ext import commands
from discord import Embed
from discord.ext.commands.core import Command, command
from discord.ext.commands.errors import BadArgument, MissingAnyRole, MissingRequiredArgument
from utils.main import post_code
import traceback as tb

class CommandError(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.discord = 'https://discord.gg/P9bW4Ug4kx'

    @commands.Cog.listener()
    async def on_command_error(self, ctx:commands.Context, error):
        ignored = (commands.CommandNotFound,)
        read_args = (commands.BadArgument,)
        if isinstance(error, ignored):
            return
        elif isinstance(error, read_args):
            await ctx.send(embed=Embed(title='Error', color=0xff0000, description='Error: `{0}`\nIf you belive this is an error join my [support discord]({1})'.format(error.args[0], self.discord)))
            return
        elif isinstance(error, MissingRequiredArgument):
            
            aliases = ctx.command.aliases
            if aliases != []:
                alias = '['
                for i in aliases:
                    if i == aliases[len(aliases) - 1]: # it is the last item in this list
                        alias += (i + ']')# just add to string
                    else:
                        alias += (i + "|") # add to string with comma and space 

            alias = ctx.command.name
            
            await ctx.send(embed=Embed(title='Error', color=0xff0000, description=f"Error: {error.args[0]}\nCorrect Usage: {ctx.clean_prefix}{alias} {ctx.command.signature}"))
            return

        elif isinstance(error, commands.MissingRole):
            await ctx.send(embed=Embed(title='Error', color=0xff0000, description='Error: **Missing role {0}**. \n{0} is required to run this command.\nIf you belive this is an error join my [support discord]({1})'.format(error.missing_role.mention, self.discord)))
            return
        
        else:
            e = Embed(title='Error', color=0xff0000, description=f'There has been an error:')
            traceback = (
                "".join(tb.format_exception(type(error), error, error.__traceback__))
                )
            link = await post_code(traceback, 'bash')
            if len(traceback) >= 2000:
                traceback = f'Error too long use the link provided below.'
            e.description +=f'\n```py\n{traceback}```\nError also located here: {link}'

            await ctx.send(embed=e)
            print('Ignoring exception in command {}:'.format(ctx.command))
            tb.print_exception(type(error), error, error.__traceback__)


def setup(bot):
    bot.add_cog(CommandError(bot))