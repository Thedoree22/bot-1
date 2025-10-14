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
    print("--- Bot is starting up ---")

    # ვტვირთავთ ყველა ჩვენს ბრძანების ფაილს
    await bot.load_extension('counting_cog')
    print("Loaded: counting_cog.py")

    await bot.load_extension('fun_cog')
    print("Loaded: fun_cog.py")

    # ვარეგისტრირებთ ბრძანებებს Discord-თან
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Error syncing commands: {e}")

    print("--- Bot is ready! ---")
        

bot.run(BOT_TOKEN)
