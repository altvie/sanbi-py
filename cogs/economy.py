import discord
from discord.ext import commands
from discord import app_commands
from core import users as user_db
from core import core_economy as eco
from datetime import datetime
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

    embed = discord.Embed(
      title=f"{interaction.user.name}'s Balance",
      color=discord.Color.blurple()
    )
    embed.add_field(name="💰 Wallet", value=f"${wallet}")
    embed.add_field(name="🏦 Bank", value=f"${bank}")
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

  async def cog_load(self):
    if self.env == "dev" and self.guild_id:
      guild = discord.Object(id=self.guild_id)
      self.bot.tree.add_command(self.balance, guild=guild)
      self.bot.tree.add_command(self.daily, guild=guild)
      self.bot.tree.add_command(self.work, guild=guild)
    else:
      self.bot.tree.add_command(self.balance)
      self.bot.tree.add_command(self.daily)
      self.bot.tree.add_command(self.work)

async def setup(bot):
  await bot.add_cog(Economy(bot))