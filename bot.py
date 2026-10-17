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
REPO_NAME = "BL4CKcomunnity/bot-CERTO" # Teu repositório

@bot.event
async def on_ready():
    guild = discord.Object(id=ID_DO_SERVIDOR)
    bot.tree.copy_global_to(guild=guild)
    await bot.tree.sync(guild=guild)
    print(f'✅ Bot conectado e comandos sincronizados no servidor!')

# Função para atualizar o whitelist.json no GitHub
def adicionar_key_github(nova_key, dias):
    if not GITHUB_TOKEN:
        print("❌ GITHUB_TOKEN não configurado!")
        return False
    
    url = f"https://api.github.com/repos/{REPO_NAME}/contents/whitelist.json"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    # Obter o ficheiro atual
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        print(f"❌ Erro ao procurar whitelist.json: {r.status_code}")
        return False
    
    data = r.json()
    sha = data['sha']
    content_encoded = data['content']
    
    # Descodificar JSON
    decoded_bytes = base64.b64decode(content_encoded)
    json_data = json.loads(decoded_bytes.decode('utf-8'))
    
    if "chaves" not in json_data:
        json_data["chaves"] = []
        
    json_data["chaves"].append({
        "key": nova_key,
        "dias": dias
    })
    
    # Codificar de volta
    novo_conteudo_str = json.dumps(json_data, indent=4)
    novo_conteudo_encoded = base64.b64encode(novo_conteudo_str.encode('utf-8')).decode('utf-8')
    
    payload = {
        "message": f"Adicionada nova key {nova_key} via bot",
        "content": novo_conteudo_encoded,
        "sha": sha
    }
    
    put_r = requests.put(url, headers=headers, json=payload)
    return put_r.status_code in [200, 201]

# 3. Slash Command para criar Keys
@bot.tree.command(name="gerarkey", description="Gera uma key temporária e guarda no GitHub")
async def gerarkey(interaction: discord.Interaction, dias: int = 30):
    key = "BL4CK-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=8))
    
    sucesso = adicionar_key_github(key, dias)
    
    if sucesso:
        await interaction.response.send_message(
            f"🔑 **Key Gerada e Registada no GitHub com Sucesso!**\n"
            f"Código: `{key}`\n"
            f"Validade: **{dias} dias**", 
            ephemeral=True
        )
    else:
        await interaction.response.send_message(
            "❌ Erro ao atualizar o `whitelist.json` no GitHub. Verifica a variável `GITHUB_TOKEN` no Render.", 
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
