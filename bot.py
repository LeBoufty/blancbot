import discord
from discord import app_commands
import json
import random
import os
import requests
from PIL import Image, ImageDraw, ImageFont
import io
import textwrap

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
smashinputs = json.load(open("data/inputs.json", 'r', encoding="utf-8"))['smashInputs']
thumbsupimages = json.load(open("data/thumbsup.json", 'r', encoding="utf-8"))
IA_message = """## Ouah les gars ! c'est de l'IA, un sujet nouveau et high tech !
Pour être **leader** dans le **market** nous avons besoin d'outils **responsive** et **easy access**. Pour cela nous envisageons de remplacer notre algorithme développé par Timmy notre **web interactive developer and js champion** par une solution utilisant l'**IA** avec comme base un **LLM** développé en local. Le tout en méthode **AGILE** et en supervision **latérale circulaire**. Sous la supervision de Jeannine la **HR management administrator** and **happiness manager** qui a vu une vidéo de formation sur l'IA."""
patate_role = 1311765186876805202
#patate_role = 541259130191740938 # Rôle de test

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

def add_text_to_image(img, message, font_path="data/Upright.ttf"):
    lines = textwrap.wrap(message, width=32)
    draw = ImageDraw.Draw(img)
    imgwidth, imgheight = img.size
    fontsize = get_font_size(min(imgwidth, imgheight))
    font = ImageFont.truetype(font_path, fontsize)
    textwidth = max(font.getmask(line).size[0] for line in lines)
    textheight = font.getmask(lines[0]).size[1]
    y_text = (imgheight - textheight) // 2 - textheight * len(lines) // 2
    for line in lines:
        draw.text(((imgwidth - textwidth) // 2, y_text),
                  line, (255, 255, 255), font=font,
                  stroke_width=fontsize // 20, stroke_fill=(0, 0, 0))
        y_text += textheight
    return img

@tree.command(
        name="thumbsup",
        description="👍👍"
)
async def thumbsup(ctx: discord.Interaction, message: str = None):
    imgno = random.randint(0, len(thumbsupimages) - 1)
    image_path = f"thumbsup/{imgno}.png"
    if message is None:
        with open(image_path, 'rb') as f:
            await ctx.response.send_message(file=discord.File(f), ephemeral=False)
    else:
        img = Image.open(image_path)
        img = add_text_to_image(img, message)
        with io.BytesIO() as image_binary:
            img.save(image_binary, 'PNG')
            image_binary.seek(0)
            await ctx.response.send_message(file=discord.File(fp=image_binary,
                                                              filename='thumbsup.png'),
                                            ephemeral=False)

@tree.command(
        name="jmm",
        description="Envie d'me compresser l'jpeg"
)
async def jmm(ctx: discord.Interaction, img: discord.Attachment, quality: int = 0, message: str = None):
    # Ouverture de l'image
    img_data = await img.read()
    image = Image.open(io.BytesIO(img_data))
    # Ajout du texte
    if message is not None:
        image = add_text_to_image(image, message)
    # Passage en RGB
    image = image.convert('RGB')
    # Compression
    with io.BytesIO() as image_binary:
        image.save(image_binary, 'JPEG', quality=quality)
        image_binary.seek(0)
        await ctx.response.send_message(file=discord.File(fp=image_binary,
                                                          filename='compressed.jpg'),
                                        ephemeral=False)

@tree.command(
        name="patatechaude",
        description="Tu connais le jeu de la patate chaude ?"
)
async def patatechaude(ctx: discord.Interaction, cible: discord.User):
    if cible.id == ctx.user.id:
        await ctx.response.send_message("Tu connais le jeu de la patate chaude ? C'est PAS toi qui réponds !", ephemeral=True)
        return
    if patate_role not in [role.id for role in ctx.user.roles]:
        await ctx.response.send_message("Tu n'as pas le rôle patate chaude.", ephemeral=True)
        return
    if cible.bot:
        await ctx.response.send_message("Les bots ne connaissent pas le jeu de la patate chaude ET ne peuvent pas répondre.", ephemeral=True)
        return
    role = discord.utils.get(ctx.guild.roles, id=patate_role)
    try:
        await cible.add_roles(role)
        await ctx.user.remove_roles(role)
    except discord.errors.Forbidden:
        await ctx.response.send_message("Je n'ai pas la permission de donner le rôle.", ephemeral=True)
        return
    await ctx.response.send_message(f"Tu connais le jeu de la patate chaude ? C'est {cible.mention} qui répond.", ephemeral=True)

@tree.command(
        name="ia",
        description="Décrit un projet innovant et unique"
)
async def IA(ctx: discord.Interaction):
    await ctx.response.send_message(IA_message, ephemeral=False)

@client.event
async def on_ready():
    await tree.sync()
    print(f"We have logged in as {client.user}")

if __name__ == "__main__":
    client.run(open("BOT_TOKEN", 'r').read())