import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
<<<<<<< HEAD

# On essaie d'importer keep_alive, si le fichier n'existe pas (hors Replit), on l'ignore
try:
    from keep_alive import keep_alive
    HAS_KEEP_ALIVE = True
except ImportError:
    HAS_KEEP_ALIVE = False
=======
from keep_alive import keep_alive
>>>>>>> 46f4bcfd25f9430433d14b94d835a8a2b80f10bc

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

class MonBot(commands.Bot):
    async def setup_hook(self):
<<<<<<< HEAD
        # Chargement des extensions (tes fichiers dans le dossier cogs)
        for extension in ['commandes_slash', 'online', 'history', 'monitor']:
            try:
                await self.load_extension(f'cogs.{extension}')
                print(f"Extension {extension} chargée avec succès !")
            except Exception as e:
                print(f"Impossible de charger l'extension {extension} : {e}")

        # Synchronisation globale des commandes slash (visible sur tous tes serveurs)
        await self.tree.sync()
        print("Commandes slash synchronisées avec succès !")

intents = discord.Intents.all()
# On utilise un prefixe optionnel car tu fonctionnes principalement en commandes slash (/)
bot = MonBot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Connecté en tant que {bot.user.name} ({bot.user.id})")
    print("Le bot est prêt et en ligne !")

@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return
    # Petite réponse automatique sympa
    if message.content.lower().startswith("bonjour") or message.content.lower().startswith("salut"):
        await message.channel.send(f"Salut {message.author.mention} ! 👋")

# Lance le keep_alive uniquement si le fichier est présent
if HAS_KEEP_ALIVE:
    keep_alive()

# Lancement du bot
=======
        # Chargement des extensions
        for extension in ['commandes_slash', 'online', 'history', 'monitor']:
            await self.load_extension(f'cogs.{extension}')

        # Synchronisation des commandes slash sur tous les guildes du bot (globale)
        await self.tree.sync()


intents = discord.Intents.all()
bot = MonBot(command_prefix="!", intents=intents)

@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return
    if message.content.lower().startswith("bonjour") or message.content.lower().startswith("salut"):
        await message.channel.send("salut")


keep_alive()
>>>>>>> 46f4bcfd25f9430433d14b94d835a8a2b80f10bc
bot.run(token=token)