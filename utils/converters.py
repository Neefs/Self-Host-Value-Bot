import re
import discord
from discord.ext import commands



money_regex = re.compile('(?:(\d{1,5})(mil|bil|tril|k|m|b|t))+?')
#re.compile("\d*(tril|bil|mil|m|k|t|b)")
money_dict = {
    'k': 1000,
    'mil': 1000000,
    'm': 1000000,
    'b': 1000000000,
    'bil':1000000000,
    'tril': 1000000000000,
    't': 1000000000000
}

class MoneyConverter(commands.Converter):
    async def convert(self, ctx: commands.Context, argument: str):
        args = argument.lower()
        matches = re.findall(money_regex, args)
        amount = 0
        if matches != []:
            for key, value in matches:
                try: amount += money_dict[value] * float(key)
                except KeyError: raise commands.BadArgument(f"{value} is an invalid time key! h|m|s|d are valid arguments")
                except ValueError: raise commands.BadArgument(f"{key} is not a number!")
        else:
            try: amount+=float(argument)
            except ValueError: raise commands.BadArgument(f'{argument} is not a number!')
            
        return round(amount)
