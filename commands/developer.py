from discord.ext import commands
import os
import discord
from datetime import datetime
from discord import Embed

class Developer(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('✅ Developer Cog is ready')

    def cog_check(self, ctx):
        if ctx.author.id == self.bot.owner_id:
            return True
        raise commands.NotOwner(f'{ctx.author.id} tried to run a owner only command.')

    @commands.group()
    async def dev(self, ctx:commands.Context):
        if not ctx.invoked_subcommand:
            await ctx.send('Run help dev')

    @dev.command(usage='clearconsole', aliases=['cc'])
    async def clearconsole(self, ctx):
        """
        Cleares console so errors are spaced out and are easier to read.
        """
        os.system("clear")
        await ctx.send(embed=Embed(title="Successfully cleared console.", color=0x00ff00))


    @dev.command(usage="loadcog <cog>", aliases=["lc"])
    async def loadcog(self, ctx, cog=None):
        folders=['commands', 'events']
        if not cog:
            await ctx.send(embed=Embed(title='Error', description='Please enter a cog', color=0xff0000, timestamp=datetime.utcnow()), delete_after=10)
            return
        
        ai=1
        for folder in folders:
            try:
                files = os.listdir(folder)
                cogpy = cog.lower() +'.py'
                shortcog = cogpy[:-3]
                print([files, cogpy, shortcog, cog, ai])
                ai+=1

                if cogpy in files:
                    await ctx.send(f'Loading {shortcog} cog...', delete_after=10)
                    self.bot.load_extension(f"{folder}.{shortcog}")
                    await ctx.send(f'{shortcog} cog has been loaded', delete_after=10)
                    print(f"⚙️ `{cogpy}` {folder[:-1]} cog has been loaded.")
                    return
                else:
                    pass                        
            except commands.errors.ExtensionNotLoaded:
                await ctx.send(embed=Embed(color=0xff0000, title='Error', description='This cog was already loaded or could not be found', delete_after=10))
                return
            except commands.errors.ExtensionAlreadyLoaded:
                await ctx.send(embed=Embed(color=0xff0000, title='Error', description='This cog was already loaded.', delete_after=10))

            except FileNotFoundError as e:
                print(str(e))
                return
            except Exception as error:
                await ctx.send(embed=Embed(color=0xff0000, title='Error', description=str(error)), delete_after=60)
                raise error
        await ctx.send(embed=Embed(color=0xff0000, title='Error', description=f"This cog doesn't exist."), delete_after=10)




    

    @dev.command(aliases=['rc'], usage='reloadcog <cog>')
    async def reloadcog(self, ctx, cog=None):
        """
        Reloads a cog. Only to be used by developers.
        """
        try:
            await ctx.message.delete()
        except discord.Forbidden:
            pass
        except discord.NotFound:
            pass
        folders=['commands', 'events']
        if not cog:
            await ctx.send(embed=Embed(title='Error', description='Please enter a cog', color=0xff0000, timestamp=datetime.utcnow()), delete_after=10)
            return
        
        for folder in folders:
            try:
                files = os.listdir(folder)
                cogpy = cog.lower() +'.py'
                shortcog = cogpy[:-3]

                if cogpy in files:
                    await ctx.send(f'Reloading {shortcog} cog...', delete_after=10)
                    self.bot.unload_extension(f"{folder}.{shortcog}")
                    self.bot.load_extension(f"{folder}.{shortcog}")
                    await ctx.send(f'{shortcog} cog has been reloaded', delete_after=10)
                    print(f"⚙️ `{cogpy}` {folder[:-1]} cog has been reloaded.")
                    return
                else:
                    pass       
            except commands.errors.ExtensionNotLoaded:
                await ctx.send(embed=Embed(color=0xff0000, title='Error', description='This cog was already loaded or could not be found', delete_after=10))
                return
            except FileNotFoundError as e:
                print(str(e))
                return
            except Exception as error:
                await ctx.send(embed=Embed(color=0xff0000, title='Error', description=str(error)), delete_after=60)
                raise error
        await ctx.send(embed=Embed(color=0xff0000, title='Error', description=f"This cog doesn't exist."), delete_after=10)


    


def setup(bot):
    bot.add_cog(Developer(bot))