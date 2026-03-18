import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Lunaris despertou como {bot.user}")

@bot.event
async def on_member_join(member):

    channel = discord.utils.get(member.guild.text_channels, name="boas-vindas")

    if channel:
        await channel.send(
f"""
**Bem-vindo à Cohors Ignis Lunaris, {member.mention}.**

Aqui você estudará os mistérios da **Alquimia Planetária**.

Para iniciar sua jornada, digite:

**!iniciar**
"""
        )

@bot.command()
async def iniciar(ctx):

    await ctx.send(
"""
⚗️ **Ritual de Iniciação**

Escolha o planeta que guiará sua jornada.

Digite um dos comandos:

!sol
!lua
!mercurio
!venus
!marte
!jupiter
!saturno
"""
)

async def dar_cargo(ctx, nome_cargo):

    role = discord.utils.get(ctx.guild.roles, name=nome_cargo)

    if role:
        await ctx.author.add_roles(role)
        await ctx.send(f"{ctx.author.mention} Tu tens **{nome_cargo}** como estrada.")
    else:
        await ctx.send("Cargo não encontrado no servidor.")

@bot.command()
async def sol(ctx):
    await dar_cargo(ctx, "Sol")

@bot.command()
async def lua(ctx):
    await dar_cargo(ctx, "Lua")

@bot.command()
async def mercurio(ctx):
    await dar_cargo(ctx, "Mercúrio")

@bot.command()
async def venus(ctx):
    await dar_cargo(ctx, "Vênus")

@bot.command()
async def marte(ctx):
    await dar_cargo(ctx, "Marte")

@bot.command()
async def jupiter(ctx):
    await dar_cargo(ctx, "Júpiter")

@bot.command()
async def saturno(ctx):
    await dar_cargo(ctx, "Saturno")

bot.run("tokendalunaris")
