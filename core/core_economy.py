import os, json
from pathlib import Path

DATA_FILE = Path('data/economy.json')

def load_data():
  if not DATA_FILE.exists():
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(DATA_FILE, "w") as f:
      json.dump({}, f)

  try:
    with open(DATA_FILE, "r") as f:
      return json.load(f)
  except json.JSONDecodeError:
    with open(DATA_FILE, "w") as f:
      json.dump({}, f)
    return {}

def save_data(data):
  with open(DATA_FILE, "w") as f:
    json.dump(data, f, indent=2)

def open_account(user_id):
  data = load_data()
  uid = str(user_id)
  if uid not in data:
    data[uid] = {
      "wallet": 0,
      "bank": 0,
      "last_daily": "",
      "inventory": []
    }
    save_data(data)
  return data

def get_balance(user_id):
  data = load_data()
  uid = str(user_id)
  return data.get(uid, {
    "wallet": 0,
    "bank": 0,
    "last_daily": "",
    "inventory": []
  })

def update_balance(user_id, amount, target="wallet"):
  data = load_data()
  uid = str(user_id)
  if uid not in data:
    open_account(user_id)
    data = load_data()
  data[uid][target] += amount
  save_data(data)
  return data[uid][target]