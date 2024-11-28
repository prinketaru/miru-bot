import discord
from discord.ext import commands
from jikanpy import Jikan
from discord.ext.pages import Paginator, Page
from datetime import datetime

class Search(commands.Cog):

    # initialize the cog
    def __init__(self, bot):
        self.bot = bot

    # create a slash command group for search
    search = discord.SlashCommandGroup('search', 'Search for an anime, manga, character, or studio.')

    # command to search for an anime
    @search.command(name='anime', description='Search for an anime.')
    @discord.option('title', type=discord.SlashCommandOptionType.string, description='The title of the show to search for.')
    async def anime(self, ctx, title: str):

        # get the search results from jikan
        jikan = Jikan()
        search_result = jikan.search('anime', title)

        # handle search not found
        if not search_result['data']:
            await ctx.send_response('No results found for your search.', ephemeral=True)
            return

        # create a list of pages to paginate        
        pages = []

        # loop through the search results
        for result in search_result['data']:

            # create an embed for the anime
            embed = discord.Embed(
                title=f"{result['title']} ({result['title_english']})",
                description=result['synopsis'],
                color=discord.Color.nitro_pink(),
                url=result['url']
            )

            # add fields to the embed
            add_field_safe(embed, 'Type', result['type'], inline=True)
            add_field_safe(embed, 'Episodes', result['episodes'], inline=True)
            add_field_safe(embed, 'Score', result['score'], inline=True)
            add_field_safe(embed, 'Status', result['status'], inline=True)
            add_field_safe(embed, 'Members', result['members'], inline=True)

            # handle demographics and genres
            demographics = result['demographics']
            add_field_safe(embed, 'Demographics', ', '.join([f"[{demo['name']}]({demo['url']})" for demo in demographics]), inline=True)

            genres = result['genres']
            add_field_safe(embed, 'Genres', ', '.join([f"[{genre['name']}]({genre['url']})" for genre in genres]), inline=True)

            # handle aired dates
            aired = result['aired']
            add_field_safe(embed, 'Start Date', f"<t:{int(datetime.fromisoformat(aired['from'].replace('Z', '+00:00')).timestamp())}:F>" if aired['from'] else 'N/A', inline=True)
            add_field_safe(embed, 'End Date', f"<t:{int(datetime.fromisoformat(aired['to'].replace('Z', '+00:00')).timestamp())}:F>" if aired['to'] else 'N/A', inline=True)

            # set thumbnail and author
            embed.set_thumbnail(url=result['images']['jpg']['image_url'])
            embed.set_author(name=', '.join([studios['name'] for studios in result['studios']]) if result['studios'] else 'N/A', url=result['studios'][0]['url'] if result['studios'] else result['url'])

            # create a page with the embed
            page = Page(embeds=[embed])
            pages.append(page)

        # create a paginator with the pages
        paginator = Paginator(pages=pages)

        # respond with the paginator
        await paginator.respond(ctx.interaction, ephemeral=False)

    # command to search for a manga
    @search.command(name='manga', description='Search for a manga.')
    @discord.option('title', type=discord.SlashCommandOptionType.string, description='The title of the manga to search for.')
    async def manga(self, ctx, title: str):

        # get the search results from jikan
        jikan = Jikan()
        search_result = jikan.search('manga', title)

        # handle search not found
        if not search_result['data']:
            await ctx.send_response('No results found for your search.', ephemeral=True)
            return
        
        # create a list of pages to paginate
        pages = []

        # loop through the search results
        for result in search_result['data']:

            # create an embed for the manga
            embed = discord.Embed(
                title=f"{result['title']} ({result['title_english']})",
                description=result['synopsis'],
                color=discord.Color.green(),
                url=result['url']
            )

            # add fields to the embed
            add_field_safe(embed, 'Type', result['type'], inline=True)
            add_field_safe(embed, 'Volumes', result['volumes'], inline=True)
            add_field_safe(embed, 'Score', result['score'], inline=True)
            add_field_safe(embed, 'Status', result['status'], inline=True)
            add_field_safe(embed, 'Members', result['members'], inline=True)

            # handle demographics and genres
            demographics = result['demographics']
            add_field_safe(embed, 'Demographics', ', '.join([f"[{demo['name']}]({demo['url']})" for demo in demographics]) if demographics else 'N/A', inline=True)

            genres = result['genres']
            add_field_safe(embed, 'Genres', ', '.join([f"[{genre['name']}]({genre['url']})" for genre in genres]) if genres else 'N/A', inline=True)

            # handle published dates
            published = result['published']
            add_field_safe(embed, 'Start Date', f"<t:{int(datetime.fromisoformat(published['from'].replace('Z', '+00:00')).timestamp())}:F>" if published['from'] else 'N/A', inline=True)
            add_field_safe(embed, 'End Date', f"<t:{int(datetime.fromisoformat(published['to'].replace('Z', '+00:00')).timestamp())}:F>" if published['to'] else 'N/A', inline=True)

            # set thumbnail and author
            embed.set_thumbnail(url=result['images']['jpg']['image_url'] if result['images']['jpg'] else 'https://www.wikidata.org/wiki/Q4044680#/media/File:MyAnimeList_Logo.png')
            embed.set_author(name='; '.join([authors['name'] for authors in result['authors']]) if result['authors'] else 'N/A', url=result['authors'][0]['url'] if result['authors'] else result['url'])

            # create a page with the embed
            page = Page(embeds=[embed])
            pages.append(page)

        # create a paginator with the pages
        paginator = Paginator(pages=pages)

        # respond with the paginator
        await paginator.respond(ctx.interaction, ephemeral=False)

    # command to search for a character
    @search.command(name='character', description='Search for a character.')
    @discord.option('name', type=discord.SlashCommandOptionType.string, description='The name of the character to search for.')
    async def character(self, ctx, name: str):

        # get the search results from jikan
        jikan = Jikan()
        search_result = jikan.search('characters', name)

        # handle search not found
        if not search_result['data']:
            await ctx.send_response('No results found for your search.', ephemeral=True)
            return
        
        # create a list of pages to paginate
        pages = []

        # loop through the search results
        for result in search_result['data']:

            # create an embed for the character
            embed = discord.Embed(
                title=f"{result['name']} ({result['name_kanji']})",
                description=result['about'],
                color=discord.Color.greyple(),
                url=result['url']
            )

            # add fields to the embed
            add_field_safe(embed, 'Nicknames', ', '.join([f"``{nickname}``" for nickname in result['nicknames']]), inline=True)
            add_field_safe(embed, 'Favorites', result['favorites'], inline=True)

            # set thumbnail
            embed.set_thumbnail(url=result['images']['jpg']['image_url'])

            #  create a page with the embed
            page = Page(embeds=[embed])
            pages.append(page)

        # create a paginator with the pages
        paginator = Paginator(pages=pages)

        # respond with the paginator
        await paginator.respond(ctx.interaction, ephemeral=False)

# helper function to add fields to an embed safely
def add_field_safe(embed, name, value, inline=True):
    if value:
        embed.add_field(name=name, value=value, inline=inline)

# cog setup function
def setup(bot):
    bot.add_cog(Search(bot))
