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

    await interaction.response.send_message("Pong 🏓...")

    end_time = time.time()
    diff = round((end_time - start_time) * 1000)
    ping = round(self.bot.latency * 1000)

    content = f"Pong 🏓! - (Round trip took: `{diff}ms`. Heartbeat: `{ping}ms`.)"
    await interaction.edit_original_response(content=content)

async def setup(bot):
  await bot.add_cog(General(bot))