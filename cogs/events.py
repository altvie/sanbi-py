import discord
from discord.ext import commands
from datetime import datetime
from config import LOG_MESSAGE_EDIT, logger

class Events(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_message_edit(self, before, after):
    if before.author.bot or before.content == after.content:
      return

    logger.debug(f"Message edited in {before.guild.name} #{before.channel.name} by {before.author}")
    channel = self.bot.get_channel(LOG_MESSAGE_EDIT)
    if not channel:
      logger.warning("Channel ID not found or bot has no access.")
      return

    if channel:
      embed = discord.Embed(
        title="📃 Message Edited",
        color=discord.Color.orange()
      )
      embed.add_field(
        name="Author",
        value=f"{before.author.mention} ({before.author})",
        inline=True
      )
      embed.add_field(
        name="Channel",
        value=f"{before.channel.mention}",
        inline=True
      )
      embed.add_field(
        name="Before",
        value=before.content[:500] + "..." if len(before.content) > 500 else before.content or "*No content*",
        inline=False
      )
      embed.add_field(
        name="After",
        value=after.content[:500] + "..." if len(after.content) > 500 else after.content or "*No content*",
        inline=False
      )
      embed.set_footer(text=f"Message ID: {before.id}")
      embed.timestamp = datetime.now()

      try:
        await channel.send(embed=embed)
      except discord.Forbidden:
        logger.warning(f"No permission to send edit log in {channel.name}")

async def setup(bot):
  await bot.add_cog(Events(bot))