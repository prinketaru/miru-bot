import discord
from discord.ext import commands
from jikanpy import Jikan
from discord.ext.pages import Paginator, Page
from datetime import datetime

class Search(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    search = discord.SlashCommandGroup('search', 'Search for an anime, manga, character, or studio.')

    @search.command(name='anime', description='Search for an anime.')
    @discord.option('title', type=discord.SlashCommandOptionType.string, description='The title of the show to search for.')
    async def anime(self, ctx, title: str):
        jikan = Jikan()
        search_result = jikan.search('anime', title)

        if not search_result['data']:
            await ctx.send_response('No results found for your search.', ephemeral=True)
            return
        
        pages = []

        for result in search_result['data']:

            embed = discord.Embed(
                title=f'{result['title']} ({result['title_japanese']})',
                description=result['synopsis'],
                color=discord.Color.nitro_pink(),
                url=result['url']
            )

            embed.add_field(name='Type', value=result['type'] if result['type'] else 'N/A', inline=True)
            embed.add_field(name='Episodes', value=result['episodes'] if result['episodes'] else 'N/A', inline=True)
            embed.add_field(name='Score', value=result['score'] if result['score'] else 'N/A', inline=True)
            embed.add_field(name='Status', value=result['status'] if result['status'] else 'N/A', inline=True)
            embed.add_field(name='Start Date', value=f'<t:{int(datetime.fromisoformat(result['aired']['from'].replace('Z', '+00:00')).timestamp())}:F>' if result['aired']['from'] else 'N/A', inline=True)
            embed.add_field(name='End Date', value=f'<t:{int(datetime.fromisoformat(result['aired']['to'].replace('Z', '+00:00')).timestamp())}:F>' if result['aired']['to'] else 'N/A', inline=True)
            embed.add_field(name='Rating', value=result['rating'] if result['rating'] else 'N/A', inline=True)
            embed.add_field(name='Members', value=result['members'] if result['members'] else 'N/A', inline=True)
            embed.add_field(name='Genres', value=', '.join([f"[{genre['name']}]({genre['url']})" for genre in result['genres']]) if result['genres'] else 'N/A', inline=True)

            embed.set_thumbnail(url=result['images']['jpg']['image_url'])
            embed.set_author(name=', '.join([studios['name'] for studios in result['studios']]) if result['studios'] else 'N/A', url=result['studios'][0]['url'] if result['studios'] else result['url'])


            page = Page(embeds=[embed])
            pages.append(page)

        paginator = Paginator(pages=pages)

        await paginator.respond(ctx.interaction, ephemeral=False)

    @search.command(name='manga', description='Search for a manga.')
    @discord.option('title', type=discord.SlashCommandOptionType.string, description='The title of the manga to search for.')
    async def manga(self, ctx, title: str):
        jikan = Jikan()
        search_result = jikan.search('manga', title)

        if not search_result['data']:
            await ctx.send_response('No results found for your search.', ephemeral=True)
            return
        
        pages = []

        for result in search_result['data']:

            embed = discord.Embed(
                title=f'{result['title']} ({result['title_japanese']})',
                description=result['synopsis'],
                color=discord.Color.green(),
                url=result['url']
            )

            if result['background']:
                embed.add_field(name='Background', value=result['background'], inline=False)
            if result['type']:
                embed.add_field(name='Type', value=result['type'] if result['type'] else 'N/A', inline=True)
            if result['volumes']:
                embed.add_field(name='Volumes', value=result['volumes'] if result['volumes'] else 'N/A', inline=True)
            if result['score']:
                embed.add_field(name='Score', value=result['score'] if result['score'] else 'N/A', inline=True)
            if result['status']:
                embed.add_field(name='Status', value=result['status'] if result['status'] else 'N/A', inline=True)
            if result['published']['from']:
                embed.add_field(name='Start Date', value=f'<t:{int(datetime.fromisoformat(result['published']['from'].replace('Z', '+00:00')).timestamp())}:F>' if result['published']['from'] else 'N/A', inline=True)
            if result['published']['to']:
                embed.add_field(name='End Date', value=f'<t:{int(datetime.fromisoformat(result['published']['to'].replace('Z', '+00:00')).timestamp())}:F>' if result['published']['to'] else 'N/A', inline=True)
            if result['demographics']:
                embed.add_field(name='Demographics', value=', '.join([f"[{demographics['name']}]({demographics['url']})" for demographics in result['demographics']]) if result['demographics'] else 'N/A', inline=True)
            if result['members']:
                embed.add_field(name='Members', value=result['members'] if result['members'] else 'N/A', inline=True)
            if result['genres']:
                embed.add_field(name='Genres', value=', '.join([f"[{genre['name']}]({genre['url']})" for genre in result['genres']]) if result['genres'] else 'N/A', inline=True)

            embed.set_thumbnail(url=result['images']['jpg']['image_url'])
            embed.set_author(name='; '.join([authors['name'] for authors in result['authors']]) if result['authors'] else 'N/A', url=result['authors'][0]['url'] if result['authors'] else result['url'])


            page = Page(embeds=[embed])
            pages.append(page)

        paginator = Paginator(pages=pages)

        await paginator.respond(ctx.interaction, ephemeral=False)

    @search.command(name='character', description='Search for a character.')
    @discord.option('name', type=discord.SlashCommandOptionType.string, description='The name of the character to search for.')
    async def character(self, ctx, name: str):
        jikan = Jikan()
        search_result = jikan.search('characters', name)

        if not search_result['data']:
            await ctx.send_response('No results found for your search.', ephemeral=True)
            return
        
        pages = []

        for result in search_result['data']:

            embed = discord.Embed(
                title=f'{result['name']} ({result['name_kanji']})',
                description=result['about'],
                color=discord.Color.greyple(),
                url=result['url']
            )

            if result['nicknames']:
                embed.add_field(name='Nicknames', value=', '.join(f"``{nickname}``" for nickname in result['nicknames']), inline=True)
            if result['favorites']:
                embed.add_field(name='Favorites', value=result['favorites'], inline=True)

            embed.set_thumbnail(url=result['images']['jpg']['image_url'])


            page = Page(embeds=[embed])
            pages.append(page)

        paginator = Paginator(pages=pages)

        await paginator.respond(ctx.interaction, ephemeral=False)

def setup(bot):
    bot.add_cog(Search(bot))