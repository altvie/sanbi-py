import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import logging
import asyncio
from pathlib import Path

# Load environemt variables
load_dotenv()

# Configure logging
logging.basicConfig(
  level=logging.INFO,
  format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
  handlers=[
    logging.StreamHandler()
  ]
)

logger = logging.getLogger(__name__)
logging.getLogger('discord').setLevel(logging.WARNING)

class DiscordBot(commands.Bot):
  def __init__(self):
    # Intents
    intents = discord.Intents.default()
    intents.message_content = True
    intents.guilds = True
    intents.members = True

    super().__init__(
      command_prefix='!',
      intents=intents,
      help_command=None,
      case_insensitive=True
    )

    self.initial_extensions = [
      'cogs.general',
      'cogs.help',
      'cogs.moderation',
      'cogs.utility'
    ]
  
  async def setup_hook(self):
    logger.info("Settings up bot...")

    # Load all cogs
    for extension in self.initial_extensions:
      try:
        await self.load_extension(extension)
        logger.info(f"Loaded extension: {extension}")
      except Exception as e:
        logger.error((f"Failed to load extension {extension}: {e}"))

    # Detect environment
    mode = os.getenv("MODE", "prod").lower()
    is_dev = mode == "dev"
    
    # Sync slash commands
    try:
      if is_dev:
        guild_id = int(os.getenv("GUILD_ID"))
        guild = discord.Object(id=guild_id)
        synced = await self.tree.sync(guild=guild)
        logger.info(f"(Dev) Synced {len(synced)} commands(s)")
      else:
        synced = await self.tree.sync()
        logger.info(f"(Prod) Synced {len(synced)} commands(s)")
    except Exception as e:
      logger.error(f"Failed to sync commands: {e}")
  
  # Called when the bot is ready
  async def on_ready(self):
    logger.info(f"{self.user} successfully logged in!")
    logger.info(f"Watching to {len(self.guilds)} guilds.")

    # Set bot status
    await self.change_presence(
      activity=discord.Activity(
        type=discord.ActivityType.watching,
        name='on development!'
      )
    )
  
  # Global error handler for prefix commands
  async def on_command_error(self, ctx, error):
    if isinstance(error, commands.CommandNotFound):
      return

    logger.error(f"Command error in {ctx.command}: {error}")
    await ctx.send(f"An error occurred: {error}")
  
async def main():
  token = os.getenv('BOT_TOKEN')
  if not token:
    logger.error("BOT_TOKEN not found in environment variables!")
    return

  # Create bot instance
  bot = DiscordBot()

  try:
    await bot.start(token)
  except discord.LoginFailure:
    logger.error("Invalid bot token!")
  except Exception as e:
    logger.error((f"An error occurred: {e}"))
  finally:
    await bot.close()

if __name__ == "__main__":
  try:
    asyncio.run(main())
  except KeyboardInterrupt:
    logger.info("Bot Stopped.")