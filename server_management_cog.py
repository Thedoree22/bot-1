import discord
from discord.ext import commands, tasks
from discord import app_commands
import json
import os
import requests
import datetime
import dateutil.parser

NOTIFY_DB = "notifications.json"
STATS_DB = "server_stats.json"

def load_data(file):
    if not os.path.exists(file): return {}
    try:
        with open(file, "r") as f: return json.load(f)
    except json.JSONDecodeError: return {}

def save_data(data, file):
    with open(file, "w") as f: json.dump(data, f, indent=4)

class ServerManagementCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.twitch_access_token = None
        # ვიწყებთ ყველა ფონურ პროცესს
        self.check_streams.start()
        self.update_stats.start()

    def cog_unload(self):
        self.check_streams.cancel()
        self.update_stats.cancel()

    # --- /clear ბრძანება ---
    @app_commands.command(name="clear", description="Shlis shetyobinebebs arkhshi")
    @app_commands.describe(amount="raodenoba (max: 100)")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def clear(self, interaction: discord.Interaction, amount: int):
        if amount > 100:
            await interaction.response.send_message("100-ze meti shetyobinebis washlis ufleba ar maqvs!", ephemeral=True)
            return
        await interaction.response.defer(ephemeral=True)
        deleted = await interaction.channel.purge(limit=amount)
        await interaction.followup.send(f"Warmatebit waishala {len(deleted)} shetyobineba.")

    # --- /poll ბრძანება ---
    @app_commands.command(name="poll", description="Qmnis martiv gamokitkhvas")
    @app_commands.describe(question="gamokitkhvis kitkhva")
    async def poll(self, interaction: discord.Interaction, question: str):
        embed = discord.Embed(
            title="📊 გამოკითხვა",
            description=f"**{question}**",
            color=discord.Color.blue()
        )
        embed.set_footer(text=f"გამოკითხვა დაიწყო: {interaction.user.name}")
        
        await interaction.response.send_message("გამოკითხვა იქმნება...", ephemeral=True)
        msg = await interaction.channel.send(embed=embed)
        await msg.add_reaction("✅")
        await msg.add_reaction("❌")

    # --- Notifications ბრძანებები ---
    notify_group = app_commands.Group(name="notifications", description="YouTube da Twitch shetyobinebebi")
    @notify_group.command(name="setup", description="Ayenebs arkhs, sadac daideba shetyobinebebi")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def notify_setup(self, interaction: discord.Interaction, channel: discord.TextChannel):
        notify_data = load_data(NOTIFY_DB)
        guild_id = str(interaction.guild.id)
        if guild_id not in notify_data: notify_data[guild_id] = {}
        notify_data[guild_id]['channel_id'] = channel.id
        save_data(notify_data, NOTIFY_DB)
        await interaction.response.send_message(f"Shetyobinebebis arkhi dayenebulia {channel.mention}-ze.", ephemeral=True)

    @notify_group.command(name="add-youtube", description="Amatebs YouTube arkhs")
    @app_commands.describe(youtube_channel_id="YouTube arkhis ID (mag: UClgRkhTL3_hImCAmdLfDE4g)")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def add_youtube(self, interaction: discord.Interaction, youtube_channel_id: str):
        notify_data = load_data(NOTIFY_DB)
        guild_id = str(interaction.guild.id)
        if guild_id not in notify_data or 'channel_id' not in notify_data[guild_id]:
            await interaction.response.send_message("Jer /notifications setup brdzanebit daayenet arkhi!", ephemeral=True)
            return
        if 'youtube_channels' not in notify_data[guild_id]: notify_data[guild_id]['youtube_channels'] = {}
        notify_data[guild_id]['youtube_channels'][youtube_channel_id] = {'last_video_id': None}
        save_data(notify_data, NOTIFY_DB)
        await interaction.response.send_message(f"YouTube arkhi `{youtube_channel_id}` damatebulia.", ephemeral=True)

    @notify_group.command(name="add-twitch", description="Amatebs Twitch arkhs")
    @app_commands.describe(username="Twitch arkhis saxeli")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def add_twitch(self, interaction: discord.Interaction, username: str):
        notify_data = load_data(NOTIFY_DB)
        guild_id = str(interaction.guild.id)
        if guild_id not in notify_data or 'channel_id' not in notify_data[guild_id]:
            await interaction.response.send_message("Jer /notifications setup brdzanebit daayenet arkhi!", ephemeral=True)
            return
        if 'twitch_channels' not in notify_data[guild_id]: notify_data[guild_id]['twitch_channels'] = {}
        notify_data[guild_id]['twitch_channels'][username.lower()] = {'live': False}
        save_data(notify_data, NOTIFY_DB)
        await interaction.response.send_message(f"Twitch arkhi `{username}` damatebulia.", ephemeral=True)

    # --- Server Stats ბრძანებები ---
    stats_group = app_commands.Group(name="serverstats", description="Serveris statistikuri arkhebi")
    @stats_group.command(name="setup", description="Qmnis avtomaturad ganakhlebad statistikis arkhebs")
    @app_commands.describe(category="Kategoria, sadac unda sheiqmnas arkhebi")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def stats_setup(self, interaction: discord.Interaction, category: discord.CategoryChannel):
        stats_data = load_data(STATS_DB)
        guild_id = str(interaction.guild.id)
        
        # ვქმნით ხმოვან არხებს
        try:
            total_channel = await category.create_voice_channel("📊 სულ: 0")
            member_channel = await category.create_voice_channel("👤 ممebrebi: 0")
            bot_channel = await category.create_voice_channel("🤖 Botebi: 0")
            
            # ვუკრძალავთ ხალხს დაკავშირებას
            await total_channel.set_permissions(interaction.guild.default_role, connect=False)
            await member_channel.set_permissions(interaction.guild.default_role, connect=False)
            await bot_channel.set_permissions(interaction.guild.default_role, connect=False)

            stats_data[guild_id] = {
                "total_channel_id": total_channel.id,
                "member_channel_id": member_channel.id,
                "bot_channel_id": bot_channel.id
            }
            save_data(stats_data, STATS_DB)
            await interaction.response.send_message("Statistikis arkhebi sheqmnilia!", ephemeral=True)
            await self.update_stats_now(interaction.guild) # მყისიერი განახლება
        except Exception as e:
            await interaction.response.send_message(f"Shecdoma: {e}", ephemeral=True)

    # --- ფონური პროცესები (Loops) ---
    
    # ეს ფუნქცია მყისიერად ანახლებს სტატისტიკას /setup-ის მერე
    async def update_stats_now(self, guild: discord.Guild):
        stats_data = load_data(STATS_DB)
        guild_id = str(guild.id)
        if guild_id not in stats_data: return
        
        config = stats_data[guild_id]
        try:
            total_channel = self.bot.get_channel(config['total_channel_id'])
            member_channel = self.bot.get_channel(config['member_channel_id'])
            bot_channel = self.bot.get_channel(config['bot_channel_id'])
            
            member_count = len([m for m in guild.members if not m.bot])
            bot_count = len([m for m in guild.members if m.bot])
            
            if total_channel: await total_channel.edit(name=f"📊 სულ: {guild.member_count}")
            if member_channel: await member_channel.edit(name=f"👤 ممebrebi: {member_count}")
            if bot_channel: await bot_channel.edit(name=f"🤖 Botebi: {bot_count}")
        except Exception as e:
            print(f"Error updating stats for {guild.name}: {e}")

    # ეს ანახლებს სტატისტიკას ყოველ 10 წუთში
    @tasks.loop(minutes=10)
    async def update_stats(self):
        await self.bot.wait_until_ready()
        stats_data = load_data(STATS_DB)
        for guild in self.bot.guilds:
            if str(guild.id) in stats_data:
                await self.update_stats_now(guild)

    # ეს ამოწმებს Twitch/YouTube-ს ყოველ 2 წუთში
    @tasks.loop(minutes=2)
    async def check_streams(self):
        await self.bot.wait_until_ready()
        notify_data = load_data(NOTIFY_DB)
        
        # Twitch-ის შემოწმება
        try:
            client_id = os.environ['TWITCH_CLIENT_ID']
            client_secret = os.environ['TWITCH_CLIENT_SECRET']
            r = requests.post(f"https://id.twitch.tv/oauth2/token?client_id={client_id}&client_secret={client_secret}&grant_type=client_credentials")
            self.twitch_access_token = r.json()['access_token']
        except Exception:
            return # თუ გასაღებები არასწორია, ვჩერდებით

        yt_api_key = os.environ.get('YOUTUBE_API_KEY')

        for guild_id, data in notify_data.items():
            channel_id = data.get('channel_id')
            if not channel_id: continue
            channel = self.bot.get_channel(channel_id)
            if not channel: continue

            # YouTube
            if yt_api_key and 'youtube_channels' in data:
                for yt_id, yt_data in data['youtube_channels'].items():
                    try:
                        url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={yt_id}&maxResults=1&order=date&type=video&key={yt_api_key}"
                        response = requests.get(url).json()
                        latest_video = response['items'][0]
                        video_id = latest_video['id']['videoId']
                        if yt_data['last_video_id'] is None:
                             notify_data[guild_id]['youtube_channels'][yt_id]['last_video_id'] = video_id
                             save_data(notify_data, NOTIFY_DB)
                             continue
                        if yt_data['last_video_id'] != video_id:
                            notify_data[guild_id]['youtube_channels'][yt_id]['last_video_id'] = video_id
                            save_data(notify_data, NOTIFY_DB)
                            await channel.send(f"📢 **axali video!** {latest_video['snippet']['channelTitle']}-ma dado axali video:\nhttps://www.youtube.com/watch?v={video_id}")
                    except Exception as e:
                        print(f"YouTube check error: {e}")

            # Twitch
            if 'twitch_channels' in data:
                usernames = list(data['twitch_channels'].keys())
                try:
                    headers = {"Client-ID": client_id, "Authorization": f"Bearer {self.twitch_access_token}"}
                    params = [("user_login", name) for name in usernames]
                    response = requests.get("https://api.twitch.tv/helix/streams", headers=headers, params=params).json()
                    live_streams = {stream['user_login']: stream for stream in response.get('data', [])}
                    for username, twitch_data in data['twitch_channels'].items():
                        is_live = username in live_streams
                        was_live = twitch_data.get('live', False)
                        if is_live and not was_live:
                            stream_data = live_streams[username]
                            notify_data[guild_id]['twitch_channels'][username]['live'] = True
                            save_data(notify_data, NOTIFY_DB)
                            embed = discord.Embed(title=f"🔴 **LIVE!** {stream_data['user_name']} online-shia!", url=f"https://twitch.tv/{username}", description=stream_data.get('title', 'striimi daiwyo!'), color=0x6441a5)
                            embed.set_thumbnail(url=stream_data['thumbnail_url'].replace('{width}', '320').replace('{height}', '180'))
                            await channel.send(embed=embed)
                        elif not is_live and was_live:
                            notify_data[guild_id]['twitch_channels'][username]['live'] = False
                            save_data(notify_data, NOTIFY_DB)
                except Exception as e:
                    print(f"Twitch check error: {e}")

async def setup(bot: commands.Bot):
    await bot.add_cog(ServerManagementCog(bot))
