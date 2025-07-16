import discord
from discord.ext import commands
from datetime import datetime
import logging
import os
from core.embed import create_embed

logger = logging.getLogger(__name__)

class Events(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.channel_message_edit = int(os.getenv("LOG_MESSAGE_EDIT", 0))

  @commands.Cog.listener()
  async def on_message_edit(self, before, after):
    if before.author.bot or before.content == after.content:
      return

    logger.debug(f"Message edited in {before.guild.name} #{before.channel.name} by {before.author}")
    channel = self.bot.get_channel(self.channel_message_edit)
    if not channel:
      logger.warning("Channel ID not found or bot has no access.")
      return

    embed = create_embed(
      title="📃 Message Edited",
      color=discord.Color.orange(),
      fields=[
        (
          "Author",
          f"{before.author.mention} ({before.author})",
          True
        ),
        (
          "Channel",
          f"{before.channel.mention}",
          True
        ),
        (
          "Before",
          before.content[:500] + "..." if len(before.content) > 500 else before.content or "*No content*",
          False
        ),
        (
          "After",
          after.content[:500] + "..." if len(after.content) > 500 else after.content or "*No content*",
          False
        )
      ],
      footer=f"Message ID: {before.id}"
    )
    embed.timestamp = datetime.now()

    try:
      await channel.send(embed=embed)
    except discord.Forbidden:
      logger.warning(f"No permission to send edit log in {channel.name}")

async def setup(bot):
  await bot.add_cog(Events(bot))