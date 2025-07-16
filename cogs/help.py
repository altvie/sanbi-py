import discord
from discord.ext import commands
from discord import app_commands, SelectOption
from discord.ui import View, Select
from core.command import register_commands
from core.embed import create_embed
import os

class HelpDropdown(Select):
  def __init__(self):
    self.command_categories = {
      "General": [
        ("/ping", "Check bot latency."),
        ("/say", "Make the bot say something."),
      ],
      "Utility": [
        ("/userinfo", "Show user information."),
        ("/serverinfo", "Show server information."),
        ("/avatar", "Get a user's avatar."),
      ],
      "Moderation": [
        ("/kick", "Kick user from server."),
        ("/ban", "Banned user from server."),
        ("/unban", "Unbanned user from server by user id."),
      ]
    }

    options = [
      SelectOption(label=cat, description=f"Show command {cat}", value=cat)
      for cat in self.command_categories
    ]

    super().__init__(
      placeholder="Select...",
      min_values=1,
      max_values=1,
      options=options
    )

  async def callback(self, interaction: discord.Interaction):
    selected = self.values[0]
    fields = [(name, desc, False) for name, desc in self.command_categories[selected]]

    embed = create_embed(
      title=f"{selected} Commands",
      description=f"Here are the commands under **{selected}**:",
      color=discord.Color.green(),
      fields=fields
    )

    for name, desc in self.command_categories[selected]:
      embed.add_field(name=name, value=desc, inline=False)

    await interaction.response.edit_message(embed=embed, view=self.view)


class HelpView(View):
  def __init__(self):
    super().__init__(timeout=180)
    self.add_item(HelpDropdown())


class Help(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.env = os.getenv("MODE", "prod").lower()
    self.guild_id = int(os.getenv("GUILD_ID", 0))

  @app_commands.command(name="help", description="Show bot commands list")
  async def help(self, interaction: discord.Interaction):
    view = HelpView()
    embed = create_embed(
      title="📖 Help Menu",
      description="Select a category from the dropdown menu below to view commands.",
      color=discord.Color.blurple()
    )
    await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
  
  async def cog_load(self):
    if self.env == "dev" and self.guild_id:
      register_commands(self.bot, self, guild_id=self.guild_id)
    else:
      register_commands(self.bot, self)

async def setup(bot):
  await bot.add_cog(Help(bot))