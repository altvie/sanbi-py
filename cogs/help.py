import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import View
from core.command import register_commands
from core.embed import create_embed
import os

CATEGORY_EMOJIS = {
  "General": "📌",
  "Utility": "🛠️",
  "Moderation": "🔨",
  "Economy": "💰"
}

class HelpButton(discord.ui.Button):
  def __init__(self, category_name, commands):
    emoji = CATEGORY_EMOJIS.get(category_name, "")
    super().__init__(
      label=f"{emoji} {category_name}",
      style=discord.ButtonStyle.blurple,
      custom_id=category_name
    )
    self.category_name = category_name
    self.commands = commands

  async def callback(self, interaction: discord.Interaction):
    fields = [
      (f"`{name}`", desc or "No description", False)
      for name, desc in self.commands
    ]

    embed = create_embed(
      title=f"{CATEGORY_EMOJIS.get(self.category_name, '')} {self.category_name} Commands",
      description=f"Here are the commands under **{self.category_name}**:",
      color=discord.Color.green(),
      fields=fields
    )

    await interaction.response.edit_message(embed=embed, view=self.view)

class HelpView(View):
  def __init__(self, bot: commands.Bot, user: discord.User, categories: dict, is_owner: bool):
    super().__init__(timeout=180)
    for name in categories:
      if name == "Moderation" and not is_owner: # Only bot owner can view Moderation command (you can change this)
        continue
      self.add_item((HelpButton(name, categories[name])))

class Help(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.env = os.getenv("MODE", "prod").lower()
    self.guild_id = int(os.getenv("GUILD_ID", 0))
    self.owner_id = int(os.getenv("BOT_OWNER_ID", 0))

  @app_commands.command(name="help", description="Show bot commands list")
  async def help(self, interaction: discord.Interaction):
    commands_list = self.bot.tree.get_commands()
    is_owner = interaction.user.id == self.owner_id

    categories = {}

    for cmd in commands_list:
      if not cmd.name or not cmd.description:
        continue

      category = cmd.module.split('.')[-1].capitalize() if cmd.module else "General"
      if category == "Moderation" and not is_owner:
        continue

      if category not in categories:
        categories[category] = []

      categories[category].append((f"/{cmd.name}", cmd.description))

    if not categories:
      await interaction.response.send_message("❌ No commands available.", ephemeral=True)
      return
    
    view = HelpView(self.bot, interaction.user, categories, is_owner)

    embed = create_embed(
      title="📖 Help Menu",
      description="Click a button below to view command categories.",
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