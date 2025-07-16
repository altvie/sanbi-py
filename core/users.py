import json
from pathlib import Path

DB_FILE = Path("data/users.json")

def load_data():
  if not DB_FILE.exists():
    DB_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(DB_FILE, "w") as f:
      json.dump({}, f)
  try:
    with open(DB_FILE, "r") as f:
      return json.load(f)
  except json.JSONDecodeError:
    with open(DB_FILE, "w") as f:
      json.dump({}, f)
    return {}

def save_data(data):
  with open(DB_FILE, "w") as f:
    json.dump(data, f, indent=2)

def open_account(user):
  uid = str(user.id)
  data = load_data()

  if uid not in data:
    data[uid] = {
      "name": user.name,
      "level": 1,
      "role": "member",
      "economy": {
        "wallet": 0,
        "bank": 0,
        "last_daily": "",
        "last_work": "",
        "inventory": []
      },
      "stats": {
        "daily_claimed": 0,
        "work_count": 0,
        "gamble_won": 0,
        "gamble_lost": 0
      }
    }
    save_data(data)

  return data
