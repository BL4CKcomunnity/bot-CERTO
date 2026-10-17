import os
import discord
from discord.ext import commands
from keep_alive import manter_vivo

# 1. Configuração do Flask para manter o bot online
manter_vivo()

# 2. Configuração do Bot do Discord
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'✅ Bot conectado com sucesso como: {bot.user}')

# (Aqui podes adicionar os teus comandos de whitelist e painel)

# 3. Arranque do Bot com a variável de ambiente segura
token = os.getenv("DISCORD_TOKEN")
if token:
    bot.run(token)
else:
    print("❌ ERRO: Token do Discord não encontrado nas Variáveis do Render!")
