import discord
from discord.ext import commands
from discord import app_commands
from core import core_economy as eco
from datetime import datetime, timedelta
import os

class Economy(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.env = os.getenv("MODE", "prod").lower()
    self.guild_id = int(os.getenv("GUILD_ID", 0))
  
  @app_commands.command(name="balance", description="Check wallet & bank balance.")
  async def balance(self, interaction: discord.Interaction):
    eco.open_account(interaction.user.id)
    balance = eco.get_balance(interaction.user.id)
    embed = discord.Embed(
      title=f"{interaction.user.name}'s balance",
      color=discord.Color.blue()
    )
    embed.add_field(
      name="💰 Wallet",
      value=f"${balance['wallet']}"
    )
    embed.add_field(
      name="🏦 Bank",
      value=f"${balance['bank']}"
    )
    await interaction.response.send_message(embed=embed)

  @app_commands.command(name="daily", description="Ambil uang harian!")
  async def daily(self, interaction: discord.Interaction):
    data = eco.load_data()
    uid = str(interaction.user.id)
    eco.open_account(uid)
    today = datetime.utcnow().strftime("%Y-%m-%d")

    if data[uid]["last_daily"] == today:
      await interaction.response.send_message("❌ Kamu sudah mengambil daily hari ini!")
    else:
      reward = 500
      data[uid]["wallet"] += reward
      data[uid]["last_daily"] = today
      eco.save_data(data)
      await interaction.response.send_message(f"✅ Kamu mendapat ${reward} dari daily reward!")

  async def cog_load(self):
    if self.env == "dev" and self.guild_id:
      guild = discord.Object(id=self.guild_id)
      self.bot.tree.add_command(self.balance, guild=guild)
      self.bot.tree.add_command(self.daily, guild=guild)
    else:
      self.bot.tree.add_command(self.balance)
      self.bot.tree.add_command(self.daily)

async def setup(bot):
  await bot.add_cog(Economy(bot))