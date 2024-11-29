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

    # reload all commands
    @discord.slash_command()
    async def reload(self, ctx):
        # get all cogs
        cogs = self.bot.extensions

        # reload all cogs
        for cog in cogs:
            self.bot.reload_extension(cog)

        # send a response
        await ctx.send_response('All commands reloaded.', ephemeral=True)

# setup the cog
def setup(bot):
    bot.add_cog(Utility(bot))