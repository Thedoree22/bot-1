import discord
from discord.ext import commands
from discord import app_commands
import random

class FunCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.special_users = {"theodoree99", "nika_geims", "o.pixen"}

    # --- Gay Command (უცვლელი) ---
    @app_commands.command(name="gay", description="ამოწმებს, რამდენი პროცენტით არის მომხმარებელი გეი.")
    @app_commands.describe(user="აირჩიე მომხმარებელი, ვისი შემოწმებაც გინდა.")
    async def gay_command(self, interaction: discord.Interaction, user: discord.Member):
        if user.name in self.special_users:
            await interaction.response.send_message("ეს პიროვნება ბაზაში არ იძებნება X !", ephemeral=True)
            return
        percentage = user.id % 101
        # ... (დანარჩენი კოდი იგივეა) ...
        gif_url = ""
        if percentage == 0: gif_url = "https://media1.tenor.com/m/pzsA8agH3aYAAAAC/giga-chad-chad.gif"
        elif percentage <= 20: gif_url = "https://media1.tenor.com/m/DprBEaWb3IAAAAAC/nah-i-dont-think-so.gif"
        elif percentage <= 50: gif_url = "https://media1.tenor.com/m/y-i9f5td_f0AAAAd/kinda-gay-lil-bit.gif"
        elif percentage == 69: gif_url = "https://media1.tenor.com/m/O1oqdGblw9cAAAAC/licking-lips-nice.gif"
        elif percentage <= 80: gif_url = "https://media1.tenor.com/m/xBSyY9Yh5_4AAAAC/gay-pride.gif"
        elif percentage < 100: gif_url = "https://media1.tenor.com/m/3956mHE2c-QAAAAC/pride-parade-lgbt.gif"
        else: gif_url = "https://media1.tenor.com/m/p_Yj2T4k2vYAAAAC/super-gay-gay.gif"
        embed = discord.Embed(title="🌈 ტედის გეების საჭერი მონა 🌈", description=f"{user.mention} არის **{percentage}%**-ით გეი!", color=discord.Color.random())
        embed.set_image(url=gif_url)
        await interaction.response.send_message(embed=embed)

    # --- Magic 8-Ball (ლოგიკური პასუხებით) ---
    @app_commands.command(name="8ball", description="დაუსვი კითხვა ჯადოსნურ ბურთს!")
    @app_commands.describe(question="შენი კითხვა...")
    async def eight_ball(self, interaction: discord.Interaction, question: str):
        # კითხვის ანალიზი
        normalized_question = question.lower()
        answer = ""

        # პასუხების კატეგორიები
        when_responses = ["მალე, ძაან მალე.", "როცა ბიძინა იტყვის.", "არასდროს!", "მაშინ, როცა კურსი დალაგდება.", "ეგ უკვე მოხდა, უბრალოდ შენ არ იცი.", "შემდეგ სავსე მთვარეზე."]
        choice_responses = ["ცხადია, პირველი.", "მეორეს გირჩევდი, ძმა.", "არც ერთი! ორივე სისულელეა.", "ორივე, რატომაც არა?", "ძაან რთული კითხვაა, პას.", "მესამე ვარიანტი მოიფიქრე."]
        why_responses = ["იმიტომ!", "ეგ ღმერთს კითხე.", "კაი კითხვაა, პასუხი არ ვიცი.", "იმიტომ რომ ეგრეა საჭირო.", "ფიზიკის კანონებიდან გამომდინარე.", "პასუხი შენშია."]
        who_responses = ["შენ თვითონ.", "ვიღაც, ვისაც არ იცნობ.", "ეგ საიდუმლოა.", "პასუხს შენს გულში იპოვი.", "გეტყვი, მარა არავის უთხრა.", "შენი მომავალი მე."]
        general_responses = ["კი ძმაო, 100%-იანია!", "აბა რა!", "ეჭვიც არ შეგეპაროს.", "ვარსკვლავები ამბობენ დიახ!", "შანსი არაა!", "დაივიწყე ეგ ამბავი.", "არა, არავითარ შემთხვევაში.", "Может быть, может быть...", "რავი აბა...", "გააჩნია ხასიათზე თუ ვარ.", "იკითხე კარგად.", "ბაზარი არაა.", "ნწ.", "არა."]
        
        # ლოგიკა, რომელიც არჩევს პასუხის ტიპს
        if normalized_question.startswith("როდის"):
            answer = random.choice(when_responses)
        elif " ან " in normalized_question:
            answer = random.choice(choice_responses)
        elif normalized_question.startswith("რატომ"):
            answer = random.choice(why_responses)
        elif normalized_question.startswith("ვინ"):
            answer = random.choice(who_responses)
        else: # თუ კითხვა სტანდარტულია
            answer = random.choice(general_responses)

        # შემთხვევითი GIF-ები
        gif_urls = ["https://media1.tenor.com/m/AD5ggvJ22gIAAAAd/magic-8-ball-magic.gif", "https://media1.tenor.com/m/8xke_3aL0CgAAAAC/magic-8-ball-answer.gif", "https://media1.tenor.com/m/jJ98i7fK3AIAAAAC/magic-8-ball.gif"]
        random_gif = random.choice(gif_urls)

        # დიზაინი
        embed = discord.Embed(
            title="🔮 ჯადოსნური ბურთი",
            description=f"**შენ იკითხე:**\n*{question}*",
            color=0x7b2fde
        )
        embed.add_field(name="ბურთის პასუხი:", value=f"## {answer}", inline=False)
        embed.set_image(url=random_gif)
        embed.set_footer(text="ბურთი არასდროს ცდება... (თითქმის)")

        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(FunCog(bot))
