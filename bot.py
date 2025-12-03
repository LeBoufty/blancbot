import discord
from discord import app_commands
import json
import random
from PIL import Image, ImageDraw, ImageFont
import io
import textwrap
import os
import requests

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
smashinputs = json.load(open("data/inputs.json", 'r', encoding="utf-8"))['smashInputs']
thumbsupimages = json.load(open("data/thumbsup.json", 'r', encoding="utf-8"))
IA_message = """## Ouah les gars ! c'est de l'IA, un sujet nouveau et high tech !
Pour être **leader** dans le **market** nous avons besoin d'outils **responsive** et **easy access**. Pour cela nous envisageons de remplacer notre algorithme développé par Timmy notre **web interactive developer and js champion** par une solution utilisant l'**IA** avec comme base un **LLM** développé en local. Le tout en méthode **AGILE** et en supervision **latérale circulaire**. Sous la supervision de Jeannine la **HR management administrator** and **happiness manager** qui a vu une vidéo de formation sur l'IA."""
patate_role = 1311765186876805202
# patate_role = 541259130191740938 # Rôle de test
pingroles: dict = json.load(open("data/pingroles.json", "r", encoding="utf-8"))

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
async def jmm(ctx: discord.Interaction, img: discord.Attachment, quality: int = 0, message: str = None, resize: int = 100):
    if quality < 0 or quality > 100:
        await ctx.response.send_message("La qualité doit être entre 0 et 100. (Par défaut : 0)", ephemeral=True)
        return
    if resize < 1 or resize > 100:
        await ctx.response.send_message("Le pourcentage de redimensionnement doit être entre 1 et 100. (Par défaut : 100)", ephemeral=True)
        return
    # Ouverture de l'image
    img_data = await img.read()
    image = Image.open(io.BytesIO(img_data))
    # Ajout du texte
    if message is not None:
        image = add_text_to_image(image, message)
    # Passage en RGB
    image = image.convert('RGB')
    # Redimensionnement
    width, height = image.size
    imgscale = resize / 100
    image = image.resize((int(width * imgscale), int(height * imgscale)))
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
    if patate_role in [role.id for role in cible.roles]:
        await ctx.response.send_message("Cette personne répond déjà.", ephemeral=True)
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
    name="rolelist",
    description="Affiche la liste des mailing lists du serveur"
)
async def rolelist(ctx: discord.Interaction):
    content = ""
    for v in pingroles.values():
        content += f"- **{v['name']}** : `{v['description']}`\n"
    embed = discord.Embed(title="Listes de diffusion", description=content)
    await ctx.response.send_message(embed=embed, ephemeral=True)

@tree.command(
    name="addrole",
    description="Ajoute un rôle aux mailing lists"
)
async def addrole(ctx: discord.Interaction, id: str, description: str):
    try: newid = int(id)
    except Exception:
        await ctx.response.send_message("L'ID fourni est invalide.", ephemeral=True)
        return
    role = discord.utils.get(ctx.guild.roles, id=newid)
    if role is None:
        await ctx.response.send_message("Ce rôle n'existe pas.", ephemeral=True)
        return
    pingroles[role.name] = {
        "name": role.name,
        "id": newid,
        "description": description
    }
    json.dump(pingroles, open("data/pingroles.json", "w", encoding="utf-8"))
    await ctx.response.send_message(f"Le rôle **{role.name}** a été ajouté aux listes de diffusion avec comme description `{description}` ! Utilisez `/subscribe` pour l'ajouter à vos rôles !")

@tree.command(
    name="deleterole",
    description="Supprime un rôle des mailing lists"
)
async def deleterole(ctx: discord.Interaction, name: str):
    try:
        pingroles.pop(name)
        json.dump(pingroles, open("data/pingroles.json", "w", encoding="utf-8"))
        await ctx.response.send_message(f"Le rôle **@{name}** a été supprimé des listes de diffusion, vous ne pouvez plus vous y inscrire via `/subscribe`.")
    except Exception:
        await ctx.response.send_message("Ce rôle n'est pas dans les mailing lists ! Utilise bien le nom du rôle et pas son ID.", ephemeral=True)

