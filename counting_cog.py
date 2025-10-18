import discord
from discord.ext import commands
from discord import app_commands
import json
import os

DB_FILE = "counting_data.json"

def load_data():
    if not os.path.exists(DB_FILE): return {}
    try:
        with open(DB_FILE, "r") as f: return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError): return {}

def save_data(data):
    with open(DB_FILE, "w") as f: json.dump(data, f, indent=4)

class CountingCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.data = load_data()
        self.footer_text = "ბოტის მფლობელი - Teddy"

    c_group = app_commands.Group(name="c", description="დათვლის სისტემის მართვა")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot or not message.guild: return
        guild_id = str(message.guild.id)
        if guild_id not in self.data or "channel_id" not in self.data[guild_id]: return
        if message.channel.id != self.data[guild_id]["channel_id"]: return
        current_count = self.data[guild_id].get("count", 0)
        last_user_id = self.data[guild_id].get("last_user_id", None)
        if message.author.id == last_user_id:
            try:
                await message.delete()
                error_msg = await message.channel.send(f"{message.author.mention} ზედიზედ ვერ დაწერ დათვლა თავიდან დაიწყო")
                await error_msg.delete(delay=5)
            except discord.Forbidden: pass
            self.data[guild_id].update({"count": 0, "last_user_id": None})
            save_data(self.data)
            return
        try: number = int(message.content)
        except ValueError:
            try: await message.delete()
            except discord.Forbidden: pass
            return
        if number == current_count + 1:
            new_count = current_count + 1
            self.data[guild_id].update({"count": new_count, "last_user_id": message.author.id})
            save_data(self.data)
            if new_count % 100 == 0 and new_count != 0:
                try:
                    await message.add_reaction("💯")
                    await message.channel.send(f"🎉 გილოცავ მიაღწიე **{new_count}**-ს 🎉")
                except discord.Forbidden: pass
            else:
                try: await message.add_reaction("✅")
                except discord.Forbidden: pass
        else:
            try:
                await message.delete()
                error_msg = await message.channel.send(f"{message.author.mention} არაა სწორი შემდეგი რიცხვია **{current_count + 1}** დათვლა თავიდან დაიწყო")
                await error_msg.delete(delay=7)
            except discord.Forbidden: pass
            self.data[guild_id].update({"count": 0, "last_user_id": None})
            save_data(self.data)

    @c_group.command(name="on", description="აყენებს არხს დათვლისთვის")
    @app_commands.describe(channel="აირჩიეთ არხი სადაც დათვლა დაიწყება")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def setup_counting(self, interaction: discord.Interaction, channel: discord.TextChannel):
        guild_id = str(interaction.guild.id)
        self.data[guild_id] = {"channel_id": channel.id, "count": 0, "last_user_id": None}
        save_data(self.data)
        embed = discord.Embed(title="✅ დათვლის სისტემა დაყენებულია", description=f"დათვლა წარმატებით დაყენდა {channel.mention} არხზე\nდაიწყეთ **1**-ით!", color=discord.Color.green())
        embed.set_footer(text=self.footer_text)
        await interaction.response.send_message(embed=embed)

    @c_group.command(name="off", description="თიშავს დათვლის სისტემას სერვერზე")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def disable_counting(self, interaction: discord.Interaction):
        guild_id = str(interaction.guild.id)
        if guild_id in self.data:
            del self.data[guild_id]
            save_data(self.data)
            embed = discord.Embed(title="❌ დათვლის სისტემა გათიშულია", description="სისტემა ამ სერვერზე გაითიშა", color=discord.Color.red())
            embed.set_footer(text=self.footer_text)
            await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(title="⚠️ შეცდომა", description="სისტემა ამ სერვერზე უკვე გათიშულია", color=discord.Color.orange())
            embed.set_footer(text=self.footer_text)
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="leaderboard", description="აჩვენებს სერვერების დათვლის ლიდერბორდს")
    async def leaderboard(self, interaction: discord.Interaction):
        self.data = load_data()
        if not self.data:
            embed = discord.Embed(title="ლიდერბორდი ცარიელია", color=discord.Color.blue())
            embed.set_footer(text=self.footer_text)
            await interaction.response.send_message(embed=embed)
            return
        sorted_guilds = sorted(self.data.items(), key=lambda item: item[1].get('count', 0), reverse=True)
        embed = discord.Embed(title="🏆 დათვლის ლიდერბორდი", description="სერვერები ყველაზე მაღალი დათვლით:", color=discord.Color.gold())
        rank = 1
        for guild_id, guild_data in sorted_guilds[:10]:
            guild = self.bot.get_guild(int(guild_id))
            guild_name = guild.name if guild else f"უცნობი სერვერი (ID: {guild_id})"
            count = guild_data.get('count', 0)
            embed.add_field(name=f"{rank}. {guild_name}", value=f"**ქულა: {count}**", inline=False)
            rank += 1
        embed.set_footer(text=self.footer_text)
        await interaction.response.send_message(embed=embed)

    @setup_counting.error
    @disable_counting.error
    async def on_counting_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message("ამ ბრძანების უფლება არ გაქვს", ephemeral=True)
        else: raise error

async def setup(bot: commands.Bot):
    await bot.add_cog(CountingCog(bot))
