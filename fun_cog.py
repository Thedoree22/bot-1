import discord
from discord.ext import commands
from discord import app_commands
import random # ვამატებთ random ბიბლიოთეკას

class FunCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.special_users = {"theodoree99", "nika_geims", "o.pixen"}

    @app_commands.command(name="gay", description="ამოწმებს, რამდენი პროცენტით არის მომხმარებელი გეი.")
    @app_commands.describe(user="აირჩიე მომხმარებელი, ვისი შემოწმებაც გინდა.")
    async def gay_command(self, interaction: discord.Interaction, user: discord.Member):
        if user.name in self.special_users:
            await interaction.response.send_message("ეს პიროვნება ბაზაში არ იძებნება X !", ephemeral=True)
            return

        percentage = user.id % 101
        
        gif_url = ""
        if percentage == 0: gif_url = "https://media1.tenor.com/m/pzsA8agH3aYAAAAC/giga-chad-chad.gif"
        elif percentage <= 20: gif_url = "https://media1.tenor.com/m/DprBEaWb3IAAAAAC/nah-i-dont-think-so.gif"
        elif percentage <= 50: gif_url = "https://media1.tenor.com/m/y-i9f5td_f0AAAAd/kinda-gay-lil-bit.gif"
        elif percentage == 69: gif_url = "https://media1.tenor.com/m/O1oqdGblw9cAAAAC/licking-lips-nice.gif"
        elif percentage <= 80: gif_url = "https://media1.tenor.com/m/xBSyY9Yh5_4AAAAC/gay-pride.gif"
        elif percentage < 100: gif_url = "https://media1.tenor.com/m/3956mHE2c-QAAAAC/pride-parade-lgbt.gif"
        else: gif_url = "https://media1.tenor.com/m/p_Yj2T4k2vYAAAAC/super-gay-gay.gif"

        embed = discord.Embed(title="🌈გეების მპოვნელი ტედის მონა🌈", description=f"{user.mention} არის **{percentage}%**-ით გეი!", color=discord.Color.random())
        embed.set_image(url=gif_url)
        await interaction.response.send_message(embed=embed)

    # --- Magic 8-Ball ბრძანება იწყება აქ ---
    @app_commands.command(name="8ball", description="დაუსვი კითხვა ჯადოსნურ ბურთს!")
    @app_commands.describe(question="შენი კითხვა...")
    async def eight_ball(self, interaction: discord.Interaction, question: str):
        responses = [
            # პოზიტიური პასუხები
            "რა თქმა უნდა!", "ეჭვგარეშეა.", "დაეყრდენი მაგას.", "დიახ, აუცილებლად.", "ჩემი აზრით, კი.", "დიდი შანსია.",
            # ნეიტრალური პასუხები
            "ბუნდოვანი პასუხია, სცადე თავიდან.", "ახლა ვერ გიწინასწარმეტყველებ.", "ჯობს ახლა არ გითხრა.", "ნიშნები ამაზე მიუთითებს.",
            # ნეგატიური პასუხები
            "არ დაეყრდნო მაგას.", "ჩემი პასუხია 'არა'.", "ჩემი წყაროები ამბობენ 'არა'.", "ძალიან საეჭვოა.", "არა მგონია.",
            # სახალისო/ქართული პასუხები
            "რავი აბა, ძმა.", "ეგ კითხე მიშას.", "50/50-ზეა რა.", "ხვალ გეტყვი.", "ვარსკვლავები არ არიან განწყობაზე.",
            "კი, მარა მერე არ ინანო.", "მამაოს კითხე ეგ.", "ეგ შენზეა დამოკიდებული.",
            # შენი მოთხოვნილი პასუხები
            "ხვალ მოკვდები.", "ხვალ ცოლს მოიყვან.", "გამდიდრდები, მარა ბედნიერი არ იქნები.", "შენს კითხვაზე პასუხი ხინკალშია.",
            "კი... თუ ლატარიას მოიგებ."
        ]
        
        answer = random.choice(responses)

        embed = discord.Embed(
            title="🔮 ჯადოსნური ბურთი ამბობს... 🔮",
            color=discord.Color.dark_purple()
        )
        embed.add_field(name="❓ შენი კითხვა:", value=f"```{question}```", inline=False)
        embed.add_field(name="💬 პასუხი:", value=f"```{answer}```", inline=False)
        embed.set_thumbnail(url="https://i.imgur.com/QЗаZ9n8.png") # 8ball სურათი

        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(FunCog(bot))
