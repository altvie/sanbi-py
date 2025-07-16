import discord
from discord.ext import commands
from discord import app_commands
from typing import Optional
from core.command import register_commands
from core.embed import create_embed
import asyncio
import os

class Moderation(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.env = os.getenv("MODE", "prod").lower()
    self.guild_id = int(os.getenv("GUILD_ID", 0))
    self.owned_id = int(os.getenv("BOT_OWNER_ID", 0))

  @app_commands.command(name="sync", description="Sync all application commands (owner only)")
  async def sync_commands(self, interaction: discord.Interaction):
    if interaction.user.id != self.owned_id:
      await interaction.response.send_message("`❌` You don't have persmission to use rhis command.", ephemeral=True)
      return

    try:
      synced = await self.bot.tree.sync()
      await interaction.response.send_message(f"`✅` Synced {len(synced)} commands globally.", ephemeral=True)
    except Exception as e:
      await interaction.response.send_message(f"`❌` Failed to sync: {e}", ephemeral=True)

  @app_commands.command(name="kick", description="Kick a user from the server")
  @app_commands.describe(
    user="The user to kick",
    reason="Reason for the kick"
  )
  @app_commands.default_permissions(kick_members=True)
  async def kick(
    self,
    interaction: discord.Interaction,
    user: discord.Member,
    reason: Optional[str] = "No reason provided"
  ):
    if not interaction.user.guild_permissions.kick_members:
      await interaction.response.send_message("❌ You don't have permission to kick members!", ephemeral=True)
      return

    if user.top_role >= interaction.user.top_role:
      await interaction.response.send_message("❌ You cannot kick this user!", ephemeral=True)
      return

    if user == interaction.user:
      await interaction.response.send_message("❌ You cannot kick yourself!", ephemeral=True)
      return

    try:
      try:
        embed = create_embed(
          title="🦶 You have been kicked",
          description=f"You have been kicked from **{interaction.guild.name}**",
          color=discord.Color.orange(),
          fields=[
            ("Reason", reason, False),
            ("Moderator", interaction.user.mention, False)
          ]
        )
        await user.send(embed=embed)
      except:
        pass

      await user.kick(reason=f"{reason} - By {interaction.user}")

      embed = create_embed(
        title="✅ User Kicked",
        description=f"{user.mention} has been kicked.",
        color=discord.Color.green(),
        fields=[
          ("Reason", reason, False)
        ]
      )
      await interaction.response.send_message(embed=embed)

    except discord.Forbidden:
      await interaction.response.send_message("❌ I don't have permission to kick this user!", ephemeral=True)
    except Exception as e:
      await interaction.response.send_message(f"❌ An error occurred: {e}", ephemeral=True)

  @app_commands.command(name="ban", description="Ban a user from the server")
  @app_commands.describe(
    user="The user to ban",
    reason="Reason for the ban",
    delete_messages="Delete messages from the last X days (0-7)"
  )
  @app_commands.default_permissions(ban_members=True)
  async def ban(
    self,
    interaction: discord.Interaction,
    user: discord.Member,
    reason: Optional[str] = "No reason provided",
    delete_messages: Optional[int] = 0
  ):
    if not interaction.user.guild_permissions.ban_members:
      await interaction.response.send_message("❌ You don't have permission to ban members!", ephemeral=True)
      return

    if delete_messages < 0 or delete_messages > 7:
      await interaction.response.send_message("❌ Delete messages must be between 0 and 7 days!", ephemeral=True)
      return

    if user.top_role >= interaction.user.top_role:
      await interaction.response.send_message("❌ You cannot ban this user!", ephemeral=True)
      return

    if user == interaction.user:
      await interaction.response.send_message("❌ You cannot ban yourself!", ephemeral=True)
      return

    try:
      try:
        embed = create_embed(
          title="🔨 You have been banned",
          description=f"You have been banned from **{interaction.guild.name}**",
          color=discord.Color.red(),
          fields=[("Reason", reason, False)]
        )
        await user.send(embed=embed)
      except:
        pass

      await user.ban(reason=f"{reason} - By {interaction.user}", delete_message_days=delete_messages)

      embed = create_embed(
        title="✅ User Banned",
        description=f"{user.mention} has been banned.",
        color=discord.Color.green(),
        fields=[("Reason", reason, False)]
      )
      await interaction.response.send_message(embed=embed)

    except discord.Forbidden:
      await interaction.response.send_message("❌ I don't have permission to ban this user!", ephemeral=True)
    except Exception as e:
      await interaction.response.send_message(f"❌ An error occurred: {e}", ephemeral=True)

  @app_commands.command(name="unban", description="Unban a user by ID")
  @app_commands.describe(
    user_id="The ID of the user to unban",
    reason="Reason for unbanning"
  )
  @app_commands.default_permissions(ban_members=True)
  async def unban(
    self,
    interaction: discord.Interaction,
    user_id: str,
    reason: Optional[str] = "No reason provided"
  ):
    if not interaction.user.guild_permissions.ban_members:
      await interaction.response.send_message("❌ You don't have permission to unban members!", ephemeral=True)
      return

    try:
      user_id = int(user_id)
      user = None

      async for ban_entry in interaction.guild.bans():
        if ban_entry.user.id == user_id:
          user = ban_entry.user
          break

      if not user:
        await interaction.response.send_message("❌ User is not banned!", ephemeral=True)
        return

      await interaction.guild.unban(user, reason=f"{reason} - By {interaction.user}")
      embed = create_embed(
        title="✅ User Unbanned",
        description=f"{user} has been unbanned.",
        color=discord.Color.green()
      )
      await interaction.response.send_message(embed=embed)

    except Exception as e:
      await interaction.response.send_message(f"❌ An error occurred: {e}", ephemeral=True)

  async def cog_load(self):
    if self.env == "dev" and self.guild_id:
      register_commands(self.bot, self, guild_id=self.guild_id)
    else:
      register_commands(self.bot, self)

async def setup(bot):
  await bot.add_cog(Moderation(bot))
