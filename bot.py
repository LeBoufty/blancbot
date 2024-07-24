import discord
from discord import app_commands
import json
import random
import os
import requests

client = discord.Client(intents=discord.Intents.default())
tree = app_commands.CommandTree(client)
smashinputs = json.load(open("data/inputs.json", 'r', encoding="utf-8"))['smashInputs']
thumbsupimages = json.load(open("data/thumbsup.json", 'r', encoding="utf-8"))
valentin_messages = open("valentin/bawardage.txt", 'r', encoding="utf-8").readlines()

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

@tree.command(
        name="thumbsup",
        description="👍👍"
)
async def thumbsup(ctx: discord.Interaction):
    imgno = random.randint(0, len(thumbsupimages) - 1)
    with open(f"thumbsup/{imgno}.png", 'rb') as f:
        await ctx.response.send_message(file=discord.File(f), ephemeral=False)

# @tree.command(
#         name="scrapevalentin",
#         description="Scrape les messages de Valentin"
# )
# async def scrapevalentin(ctx: discord.Interaction):
#     await ctx.response.defer(ephemeral=True)
#     channel = ctx.channel
#     messages = channel.history(limit=20000)
#     VALENTIN_ID = int(open("VALENTIN_ID", 'r').read())
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

if __name__ == "__main__":
    try:
        os.mkdir("thumbsup")
        for i, url in enumerate(thumbsupimages):
            with open(f"thumbsup/{i}.png", 'wb') as f:
                f.write(requests.get(url).content)
    except:
        pass
    client.run(open("BOT_TOKEN", 'r').read())