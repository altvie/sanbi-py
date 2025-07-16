import discord
from discord.ext import commands
from discord import app_commands
from typing import Optional
from core.command import register_commands
from core.embed import create_embed
import os

class Utility(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.env = os.getenv("MODE", "prod").lower()
    self.guild_id = int(os.getenv("GUILD_ID", 0))

  @app_commands.command(name="userinfo", description="Get information about a user")
  @app_commands.describe(user="The user to get information about")
  async def userinfo(self, interaction: discord.Interaction, user: Optional[discord.Member] = None):
    if user is None:
      user = interaction.user

    # Dates
    created_at = user.created_at.strftime("%B %d, %Y")
    joined_at = user.joined_at.strftime("%B %d, %Y") if user.joined_at else "Unknown"

    # Status
    status_emoji = {
      discord.Status.online: "🟢",
      discord.Status.idle: "🟡",
      discord.Status.dnd: "🔴",
      discord.Status.offline: "⚫"
    }

    # Roles
    roles = [role.mention for role in user.roles[1:]]  # skip @everyone
    roles_text = ", ".join(roles[:10]) if roles else "None"
    if len(roles) > 10:
      roles_text += f" and {len(roles) - 10} more..."

    embed = create_embed(
      title=f"👤 User Information - {user}",
      color=user.color if user.color != discord.Color.default() else discord.Color.blue(),
      fields=[
        (
          "📋 Basic Info",
          f"**Username:** {user.name}\n**Display Name:** {user.display_name}\n**ID:** {user.id}\n**Bot:** {'Yes' if user.bot else 'No'}",
          True
        ),
        (
          "📅 Dates",
          f"**Created:** {created_at}\n**Joined:** {joined_at}",
          True
        ),
        (
          "📱 Status",
          f"**Status:** {status_emoji.get(user.status, '❓')} {user.status}\n**Activity:** {user.activity.name if user.activity else 'None'}",
          True
        ),
        (
          f"🎭 Roles ({len(user.roles) - 1})",
          roles_text,
          True
        )
      ],
      thumbnail=user.avatar.url if user.avatar else None
    )

    await interaction.response.send_message(embed=embed)

  @app_commands.command(name="serverinfo", description="Get information about the server")
  async def serverinfo(self, interaction: discord.Interaction):
    guild = interaction.guild

    embed = discord.Embed(
      title=f"🏰 Server Information - {guild.name}",
      color=discord.Color.purple()
    )

    if guild.icon:
      embed.set_thumbnail(url=guild.icon.url)

    embed.add_field(
      name="📋 Basic Info",
      value=f"**Name:** {guild.name}\n"
            f"**ID:** {guild.id}\n"
            f"**Owner:** {guild.owner.mention if guild.owner else 'Unknown'}\n"
            f"**Created:** {guild.created_at.strftime('%B %d, %Y')}",
      inline=True
    )

    total_members = guild.member_count
    online_members = len([m for m in guild.members if m.status != discord.Status.offline])
    bot_count = len([m for m in guild.members if m.bot])

    embed.add_field(
      name="👥 Members",
      value=f"**Total:** {total_members}\n"
            f"**Online:** {online_members}\n"
            f"**Bots:** {bot_count}\n"
            f"**Humans:** {total_members - bot_count}",
      inline=True
    )

    text_channels = len(guild.text_channels)
    voice_channels = len(guild.voice_channels)
    categories = len(guild.categories)

    embed.add_field(
      name="📺 Channels",
      value=f"**Text:** {text_channels}\n"
            f"**Voice:** {voice_channels}\n"
            f"**Categories:** {categories}\n"
            f"**Total:** {text_channels + voice_channels}",
      inline=True
    )

    features = []
    if guild.premium_tier > 0:
      features.append(f"Nitro Boost Level {guild.premium_tier}")
    if guild.premium_subscription_count:
      features.append(f"{guild.premium_subscription_count} Boosts")
    if guild.verification_level != discord.VerificationLevel.none:
      features.append(f"Verification: {guild.verification_level.name.title()}")

    if features:
      embed.add_field(
        name="✨ Features",
        value="\n".join(features),
        inline=False
      )

    embed.add_field(
      name="🎭 Roles",
      value=f"**Count:** {len(guild.roles)}",
      inline=True
    )

    embed.add_field(
      name="😀 Emojis",
      value=f"**Count:** {len(guild.emojis)}",
      inline=True
    )

    await interaction.response.send_message(embed=embed)

  @app_commands.command(name="avatar", description="Get a user's avatar")
  @app_commands.describe(user="The user to get the avatar of")
  async def avatar(self, interaction: discord.Interaction, user: Optional[discord.Member] = None):
    if user is None:
      user = interaction.user

    embed = discord.Embed(
      title=f"🖼️ Avatar - {user.display_name}",
      color=user.color if user.color != discord.Color.default() else discord.Color.blue()
    )

    if user.avatar:
      embed.set_image(url=user.avatar.url)
      embed.add_field(
        name="Links",
        value=f"[PNG]({user.avatar.with_format('png').url}) | "
              f"[JPG]({user.avatar.with_format('jpg').url}) | "
              f"[WEBP]({user.avatar.with_format('webp').url})",
        inline=False
      )
    else:
      embed.description = "User has no custom avatar"
      embed.set_image(url=user.default_avatar.url)

    await interaction.response.send_message(embed=embed)

  async def cog_load(self):
    if self.env == "dev" and self.guild_id:
      register_commands(self.bot, self, guild_id=self.guild_id)
    else:
      register_commands(self.bot, self)

async def setup(bot):
  await bot.add_cog(Utility(bot))