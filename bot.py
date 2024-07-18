import discord
from discord import app_commands
import json
import random

client = discord.Client(intents=discord.Intents.default())
tree = app_commands.CommandTree(client)
smashinputs = json.load(open("data/inputs.json", 'r', encoding="utf-8"))['smashInputs']

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

@client.event
async def on_ready():
    await tree.sync()
    print(f"We have logged in as {client.user}")

if __name__ == "__main__":
    client.run(open("BOT_TOKEN", 'r').read())