import os
from flask import Flask
from threading import Thread
import discord
from discord.ext import commands

app = Flask('')

@app.route('/')
def home():
    return "Bot Online 24/7!"

def run():
    # Usa a porta atribuída pelo Render ou a 8080 por defeito
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

keep_alive()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Bot ligado com sucesso como: {bot.user}')

# (Cola aqui o resto dos teus comandos da whitelist)

bot.run(os.getenv("DISCORD_TOKEN"))
