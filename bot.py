import discord
from discord import app_commands
import json
import random
import os
import requests
from PIL import Image, ImageDraw, ImageFont
import io
import textwrap
from pythonWordArt import pyWordArt

client = discord.Client(intents=discord.Intents.default())
tree = app_commands.CommandTree(client)
smashinputs = json.load(open("data/inputs.json", 'r', encoding="utf-8"))['smashInputs']
thumbsupimages = json.load(open("data/thumbsup.json", 'r', encoding="utf-8"))
valentin_messages = open("valentin/bawardage.txt", 'r', encoding="utf-8").readlines()
wordart_styles = ["aqua", "chrome", "gray-block", "green-marble", "horizon", "marble-slab", "purple", "rainbow", "sunset", "superhero", "tilt"]
VALENTIN_ID = int(open("VALENTIN_ID", 'r').read())

@tree.command(
        name="randomizeinputs",
        description="Donne une config aléatoire pour Smash"
)
async def randomizeinputs(ctx: discord.Interaction):
    message = "Voici ce avec quoi tu vas devoir jouer :\n"
    for input in smashinputs:
        message += f"* **{input.replace('_', ' ')} :** {random.choice(smashinputs[input])}\n"
    await ctx.response.send_message(message, ephemeral=False)

@tree.command(
        name="premierministre",
        description="Bonjour à tous je suis le premier ministre."
)
async def premierministre(ctx: discord.Interaction):
    await ctx.response.send_message("Bonjour à tous je suis le premier ministre.", ephemeral=False)

def get_font_size(imgscale):
    return max(24, int(imgscale / 10))

@tree.command(
        name="thumbsup",
        description="👍👍"
)
async def thumbsup(ctx: discord.Interaction, message: str = None):
    imgno = random.randint(0, len(thumbsupimages) - 1)
    if message is None:
        with open(f"thumbsup/{imgno}.png", 'rb') as f:
            await ctx.response.send_message(file=discord.File(f), ephemeral=False)
    else:
        lines = textwrap.wrap(message, width=32)
        img = Image.open(f"thumbsup/{imgno}.png")
        draw = ImageDraw.Draw(img)
        imgwidth, imgheight = img.size
        fontsize = get_font_size(min(imgwidth, imgheight))
        font = ImageFont.truetype("data/Upright.ttf", fontsize)
        textwidth = max(font.getmask(line).size[0] for line in lines)
        textheight = font.getmask(lines[0]).size[1]
        y_text = (imgheight - textheight) // 2 - textheight * len(lines) // 2
        for line in lines:
            draw.text(((imgwidth - textwidth) // 2, y_text),
                      line, (255,255,255), font=font,
                      stroke_width=fontsize//20, stroke_fill=(0, 0, 0))
            y_text += textheight
        with io.BytesIO() as image_binary:
                    img.save(image_binary, 'PNG')
                    image_binary.seek(0)
                    await ctx.response.send_message(file=discord.File(fp=image_binary,
                                                                      filename='thumbsup.png'),
                                                    ephemeral=False)

# @tree.command(
#         name="scrapevalentin",
#         description="Scrape les messages de Valentin"
# )
# async def scrapevalentin(ctx: discord.Interaction):
#     await ctx.response.defer(ephemeral=True)
#     channel = ctx.channel
#     messages = channel.history(limit=20000)
#     messages = [message.content async for message in messages if message.author.id == VALENTIN_ID]
#     with open(f"valentin/{channel.name}.txt", 'w', encoding="utf-8") as f:
#         for m in messages:
#             try: f.write(m + "\n")
#             except: pass
#     await ctx.followup.send("Messages scrapés", ephemeral=True)

@tree.command(
        name="valentin",
        description="Dispense de la sagesse"
)
async def valentin(ctx: discord.Interaction):
    await ctx.response.send_message(random.choice(valentin_messages), ephemeral=False)

@client.event
async def on_ready():
    await tree.sync()
    print(f"We have logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.auhtor.id == VALENTIN_ID and message.content != "":
        open("valentin/bawardage.txt", 'a', encoding="utf-8").write(message.content + "\n")

if __name__ == "__main__":
    try:
        os.mkdir("thumbsup")
        for i, url in enumerate(thumbsupimages):
            with open(f"thumbsup/{i}.png", 'wb') as f:
                f.write(requests.get(url).content)
    except:
        pass
    client.run(open("BOT_TOKEN", 'r').read())