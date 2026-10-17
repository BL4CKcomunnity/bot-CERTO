import os
import random
import string
import threading
import base64
import json
import requests
from flask import Flask
import discord
from discord.ext import commands

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

ID_DO_SERVIDOR = 1462932885924347916
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO_NAME = "BL4CKcomunnity/bot-CERTO" # Nome exato com dois 'n' conforme o teu link

@bot.event
async def on_ready():
    guild = discord.Object(id=ID_DO_SERVIDOR)
    bot.tree.copy_global_to(guild=guild)
    await bot.tree.sync(guild=guild)
    print(f'✅ Bot conectado e comandos sincronizados no servidor!')

# Função para atualizar o whitelist.json no GitHub
def adicionar_key_github(nova_key, nick_roblox, dias):
    if not GITHUB_TOKEN:
        print("❌ GITHUB_TOKEN não configurado no Render!")
        return "token_em_falta"
    
    url = f"https://api.github.com/repos/{REPO_NAME}/contents/whitelist.json"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    # Obter o ficheiro atual do GitHub
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        print(f"❌ Erro ao procurar whitelist.json: {r.status_code} - {r.text}")
        return "erro_github"
    
    data = r.json()
    sha = data['sha']
    content_encoded = data['content']
    
    # Descodificar JSON
    decoded_bytes = base64.b64decode(content_encoded)
    json_data = json.loads(decoded_bytes.decode('utf-8'))
    
    if "chaves" not in json_data:
        json_data["chaves"] = []
        
    # Adicionar a nova key
    json_data["chaves"].append({
        "key": nova_key,
        "nick": nick_roblox,
        "dias": dias
    })
    
    # Codificar de volta
    novo_conteudo_str = json.dumps(json_data, indent=4)
    novo_conteudo_encoded = base64.b64encode(novo_conteudo_str.encode('utf-8')).decode('utf-8')
    
    payload = {
        "message": f"Adicionada key para {nick_roblox} ({dias} dias) via bot",
        "content": novo_conteudo_encoded,
        "sha": sha
    }
    
    put_r = requests.put(url, headers=headers, json=payload)
    if put_r.status_code in [200, 201]:
        return "sucesso"
    else:
        print(f"❌ Erro no commit do GitHub: {put_r.status_code} - {put_r.text}")
        return "erro_github"

# 3. Comando /gerarkey com campos claros (Nick e Dias)
@bot.tree.command(name="gerarkey", description="Gera uma key temporária associada a um nick e dias")
async def gerarkey(interaction: discord.Interaction, nick: str, dias: int):
    key = "BL4CK-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=8))
    
    resultado = adicionar_key_github(key, nick, dias)
    
    if resultado == "sucesso":
        await interaction.response.send_message(
            f"🔑 **Key Gerada e Registada no GitHub com Sucesso!**\n\n"
            f"👤 **Nick Roblox:** `{nick}`\n"
            f"🎫 **Key:** `{key}`\n"
            f"⏳ **Validade:** **{dias} dias**", 
            ephemeral=True
        )
    elif resultado == "token_em_falta":
        await interaction.response.send_message(
            "❌ Erro: A variável `GITHUB_TOKEN` não está configurada no Render.", 
            ephemeral=True
        )
    else:
        await interaction.response.send_message(
            "❌ Erro ao atualizar o GitHub. Confere se o Token tem permissões `repo`.", 
            ephemeral=True
        )

# 4. Inicialização
if __name__ == "__main__":
    keep_alive()
    token = os.getenv("DISCORD_TOKEN")
    if token:
        bot.run(token)
    else:
        print("❌ ERRO: Token do Discord não encontrado!")
