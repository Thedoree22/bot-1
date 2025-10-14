import discord
from discord.ext import commands
import os

# Railway ამ ტოკენს თავისით წაიკითხავს საიდუმლო ველიდან
BOT_TOKEN = os.environ['BOT_TOKEN']

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    await bot.load_extension('counting_cog')
    await bot.load_extension('fun_cog')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Error syncing commands: {e}")
        

bot.run(BOT_TOKEN)
