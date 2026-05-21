import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Chargement des variables d'environnement (.env)
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN") # ou "TOKEN" selon ce que tu as écrit dans ton .env

# Configuration des intentions (Intents) de Discord
intents = discord.Intents.default()
intents.message_content = True  # Obligatoire pour lire les messages

# Création de l'instance du Bot
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"=== Bot connecté avec succès ===")
    print(f"Nom : {bot.user.name}")
    print(f"ID : {bot.user.id}")
    print(f"================================")
    
    # Chargement automatique des extensions (cogs)
    extensions = ["cogs.history", "cogs.monitor"]
    for ext in extensions:
        try:
            await bot.load_extension(ext)
            print(f"Extension '{ext}' chargée avec succès.")
        except Exception as e:
            print(f"Impossible de charger l'extension {ext} : {e}")

# Lancement du bot
if __name__ == "__main__":
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("Erreur : Aucun token trouvé. Vérifie ton fichier .env ou tes variables d'environnement.")