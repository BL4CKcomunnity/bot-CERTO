import os
import random
import string
import threading
from flask import Flask
import discord
from discord.ext import commands
from discord import ui

# 1. Servidor Web (Flask) para manter o Render ativo
app = Flask('')

@app.route('/')
def home():
    return "Bot BL4CK está Online!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = threading.Thread(target=run_flask)
    t.daemon = True
    t.start()

# 2. Configuração do Bot do Discord
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# 3. Modal para solicitar Whitelist
class WhitelistModal(ui.Modal, title="Solicitar Whitelist"):
    nick = ui.TextInput(label="Teu Nick do Roblox", placeholder="Escreve aqui o teu nick exato...")

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"✅ Whitelist solicitada com sucesso para **{self.nick.value}**!", ephemeral=True)

# 4. Vista com o Botão
class WhitelistView(ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @ui.button(label="Solicitar Whitelist", style=discord.ButtonStyle.green, custom_id="btn_whitelist")
    async def btn_callback(self, interaction: discord.Interaction, button: ui.Button):
        await interaction.response.send_modal(WhitelistModal())

@bot.event
async def on_ready():
    print(f'✅ Bot conectado com sucesso como: {bot.user}')

# 5. Comandos
@bot.command()
async def painel(ctx):
    embed = discord.Embed(
        title="🔒 Sistema de Whitelist",
        description="Clica no botão abaixo para solicitar a tua Whitelist no servidor!",
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed, view=WhitelistView())

@bot.command()
async def gerarkey(ctx, dias: int = 30):
    key = "BL4CK-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=8))
    await ctx.send(f"🔑 **Key Gerada com Sucesso!**\n`{key}`\nValidade: **{dias} dias**")

# 6. Inicialização
if __name__ == "__main__":
    keep_alive()  # Inicia o Flask em segundo plano
    token = os.getenv("DISCORD_TOKEN")
    if token:
        bot.run(token)
    else:
        print("❌ ERRO: Token do Discord não encontrado!")
