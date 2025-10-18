import discord
from discord.ext import commands
import os

# ვიღებთ ბოტის ტოკენს Railway-ს საიდუმლო ველიდან
BOT_TOKEN = os.environ.get('BOT_TOKEN')

if BOT_TOKEN is None:
    print("FATAL ERROR: BOT_TOKEN not found in environment variables.")
    exit()

# --- ბოტის უფლებების (Intents) დაყენება ---
# ჩვენ გვჭირდება "Members" და "Message Content" უფლებები,
# რომ Welcome, Stats და Counting ფუნქციებმა იმუშაოს.
intents = discord.Intents.default()
intents.members = True
intents.message_content = True 

# ვქმნით ბოტის ობიექტს ამ უფლებებით
bot = commands.Bot(command_prefix="!", intents=intents)

# ეს ფუნქცია მუშაობს, როცა ბოტი წარმატებით ირთვება
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("Bot is ready and online!")
    print("-" * 30)
    
    # --- ვიწყებთ ყველა ჩვენი ფუნქციის (Cogs) ჩატვირთვას ---
    cogs_to_load = [
        'counting_cog',           # დათვლის სისტემა
        'fun_cog',                # /gay da /8ball
        'welcome_and_roles_cog',  # მისალმება და ავტო-როლი
        'giveaway_cog',           # გათამაშებები
        'server_management_cog'   # Stats, Clear, Poll, Notifications
    ]
    
    loaded_cogs = []
    failed_cogs = []

    for cog in cogs_to_load:
        try:
            await bot.load_extension(cog)
            loaded_cogs.append(cog)
        except Exception as e:
            print(f"FAILED to load cog '{cog}': {e}")
            failed_cogs.append(f"{cog} ({e})")

    print("\n--- Cog Loading Summary ---")
    print(f"Successfully loaded: {', '.join(loaded_cogs)}")
    if failed_cogs:
        print(f"FAILED to load: {', '.join(failed_cogs)}")
    
    print("-" * 30)

    # --- სლეშ ბრძანებების რეგისტრაცია (Sync) ---
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} slash command(s) successfully.")
    except Exception as e:
        print(f"Error syncing commands: {e}")
    
    print("-" * 30)

# ვუშვებთ ბოტს ტოკენის გამოყენებით
bot.run(BOT_TOKEN)
