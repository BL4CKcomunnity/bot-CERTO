import os
import random
import string
import threading
from flask import Flask
import discord
from discord.ext import commands
from discord import ui

# 1. Servidor Web (Flask) para o Render
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

# 2. Configuração do Bot
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# ID do teu servidor configurado
ID_DO_SERVIDOR = 1462932885924347916

@bot.event
async def on_ready():
    guild = discord.Object(id=ID_DO_SERVIDOR)
    # Sincronização direta para o teu servidor (aparece na hora)
    bot.tree.copy_global_to(guild=guild)
    await bot.tree.sync(guild=guild)
    print(f'✅ Bot conectado e comandos sincronizados no servidor!')

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

# 5. Slash Commands
@bot.tree.command(name="painel", description="Envia o painel de Whitelist")
async def painel(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🔒 Sistema de Whitelist",
        description="Clica no botão abaixo para solicitar a tua Whitelist no servidor!",
        color=discord.Color.blue()
    )
    await interaction.response.send_message(embed=embed, view=WhitelistView())

@bot.tree.command(name="gerarkey", description="Gera uma key de Whitelist")
async def gerarkey(interaction: discord.Interaction, dias: int = 30):
    key = "BL4CK-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=8))
    await interaction.response.send_message(f"🔑 **Key Gerada com Sucesso!**\n`{key}`\nValidade: **{dias} dias**", ephemeral=True)

# 6. Inicialização
if __name__ == "__main__":
    keep_alive()
    token = os.getenv("DISCORD_TOKEN")
    if token:
        bot.run(token)
    else:
        print("❌ ERRO: Token do Discord não encontrado!")
