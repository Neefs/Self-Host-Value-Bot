import typing
from discord.embeds import Embed
from discord.errors import InvalidArgument
from utils.converters import MoneyConverter
from utils.pagination import paginationView
import discord
from sqlite import read_data, remove_data, insert_data, update_data
from discord.ext import commands

class Value(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def cog_check(self, ctx: commands.Context):
        role = ctx.guild.get_role(self.bot.config['value']['role'])
        if not role:
            raise commands.BadArgument('The role defined in the config could not be found in this guild. Please change the role in config then try again.')
        if role in ctx.author.roles:
            return True
        raise commands.MissingRole(role)

    # def valuemanager():
    #     async def predicate
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('✅ Value Cog is ready')

    @commands.command()
    async def add(self, ctx, member:typing.Optional[discord.User], amount:MoneyConverter):
        """Add your/another players balance."""
        bank:dict = self.bot.banks
        if member: user = member
        else: user = ctx.author

        if bank.get(user.id) is not None:
            bal = bank[user.id]
            bal = bank[user.id] = bal + amount
            await update_data(database='banks', tables=[['amount', bal]], checks=[['user', user.id]])
            await ctx.send(embed=Embed(title='Value Added', color=self.bot.user.color, description='Added ${:,}. {} balance is now ${:,}'.format(amount, user.mention, bal)))
        else:
            incase = await read_data(database='banks', tables=['amount'], checks=[['user', user.id]])
            print(incase)
            if incase != []:
                bal = bank[user.id] = incase[0][0]+amount
            else: 
                bal = bank[user.id] = amount
                await insert_data(database='banks', tables=[['user', user.id], ['amount', bal]])
            await ctx.send(embed=Embed(title='Value Added', color=self.bot.user.color, description='Added ${:,}. {} balance is now ${:,}'.format(amount, user.mention, bal)))

    @commands.command()
    async def top(self, ctx):
        bank:dict = self.bot.banks
        if bank == {}:
            await ctx.send(embed=Embed(title='Value Top', color=self.bot.user.color, description='Get value Slackas.'))
            return
        embed = Embed(title='Value Top', color=self.bot.user.color, description='')
        pages = []
        position = 1
        place = 0
        for user, value in sorted(bank.items(), key=lambda entry: entry[1], reverse=True):
            embed.description += f"**{position}.** <@{user}>" + " {:,}\n".format(value)
            position+=1
            place += 1

            if place >= 10:
                pages.append(embed)
                embed = Embed(title='Value Top', color=self.bot.user.color, description='')
                place = 0
        # if len(pages) == 0:
        #     pages.append(embed)
        # if place >= 1 and len(pages) != 1:
        #     pages.append(embed)
        if embed.description != '':
            pages.append(embed)


        view = paginationView(pages, ctx)
        view.msg = await ctx.send(embed=pages[0], view=view)
            





           

    

def setup(bot):
    bot.add_cog(Value(bot))