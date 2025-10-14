import discord
from discord.ext import commands
from discord import app_commands

class FunCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        # აქ ვინახავთ იმ მომხმარებლების სახელებს, ვისზეც ბრძანება არ იმუშავებს
        self.special_users = {"theodoree99", "nika_geims", "o.pixen"}

    @app_commands.command(name="gay", description="ამოწმებს, რამდენი პროცენტით არის მომხმარებელი გეი.")
    @app_commands.describe(user="აირჩიე მომხმარებელი, ვისი შემოწმებაც გინდა.")
    async def gay_command(self, interaction: discord.Interaction, user: discord.Member):
        """
        მთავარი ბრძანება, რომელიც ითვლის პროცენტს და აგზავნის პასუხს.
        """
        # 1. ვამოწმებთ, ხომ არ არის მომხმარებელი "სპეციალურ" სიაში
        # user.name იღებს მომხმარებლის სახელს დისქორდში (მაგ: theodoree99)
        if user.name in self.special_users:
            await interaction.response.send_message("ეს პიროვნება ბაზაში არ იძებნება X !", ephemeral=True)
            return # ვწყვეტთ ბრძანების მუშაობას

        # 2. ვიყენებთ მომხმარებლის უნიკალურ ID-ს, რომ პროცენტი ყოველთვის ერთი და იგივე იყოს.
        # user.id არის უნიკალური რიცხვი, რომელიც ყველა მომხმარებელს აქვს.
        # % 101 ნიშნავს, რომ ნებისმიერი რიცხვის 101-ზე გაყოფისას მიღებული ნაშთი იქნება 0-დან 100-მდე.
        # ეს უზრუნველყოფს, რომ კონკრეტული ID-სთვის პასუხი არასდროს შეიცვლება.
        percentage = user.id % 101

        # 3. პროცენტის მიხედვით ვირჩევთ შესაბამის GIF-ს
        gif_url = ""
        if percentage == 0:
            gif_url = "https://media1.tenor.com/m/pzsA8agH3aYAAAAC/giga-chad-chad.gif"
        elif percentage <= 20:
            gif_url = "https://media1.tenor.com/m/DprBEaWb3IAAAAAC/nah-i-dont-think-so.gif"
        elif percentage <= 50:
            gif_url = "https://media1.tenor.com/m/y-i9f5td_f0AAAAd/kinda-gay-lil-bit.gif"
        elif percentage == 69: # განსაკუთრებული შემთხვევა :)
            gif_url = "https://media1.tenor.com/m/O1oqdGblw9cAAAAC/licking-lips-nice.gif"
        elif percentage <= 80:
            gif_url = "https://media1.tenor.com/m/xBSyY9Yh5_4AAAAC/gay-pride.gif"
        elif percentage < 100:
            gif_url = "https://media1.tenor.com/m/3956mHE2c-QAAAAC/pride-parade-lgbt.gif"
        else: # 100%
            gif_url = "https://media1.tenor.com/m/p_Yj2T4k2vYAAAAC/super-gay-gay.gif"

        # 4. ვქმნით ლამაზ შეტყობინებას (Embed)
        embed = discord.Embed(
            title="🌈 Gay-o-Meter 3000 🌈",
            description=f"{user.mention} არის **{percentage}%**-ით გეი!",
            color=discord.Color.random() # Embed-ს ყოველ ჯერზე სხვადასხვა ფერი ექნება
        )
        embed.set_image(url=gif_url) # ვამატებთ GIF-ს

        # 5. ვაგზავნით პასუხს
        await interaction.response.send_message(embed=embed)

# ეს ფუნქცია საჭიროა, რომ ბოტმა შეძლოს ამ ფაილის ჩატვირთვა
async def setup(bot: commands.Bot):
    await bot.add_cog(FunCog(bot))
