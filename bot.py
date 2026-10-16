import os
import discord
from discord.ext import commands
from flask import Flask
from threading import Thread

# 1. Configuração do Servidor Web (Flask)
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

# Inicia o Flask em segundo plano para não bloquear o bot
keep_alive()

# 2. Configuração do Bot do Discord
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'✅ Bot conectado com sucesso como: {bot.user}')

# (Aqui podes ter os teus comandos de whitelist)

# 3. Arranque do Bot
token = os.getenv("DISCORD_TOKEN")
if token:
    bot.run(token)
else:
    print("❌ ERRO: Token do Discord não encontrado!")
