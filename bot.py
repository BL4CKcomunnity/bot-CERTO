import os
import discord
from discord.ext import commands
from flask import Flask
from threading import Thread

# 1. Configurar o Flask para o Render detetar a porta aberta
app = Flask('')

@app.route('/')
def home():
    return "Bot Online 24/7!"

def run():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# Iniciar o servidor web primeiro
keep_alive()

# 2. Configurar o Bot do Discord
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Bot ligado com sucesso como: {bot.user}')

# (Cola aqui os teus comandos de whitelist do Roblox)

# 3. Arrancar o bot com a variável de ambiente segura
bot.run(os.getenv("DISCORD_TOKEN"))
