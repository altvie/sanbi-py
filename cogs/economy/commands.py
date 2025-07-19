import discord
from discord.ext import commands
from discord import app_commands
from core import users as user_db
from core import economy as eco
from core.command import register_commands
from datetime import datetime
from core.embed import create_embed
import os, random

class Economy(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.env = os.getenv("MODE", "prod").lower()
    self.guild_id = int(os.getenv("GUILD_ID", 0))

  @app_commands.command(name="balance", description="Check wallet & bank balance.")
  async def balance(self, interaction: discord.Interaction):
    user_db.open_account(interaction.user)
    wallet = eco.get_wallet(interaction.user.id)
    bank = eco.get_bank(interaction.user.id)

    embed = create_embed(
      title=f"{interaction.user.name}'s Balance",
      fields=[
        (
          "💰 Wallet",
          f"${wallet}",
          True
        ),
        (
          "🏦 Bank",
          f"${bank}",
          True
        )
      ]
    )
    await interaction.response.send_message(embed=embed)

  @app_commands.command(name="daily", description="Claim your daily reward")
  async def daily(self, interaction: discord.Interaction):
    user = interaction.user
    uid = str(user.id)
    today = datetime.now().strftime("%Y-%m-%d")

    user_db.open_account(user)
    data = user_db.load_data()

    if data[uid]["economy"]["last_daily"] == today:
      await interaction.response.send_message("`❌` You already claimed today's reward.")
    else:
      reward = 500
      data[uid]["economy"]["wallet"] += reward
      data[uid]["economy"]["last_daily"] = today
      eco.update_stat(uid, "daily_claimed")
      user_db.save_data(data)
      await interaction.response.send_message(f"`✅` You received $`{reward}` from daily!")

  @app_commands.command(name="work", description="Work to earn money")
  async def work(self, interaction: discord.Interaction):
    user = interaction.user
    user_db.open_account(user)
    earned = random.randint(100, 300)
    eco.update_wallet(user.id, earned)
    eco.update_stat(user.id, "work_count")
    await interaction.response.send_message(f"`💼` You earned ${earned} from working!")

  @app_commands.command(name="deposit", description="Deposit money to your bank account")
  @app_commands.describe(amount="Amount of money to deposit (use 'all' to deposit everything)")
  async def deposit(self, interaction: discord.Interaction, amount: str):
    user = interaction.user
    user_db.open_account(user)
    uid = str(user.id)
    wallet_balance = eco.get_wallet(uid)

    if amount.lower() == "all":
      amount = wallet_balance
    else:
      if not amount.isdigit() or int(amount) <= 0:
        await interaction.response.send_message("`❌` Please enter a valid amount.", ephemeral=True)
        return
      amount = int(amount)

    if wallet_balance < amount:
      await interaction.response.send_message("`❌` You don't have enough funds in your wallet.", ephemeral=True)
      return

    eco.update_wallet(uid, -amount)
    eco.update_bank(uid, amount)
    await interaction.response.send_message(f"`🏦` Deposited $`{amount}` to your bank.")

  @app_commands.command(name="withdraw", description="Withdraw money from your bank account")
  @app_commands.describe(amount="Amount of money to withdraw (use 'all' to withdraw everything)")
  async def withdraw(self, interaction: discord.Interaction, amount: str):
    user = interaction.user
    user_db.open_account(user)
    uid = str(user.id)
    bank_balance = eco.get_bank(uid)

    if amount.lower() == "all":
      amount = bank_balance
    else:
      if not amount.isdigit() or int(amount) <= 0:
        await interaction.response.send_message("`❌` Please enter a valid amount.", ephemeral=True)
        return
      amount = int(amount)

    if bank_balance < amount:
      await interaction.response.send_message("`❌` You don't have enough funds in your bank.", ephemeral=True)
      return

    eco.update_bank(uid, -amount)
    eco.update_wallet(uid, amount)
    await interaction.response.send_message(f"`💸` Withdrew $`{amount}` from your bank.")

  @app_commands.command(name="coinflip", description="Flip a coin and test your luck!")
  @app_commands.describe(choice="Choose between 'head' or 'tail'", amount="Amount of coins to bet")
  async def coinflip(self, interaction: discord.Interaction, choice: str, amount: int):
    choice = choice.lower()
    if choice not in ["head", "tail"]:
      await interaction.response.send_message("`❌` Please choose either 'head' or 'tail'.", ephemeral=True)
      return
    
    user_id = str(interaction.user.id)
    balance = eco.get_wallet(user_id)

    if amount <= 0:
      await interaction.response.send_message("❌ Bet amount must be greater than 0.", ephemeral=True)
      return

    if amount > balance:
      await interaction.response.send_message("❌ You don't have enough coins for this bet.", ephemeral=True)
      return

    result = random.choice(["head", "tail"])
    win = result == choice

    if win:
      eco.update_wallet(user_id, amount)
      msg = f"🎉 The coin landed on **{result}**! You won **{amount}** coins!"
    else:
      eco.update_wallet(user_id, -amount)
      msg = f"💀 The coin landed on **{result}**. You lost **{amount}** coins."

    embed = create_embed(
      title="🪙 Coinflip",
      description=msg
    )
    await interaction.response.send_message(embed=embed)

  async def cog_load(self):
    if self.env == "dev" and self.guild_id:
      register_commands(self.bot, self, guild_id=self.guild_id)
    else:
      register_commands(self.bot, self)

async def setup(bot):
  await bot.add_cog(Economy(bot))