@tree.command(
    name="resetsubscribers",
    description="Retire le rôle à tout le monde"
)
async def resetsubscribers(ctx: discord.Interaction, name: str):
    try:
        id = pingroles[name]["id"]
        role = discord.utils.get(ctx.guild.roles, id=id)
        if role is None:
            await ctx.response.send_message("Ce rôle n'existe pas.", ephemeral=True)
            return
        for m in role.members:
            await m.remove_roles(role)
        await ctx.response.send_message(f"Les abonnés à **@{name}** ont été remis à zéro, vous pouvez vous y réinscrire via `/subscribe` !")
    except Exception:
        await ctx.response.send_message("Ce rôle n'est pas dans les mailing lists ! Utilise bien le nom du rôle et pas son ID.", ephemeral=True)

@tree.command(
    name="subscribe",
    description="Abonne-toi à une liste de diffusion"
)
async def subscribe(ctx: discord.Interaction, name: str):
    try:
        id = pingroles[name]["id"]
        role = discord.utils.get(ctx.guild.roles, id=id)
        if role is None:
            await ctx.response.send_message("Ce rôle n'existe pas.", ephemeral=True)
            return
        await ctx.user.add_roles(role)
        await ctx.response.send_message(f"Tu es maintenant abonné à **{name}** !", ephemeral=True)
    except Exception:
        await ctx.response.send_message("Ce rôle n'est pas dans les mailing lists ! Utilise bien le nom du rôle et pas son ID.", ephemeral=True)

@tree.command(
    name="unsubscribe",
    description="Désabonne-toi d'une liste de diffusion"
)
async def unsubscribe(ctx: discord.Interaction, name: str):
    try:
        id = pingroles[name]["id"]
        role = discord.utils.get(ctx.guild.roles, id=id)
        if role is None:
            await ctx.response.send_message("Ce rôle n'existe pas.", ephemeral=True)
            return
        await ctx.user.remove_roles(role)
        await ctx.response.send_message(f"Tu es maintenant désabonné de **{name}** !", ephemeral=True)
    except Exception:
        await ctx.response.send_message("Ce rôle n'est pas dans les mailing lists ! Utilise bien le nom du rôle et pas son ID.", ephemeral=True)

@tree.command(
        name="ia",
        description="Décrit un projet innovant et unique"
)
async def IA(ctx: discord.Interaction):
    await ctx.response.send_message(IA_message, ephemeral=False)

def archipelago_online():
    response = requests.get("http://archipelago.mafreidyne.motorcycles").status_code
    return response == 400

@tree.command(
    name="archipelago",
    description="Affiche l'état actuel du serveur Archipelago"
)
async def archipelago(ctx: discord.Interaction):
    yamls = ["`" + i + "`" for i in os.listdir("Players")]
    title = "🟡 État du serveur inconnu."
    if archipelago_online():
        title = "🟢 Le serveur est en ligne !\n\n"
    else:
        title = "🔴 Le serveur est hors ligne.\n\n"
    content = f"YAML trouvés : {', '.join(yamls)}"
    embed = discord.Embed(title=title, description=content)
    await ctx.response.send_message(embed=embed, ephemeral=True)

@tree.command(
    name="uploadyaml",
    description="Permet d'envoyer un yaml au serveur"
)
async def uploadyaml(ctx: discord.Interaction, yaml: discord.Attachment):
    if not (yaml.filename.endswith(".yml") or yaml.filename.endswith(".yaml")):
        await ctx.response.send_message("Ce fichier n'est pas un YAML.", ephemeral=True)
        return
    open(f"Players/{yaml.filename}", "wb").write(await yaml.read())
    await ctx.response.send_message("Fichier envoyé !", ephemeral=True)

@tree.command(
    name="deleteyaml",
    description="Supprime un yaml du serveur"
)
async def deleteyaml(ctx: discord.Interaction, yaml: str):
    try:
        os.remove(f"Players/{yaml}")
        await ctx.response.send_message("Fichier supprimé !", ephemeral=True)
    except:
        await ctx.response.send_message("Une erreur s'est produite.", ephemeral=True)

@client.event
async def on_ready():
    await tree.sync()
    print(f"We have logged in as {client.user}")

if __name__ == "__main__":
    client.run(open("BOT_TOKEN", 'r').read())
