import discord
from discord.ext import commands
import requests

class Interactions(commands.Cog):
    # initialize the cog
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name='waifu', description='Get a random waifu image.')
    @discord.option(
        name='neko',
        type=discord.SlashCommandOptionType.boolean,
        description='Get a random neko image instead.',
        required=False,
    )
    async def waifu(self, ctx, neko: bool = False):
        # get image from api
        url = 'https://api.waifu.pics/sfw/waifu'

        # check if neko is true
        if neko:
            url = 'https://api.waifu.pics/sfw/neko'

        # get data
        response = requests.get(url)
        data = response.json()

        # send image
        await ctx.send_response(data['url'])

    # create interactions slash command group
    interactions = discord.SlashCommandGroup('interact', 'Interact with another user using anime gifs.')

    # hug command
    @interactions.command(name='hug', description='Hug another user.')
    @discord.option('user', type=discord.SlashCommandOptionType.user, description='The user to hug.')
    async def hug(self, ctx, user: discord.User):
        response = requests.get('https://api.waifu.pics/sfw/hug')
        data = response.json()

        embed = discord.Embed(
            description=f'**{ctx.author.mention} hugs {user.mention}**',
        )
        embed.set_image(url=data['url'])

        await ctx.send_response(embed=embed)

    # pat command
    @interactions.command(name='pat', description='Pat another user.')
    @discord.option('user', type=discord.SlashCommandOptionType.user, description='The user to pat.')
    async def pat(self, ctx, user: discord.User):
        response = requests.get('https://api.waifu.pics/sfw/pat')
        data = response.json()

        embed = discord.Embed(
            description=f'**{ctx.author.mention} pats {user.mention}**',
        )
        embed.set_image(url=data['url'])

        await ctx.send_response(embed=embed)

    # kiss command
    @interactions.command(name='kiss', description='Kiss another user.')
    @discord.option('user', type=discord.SlashCommandOptionType.user, description='The user to kiss.')
    async def kiss(self, ctx, user: discord.User):
        response = requests.get('https://api.waifu.pics/sfw/kiss')
        data = response.json()

        embed = discord.Embed(
            description=f'**{ctx.author.mention} kisses {user.mention}**',
        )
        embed.set_image(url=data['url'])

        await ctx.send_response(embed=embed)

    # slap command
    @interactions.command(name='slap', description='Slap another user.')
    @discord.option('user', type=discord.SlashCommandOptionType.user, description='The user to slap.')
    async def slap(self, ctx, user: discord.User):
        response = requests.get('https://api.waifu.pics/sfw/slap')
        data = response.json()

        embed = discord.Embed(
            description=f'**{ctx.author.mention} slaps {user.mention}**',
        )
        embed.set_image(url=data['url'])

        await ctx.send_response(embed=embed)

# setup the cog
def setup(bot):
    bot.add_cog(Interactions(bot))