import discord
from discord import app_commands

def register_commands(bot, cog, guild_id=None):
  for attr_name in dir(cog):
    attr = getattr(cog, attr_name)
    if isinstance(attr, app_commands.Command):
      try:
        if guild_id:
          bot.tree.add_command(attr, guild=discord.Object(id=guild_id))
        else:
          bot.tree.add_command(attr)
      except app_commands.errors.CommandAlreadyRegistered:
        pass