import discord

def create_embed(
  title=None,
  description=None,
  color=discord.Color.blue(),
  fields=None,
  thumbnail=None,
  image=None,
  footer=None,
  author=None
):
  embed = discord.Embed(
    title=title or "",
    description=description or "",
    color=color
  )
  
  if fields:
    for field in fields:
      name = field[0]
      value = field[1]
      inline = field[2] if len(field) > 2 else False
      embed.add_field(name=name, value=value, inline=inline)
  
  if thumbnail:
    embed.set_thumbnail(url=thumbnail)
  if image:
    embed.set_thumbnail(url=image)
  if footer:
    embed.set_thumbnail(url=footer)
  if author:
    embed.set_thumbnail(url=author)
  
  return embed