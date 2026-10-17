import os
import discord
from discord.ext import commands
from discord import ui
import random
import string

# 1. Configuração do Bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# 2. Modal/Janela para solicitar Whitelist
class WhitelistModal(ui.Modal, title="Solicitar Whitelist"):
    nick = ui.TextInput(label="Teu Nick do Roblox", placeholder="Escreve aqui o teu nick exato...")

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"✅ Whitelist solicitada com sucesso para **{self.nick.value}**!", ephemeral=True)

# 3. Vista com o Botão de Whitelist
class WhitelistView(ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @ui.button(label="Solicitar Whitelist", style=discord.ButtonStyle.green, custom_id="btn_whitelist")
    async def btn_callback(self, interaction: discord.Interaction, button: ui.Button):
        await interaction.response.send_modal(WhitelistModal())

@bot.event
async def on_ready():
    print(f'✅ Bot conectado com sucesso como: {bot.user}')

# 4. Comando para enviar o Painel (!painel)
@bot.command()
async def painel(ctx):
    embed = discord.Embed(
        title="🔒 Sistema de Whitelist",
        description="Clica no botão abaixo para solicitar a tua Whitelist no servidor!",
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed, view=WhitelistView())

# 5. Comando para gerar Keys (!gerarkey <dias>)
@bot.command()
async def gerarkey(ctx, dias: int = 30):
    key = "BL4CK-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=8))
    await ctx.send(f"🔑 **Key Gerada com Sucesso!**\n`{key}`\nValidade: **{dias} dias**")

# 6. Arranque com a variável do Render
token = os.getenv("DISCORD_TOKEN")
if token:
    bot.run(token)
else:
    print("❌ ERRO: Token do Discord não encontrado!")
