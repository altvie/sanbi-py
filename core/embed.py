import discord

def create_embed(
  title=None,
  description=None,
  color=discord.Color.blue(),
  fields=None,
  thumbnail=None,
  image=None,
  footer=None,
  author=None,
  author_icon=None,
  footer_icon=None
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
    embed.set_image(url=image)
  if footer:
    embed.set_footer(url=footer, icon_url=footer_icon)
  if author:
    embed.set_author(url=author, author_icon=author_icon)
  
  return embed