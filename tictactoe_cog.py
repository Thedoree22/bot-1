import discord
from discord.ext import commands
from discord import app_commands
from typing import List

class TicTacToeView(discord.ui.View):
    player1: discord.Member
    player2: discord.Member
    current_player: discord.Member
    children: List[discord.ui.Button]

    def __init__(self, player1, player2):
        super().__init__(timeout=180)
        self.player1 = player1
        self.player2 = player2
        self.current_player = player1
        for i in range(9):
            button = discord.ui.Button(label="\u200b", style=discord.ButtonStyle.secondary, row=i // 3)
            button.callback = self.button_callback
            self.add_item(button)

    async def button_callback(self, interaction: discord.Interaction):
        if interaction.user != self.current_player:
            await interaction.response.send_message("შენი სვლა არ არის!", ephemeral=True)
            return
        
        button = interaction.data["custom_id"]
        clicked_button = next(b for b in self.children if b.custom_id == button)

        if self.current_player == self.player1:
            clicked_button.label = "X"
            clicked_button.style = discord.ButtonStyle.danger
            self.current_player = self.player2
            next_turn_text = f"ახლა {self.player2.mention}-ის სვლაა (O)"
        else:
            clicked_button.label = "O"
            clicked_button.style = discord.ButtonStyle.success
            self.current_player = self.player1
            next_turn_text = f"ახლა {self.player1.mention}-ის სვლაა (X)"
        
        clicked_button.disabled = True
        winner = self.check_winner()
        if winner:
            for child in self.children:
                child.disabled = True
            await interaction.response.edit_message(content=f"🎉 **{winner.mention}**-მა მოიგო!", view=self)
            self.stop()
        elif all(child.disabled for child in self.children):
            await interaction.response.edit_message(content="ფრეა! 🤝", view=self)
            self.stop()
        else:
            await interaction.response.edit_message(content=next_turn_text, view=self)

    def check_winner(self):
        win_cond = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
        for combo in win_cond:
            a, b, c = combo
            if self.children[a].label != "\u200b" and self.children[a].label == self.children[b].label == self.children[c].label:
                return self.player1 if self.children[a].label == "X" else self.player2
        return None

class TicTacToeCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="tictactoe", description="იწყებს იქსიკი და ნოლიკის თამაშს.")
    @app_commands.describe(opponent="აირჩიე მოწინააღმდეგე.")
    async def tictactoe(self, interaction: discord.Interaction, opponent: discord.Member):
        player1 = interaction.user
        player2 = opponent
        if player2.bot or player1 == player2:
            await interaction.response.send_message("საკუთარ თავს ან ბოტს ვერ ეთამაშები!", ephemeral=True)
            return
        view = TicTacToeView(player1, player2)
        await interaction.response.send_message(
            content=f"**{player1.mention}** (X) vs **{player2.mention}** (O)\n\nახლა {player1.mention}-ის სვლაა!",
            view=view
        )

async def setup(bot: commands.Bot):
    await bot.add_cog(TicTacToeCog(bot))
