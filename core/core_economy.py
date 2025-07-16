from core.user import load_data, save_data

def get_wallet(user_id):
  return load_data()[str(user_id)]["economy"]["wallet"]

def update_wallet(user_id, amount):
  data = load_data()
  uid = str(user_id)
  data[uid]["economy"]["wallet"] += amount
  save_data(data)
  return data[uid]["economy"]["wallet"]

def get_bank(user_id):
  return load_data()[str(user_id)]["economy"]["bank"]

def update_bank(user_id, amount):
  data = load_data()
  uid = str(user_id)
  data[uid]["economy"]["bank"] += amount
  save_data(data)
  return data[uid]["economy"]["bank"]

def update_stat(user_id, stat_name, amount=1):
  data = load_data()
  uid = str(user_id)
  if stat_name in data[uid]["stats"]:
    data[uid]["stats"][stat_name] += amount
  else:
    data[uid]["stats"][stat_name] = amount
  save_data(data)

def get_stat(user_id, stat_name):
  return load_data()[str(user_id)]["stats"].get(stat_name, 0)