import discord
from discord.ext import commands
import os

BOT_TOKEN = os.environ.get('BOT_TOKEN')
if BOT_TOKEN is None:
    print("FATAL ERROR: BOT_TOKEN ar aris motavsebuli Railway Variables-shi.")
    exit()

# --- Botis uflebebi (Intents) ---
intents = discord.Intents.default()
intents.members = True       # aucilebelia Welcome, Auto-Role, Stats-istvis
intents.message_content = True # aucilebelia Counting-istvis

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot chartulia rogorc {bot.user}")
    print("-" * 30)
    
    # --- Yvela funqciis (Cogs) chatvirtva ---
    cogs_to_load = [
        'counting_cog',
        'fun_cog',
        'welcome_and_roles_cog',
        'giveaway_cog',
        'server_management_cog'
    ]
    
    for cog in cogs_to_load:
        try:
            await bot.load_extension(cog)
            print(f"Warmatebit chaitvirta: {cog}")
        except Exception as e:
            print(f"ERROR: Ver chaitvirta {cog}: {e}")

    print("-" * 30)

    # --- Slesh brdzanebebis daregistrireba ---
    try:
        synced = await bot.tree.sync()
        print(f"Warmatebit daregistrirda {len(synced)} brdzaneba.")
    except Exception as e:
        print(f"Error brdzanebebis registraciisas: {e}")
    
    print("-" * 30)

bot.run(BOT_TOKEN)
