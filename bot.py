import discord
from discord import app_commands

client = discord.Client(intents=discord.Intents.default())

@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")

if __name__ == "__main__":
    client.run(open("BOT_TOKEN", 'r').read())