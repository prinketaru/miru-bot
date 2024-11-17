import discord
import os
from dotenv import load_dotenv

load_dotenv()

# initialize bot
bot = discord.Bot(intents=discord.Intents.default(), default_command_integration_types={discord.IntegrationType.user_install, discord.IntegrationType.guild_install})

# on ready
@bot.event
async def on_ready():
    print(f'{bot.user} is ready and online!')

# load cogs
cogs_list = [
    'utility',
    'search'
]

for cog in cogs_list:
    bot.load_extension(f'cogs.{cog}')

# run bot
bot.run(os.getenv('TOKEN'))