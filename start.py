import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from keep_alive import keep_alive

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

class MonBot(commands.Bot):
    async def setup_hook(self):
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
bot.run(token=token)