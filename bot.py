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
REPO_NAME = "BL4CKcomunnity/bot-CERTO"

@bot.event
async def on_ready():
    guild = discord.Object(id=ID_DO_SERVIDOR)
    bot.tree.copy_global_to(guild=guild)
    await bot.tree.sync(guild=guild)
    print(f'✅ Bot conectado e comandos sincronizados no servidor!')

# Função universal para atualizar o whitelist.json e devolver o erro exato
def atualizar_github(tipo, nick_ou_key, extra=None):
    if not GITHUB_TOKEN:
        return "Erro: GITHUB_TOKEN não configurado no Render."
    
    url = f"https://api.github.com/repos/{REPO_NAME}/contents/whitelist.json"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        return f"Erro ao ler do GitHub (Código {r.status_code}): {r.text}"
    
    data = r.json()
    sha = data['sha']
    content_encoded = data['content']
    
    try:
        json_data = json.loads(base64.b64decode(content_encoded).decode('utf-8'))
    except Exception as e:
        return f"Erro ao descodificar o JSON: {str(e)}"
    
    # Decidir o que atualizar com base no comando
    if tipo == "key":
        if "chaves" not in json_data:
            json_data["chaves"] = []
        json_data["chaves"].append({
            "key": nick_ou_key,
            "nick": extra["nick"],
            "dias": extra["dias"]
        })
        msg_commit = f"Adicionada key temporária para {extra['nick']}"
        
    elif tipo == "perm":
        # Vamos aceitar tanto a chave com acentos como sem para evitar falhas
        chave_lista = "usuários_da_lista_de_permisões"
        if chave_lista not in json_data:
            if "usuarios_da_lista_de_permisoes" in json_data:
                chave_lista = "usuarios_da_lista_de_permisoes"
            else:
                json_data[chave_lista] = []
                
        if nick_ou_key not in json_data[chave_lista]:
            json_data[chave_lista].append(nick_ou_key)
        msg_commit = f"Adicionado {nick_ou_key} à whitelist permanente"

    novo_conteudo_str = json.dumps(json_data, indent=4, ensure_ascii=False)
    novo_conteudo_encoded = base64.b64encode(novo_conteudo_str.encode('utf-8')).decode('utf-8')
    
    payload = {
        "message": msg_commit,
        "content": novo_conteudo_encoded,
        "sha": sha
    }
    
    put_r = requests.put(url, headers=headers, json=payload)
    if put_r.status_code in [200, 201]:
        return "SUCESSO"
    else:
        return f"Erro GitHub (Código {put_r.status_code}): {put_r.json().get('message', put_r.text)}"

# 3. Comando /gerarkey
@bot.tree.command(name="gerarkey", description="Gera uma key temporária associada a um nick e dias")
async def gerarkey(interaction: discord.Interaction, nick: str, dias: int):
    key = "BL4CK-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=8))
    resultado = atualizar_github("key", key, {"nick": nick, "dias": dias})
    
    if resultado == "SUCESSO":
        await interaction.response.send_message(
            f"🔑 **Key Gerada e Registada no GitHub!**\n\n👤 **Nick:** `{nick}`\n🎫 **Key:** `{key}`\n⏳ **Validade:** **{dias} dias**", 
            ephemeral=True
        )
    else:
        await interaction.response.send_message(f"❌ `{resultado}`", ephemeral=True)

# 4. Comando /whitelist
@bot.tree.command(name="whitelist", description="Adiciona um utilizador diretamente à whitelist permanente")
async def whitelist(interaction: discord.Interaction, nick: str):
    resultado = atualizar_github("perm", nick)
    
    if resultado == "SUCESSO":
        await interaction.response.send_message(
            f"✅ **Utilizador adicionado à Whitelist Permanente!**\n\n👤 **Nick:** `{nick}`\n♾️ **Acesso:** Infinito", 
            ephemeral=True
        )
    else:
        await interaction.response.send_message(f"❌ `{resultado}`", ephemeral=True)

# 5. Inicialização
if __name__ == "__main__":
    keep_alive()
    token = os.getenv("DISCORD_TOKEN")
    if token:
        bot.run(token)
    else:
        print("❌ ERRO: Token do Discord não encontrado!")
