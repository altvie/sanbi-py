# 🤖 Sanbi Bot Python
### Discord bot using Python.

---

## 🌳 Project Structure
```
sanbi-py/
├── main.py                 # Main bot file
├── cogs/
│   ├── __init__.py
│   ├── general.py          # General commands (ping, info, help)
│   ├── moderation.py       # Moderation commands (kick, ban, clear)
│   ├── utility.py          # Utility commands (userinfo, serverinfo, avatar)
│   ├── events.py           # Event listeners (join/leave, message logs)
│   ├── help.py             # Help command
│   └── economy.py          # Economy commands (balance, daily, work, gamble)
├── core/
│   ├── __init__.py
│   ├── command.py          # register_command
│   ├── core_economy.py     # Economy function (get_wallet, etc)
│   ├── embed.py            # Reusable embed function (create_embed)
│   └── users.py            # User function (load_data, save_data, etc)
├── data/
│   ├── users.json          # User database
├── .env.example            # Environment variables example
├── .gitignore              # Git ignore file
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

---

## 📦 Installation 
1. **Clone the repository**
    ```bash
    git clone https://github.com/altvie/sanbi-py.git
    cd sanbi-py
    ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` change with your own value:
   ```bash
   BOT_TOKEN=your_bot_token
   BOT_OWNER_ID=your_owner_id

   CLIENT_ID=your_application_id
   GUILD_ID=your_test_guild_id

   LOG_MESSAGE_EDIT=your_channel_id

   # prod = production | dev=development
   MODE=dev
   ```

5. **Run the bot**
   ```bash
   python main.py # Linux: python3 main.py
   ```

---

## 🔧 Development

### Adding New Commands
1. Create a new cog file in the `cogs/` directory
2. Import the cog in `main.py` by adding it to `initial_extensions`
3. Use the `@app_commands.command()` decorator for slash commands

### Example Cog Structure
```python
import discord
from discord.ext import commands
from discord import app_commands
from core.command import register_commands
import os

class MyCog(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.env = os.getenv("MODE", "prod").lower()
    self.guild_id = int(os.getenv("GUILD_ID", 0))
    
  @app_commands.command(name="mycommand", description="My command description")
  async def my_command(self, interaction: discord.Interaction):
    await interaction.response.send_message("Hello!")
    
  async def cog_load(self):
  if self.env == "dev" and self.guild_id:
    register_commands(self.bot, self, guild_id=self.guild_id)
  else:
    register_commands(self.bot, self)

async def setup(bot):
  await bot.add_cog(MyCog(bot))
```