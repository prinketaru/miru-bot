import discord
from discord.ext import commands

class Utility(commands.Cog):

    # initialize the cog
    def __init__(self, bot):
        self.bot = bot

    # create a slash command for ping
    @discord.slash_command()
    async def ping(self, ctx):
        
        # send a response with the bot's latency
        await ctx.send_response(f'Pong! ``{round(self.bot.latency * 1000)}ms``', ephemeral=True)

# setup the cog
def setup(bot):
    bot.add_cog(Utility(bot))