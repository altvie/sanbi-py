import discord
from discord.ext import commands
from discord import app_commands
import time
import platform
import psutil
import os

class General(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @app_commands.command(name="ping", description="Check bot latency")
  async def ping(self, interaction: discord.Interaction):
    start_time = time.time()

    embed = discord.Emebed(
      title="🏓 Pong!",
      color=discord.Color.green()
    )

    # calculate latency
    latency = round(self.bot.latency * 1000)

    embed.add_field(
      name="Bot Latency",
      value=f"{latency}ms",
      inline=True
    )

    await interaction.response.send_message(embed=embed)

    # Calculate response time
    end_time = time.time()
    response_time = round((end_time - start_time) * 1000)

    embed.add_field(
      name="Response Time",
      value=f"{response_time}ms",
      inline=True
    )

    await interaction.edit_original_response(embed=embed)

async def setup(bot):
  await bot.add_cog(General(bot))