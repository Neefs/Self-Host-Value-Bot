import asyncio
import json
import typing

import discord
from discord.embeds import Embed
from discord.ext import commands
from sqlite import insert_data, read_data, remove_data, update_data
from utils.converters import MoneyConverter
from utils.main import server_balance, value_manager
from utils.pagination import paginationView


class Value(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

  
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('✅ Value Cog is ready')

    @commands.command()
    @value_manager()
    async def add(self, ctx, member:typing.Optional[discord.User], amount:MoneyConverter):
        """Adds to your/another players balance."""
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
            if incase != []:
                bal = bank[user.id] = incase[0][0]+amount
            else: 
                bal = bank[user.id] = amount
                await insert_data(database='banks', tables=[['user', user.id], ['amount', bal]])
            await ctx.send(embed=Embed(title='Value Added', color=self.bot.user.color, description='Added ${:,}. {} balance is now ${:,}'.format(amount, user.mention, bal)))

    @commands.command()
    @value_manager()
    async def remove(self, ctx, member:typing.Optional[discord.User], amount:MoneyConverter):
        """Removes to your/another players balance."""
        bank:dict = self.bot.banks
        if member: user = member
        else: user = ctx.author 
        if bank.get(user.id) is not None:
            bal = bank[user.id]
            if bal - amount < 0:
                bal = bank[user.id] = 0
            else:
                bal = bank[user.id] = bal-amount
            await update_data(database='banks', tables=[['amount', bal]], checks=[['user', user.id]])
            await ctx.send(embed=Embed(title='Value Removed', color=self.bot.user.color, description='Removed ${:,}. {} balance is now ${:,}'.format(amount, user.mention, bal)))
        else:
            incase = await read_data(database='banks', tables=['amount'], checks=[['user', user.id]])
            if incase != []:
                bal = bank[user.id] = incase[0][0]
                if bal - amount < 0:
                    bal = bank[user.id] = 0
                else:
                    bal = bank[user.id] = bal-amount
            else:
                bal = bank[user.id] = 0
                await insert_data(database='banks', tables=[['user', user.id], ['amount', bal]])
            await ctx.send(embed=Embed(title='Value Removed', color=self.bot.user.color, description='Removed ${:,}. {} balance is now ${:,}'.format(amount, user.mention, bal)))

    @commands.command(aliases=['clear'])
    @value_manager()
    async def reset(self, ctx, member:typing.Optional[discord.User]):
        """Resets the value of a specified player or the whole server."""
        bank:dict = self.bot.banks
        if member:
            if bank.get(member.id) is None:
                raise commands.BadArgument('The user is not in the database.')
            bank.pop(member.id)
            await remove_data(database='banks', checks=[['user', member.id]])
            await ctx.send(embed=Embed(title='Reset Value', description=f'Reset the value of {member.mention}.', color=self.bot.user.color))
        else:
            await ctx.send(f':warning: **You are about to reset the __MONEY__ module**\n{ctx.author.mention} Type CONFIRM RESET in chat within the next 10 seconds to confirm the reset')
            try: msg:discord.Message = await self.bot.wait_for('message', timeout=10, check=lambda message: message.author == ctx.author and message.channel == ctx.channel)
            except asyncio.TimeoutError:
                await ctx.send(embed=Embed(title='Error', color=0xff0000, description='Timed out. If you wish to reset all balances try again.'))
                return
            if msg.content.__contains__('CONFIRM RESET'):
                bank.clear()
                print(bank)
                value = await remove_data(database='banks')
                print(value)
                await ctx.send(embed=Embed(title='Reset', color=self.bot.user.color, description="""
                :white_check_mark: RESET CONFIRMED
                The highscores and history of the VALUE module has been deleted.
                Hope you had a good map.
                """))
            else:
                await ctx.send('Reset has been aborted.')

    @commands.command()
    async def top(self, ctx):
        bank:dict = self.bot.banks
        if bank == {}:
            await ctx.send(embed=Embed(title='Value Top', color=self.bot.user.color, description='Get value Slackas.'))
            return
        embed = Embed(title='Value Top', color=self.bot.user.color, description='').set_footer(text='Server Balance ${:,}'.format(await server_balance(self.bot)))
        pages = []
        position = 1
        place = 0
        for user, value in sorted(bank.items(), key=lambda entry: entry[1], reverse=True):
            embed.description += f"**{position}.** <@{user}>" + " {:,}\n".format(value)
            position+=1
            place += 1
            if place >= 10:
                pages.append(embed)
                embed = Embed(title='Value Top', color=self.bot.user.color, description='').set_footer(text='Server Balance ${:,}'.format(await server_balance(self.bot)))
                place = 0
        if embed.description != '':
            pages.append(embed)


        view = paginationView(pages, ctx)
        view.msg = await ctx.send(embed=pages[0], view=view)
        
            





           

    

async def setup(bot):
    await bot.add_cog(Value(bot))
