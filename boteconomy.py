from discord.ext import commands
import sqlite3
import time

# =========================
# CONFIG
# =========================
TOKEN = "SEU_TOKEN_AQUI"

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# =========================
# BANCO DE DADOS
# =========================
conn = sqlite3.connect("economia.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    user_id INTEGER PRIMARY KEY,
    saldo INTEGER,
    last_daily REAL
)
""")
conn.commit()

# =========================
# FUNÇÕES
# =========================
def get_user(user_id):
    cursor.execute("SELECT * FROM usuarios WHERE user_id = ?", (user_id,))
    user = cursor.fetchone()

    if user is None:
        cursor.execute("INSERT INTO usuarios (user_id, saldo, last_daily) VALUES (?, ?, ?)",
                       (user_id, 0, 0))
        conn.commit()
        return (user_id, 0, 0)

    return user

# =========================
# EVENTO
# =========================
@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")

# =========================
# COMANDOS
# =========================

@bot.command()
async def saldo(ctx):
    user = get_user(ctx.author.id)
    await ctx.send(f"💰 {ctx.author.name}, seu saldo é: {user[1]} moedas")

@bot.command()
async def trabalhar(ctx):
    user = get_user(ctx.author.id)

    ganho = 50

    cursor.execute("UPDATE usuarios SET saldo = saldo + ? WHERE user_id = ?",
                   (ganho, ctx.author.id))
    conn.commit()

    await ctx.send(f"💼 {ctx.author.name} trabalhou e ganhou {ganho} moedas!")

@bot.command()
async def daily(ctx):
    user = get_user(ctx.author.id)
    agora = time.time()

    if agora - user[2] < 86400:
        restante = int(86400 - (agora - user[2]))
        await ctx.send(f"⏳ Espere {restante} segundos para usar o daily novamente.")
        return

    recompensa = 200

    cursor.execute("""
    UPDATE usuarios 
    SET saldo = saldo + ?, last_daily = ?
    WHERE user_id = ?
    """, (recompensa, agora, ctx.author.id))

    conn.commit()

    await ctx.send(f"🎁 {ctx.author.name} recebeu {recompensa} moedas no daily!")

@bot.command()
async def transferir(ctx, membro: discord.Member, valor: int):
    if valor <= 0:
        await ctx.send(" Valor inválido.")
        return

    user = get_user(ctx.author.id)
    alvo = get_user(membro.id)

    if user[1] < valor:
        await ctx.send(" Você não tem saldo suficiente.")
        return

    cursor.execute("UPDATE usuarios SET saldo = saldo - ? WHERE user_id = ?",
                   (valor, ctx.author.id))

    cursor.execute("UPDATE usuarios SET saldo = saldo + ? WHERE user_id = ?",
                   (valor, membro.id))

    conn.commit()

    await ctx.send(f"💸 {ctx.author.name} transferiu {valor} moedas para {membro.name}!")

# =========================
# RODAR BOT
# =========================
bot.run(TOKEN)