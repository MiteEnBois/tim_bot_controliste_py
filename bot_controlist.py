# bot.py
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv
import json
import datetime

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

with open('roles.json') as json_file:
    global roles_list
    roles_list = json.load(json_file)["role_list"]


def check_roles(member):
    i = 0
    for r in member.roles:
        if r.name in roles_list:
            i += 1
    return i


def get_rol(member):
    for r in member.roles:
        if r.name in roles_list:
            return r
    return None


@bot.command(name='list')
async def list_role(ctx):
    roles = ctx.guild.roles
    txt = "__**Liste des equipes**__\n"
    for r in roles:
        if r.name in roles_list:
            txt += "**"+r.name + "** : "+str(len(r.members)) + "\n"

    await ctx.send(txt)
    print("list asked at "+ctx.message.created_at.ctime()+" by "+str(ctx.message.author))


@bot.command(name='rejoin')
async def rejoin(ctx, invite: discord.Member):
    auth = ctx.author
    if check_roles(auth) != 1:
        await ctx.send(auth.name+" n'a pas de roles, ou en a meme trop. C'est zarb")
        return
    if check_roles(invite) != 0:
        await ctx.send(invite.name+" a déjà un role. Impossible de l'inviter")
        return
    r = get_rol(auth)
    await invite.add_roles(r)
    print(str(auth)+" a invité "+str(invite)+" à rejoindre la "+r.name+" à "+ctx.message.created_at.ctime())
    await ctx.send(auth.name+" a invité "+invite.name+" à rejoindre la "+r.name+"\n")


@bot.command(name='degage')
async def degage(ctx, invite: discord.Member):
    auth = ctx.author
    if check_roles(auth) != 1:
        await ctx.send(auth.name+" n'a pas de roles, ou en a meme trop. C'est zarb")
        return
    if check_roles(invite) != 1:
        await ctx.send(invite.name+" n'a pas de roles, ou en a meme trop. C'est zarb")
        return
    ra = get_rol(auth)
    ri = get_rol(invite)
    if ri != ra:
        await ctx.send("les roles ne sont pas identiques. Degage annulé")
        return
    await invite.remove_roles(ri)
    print(str(auth)+" a dégagé "+str(invite)+" de "+ri.name+" à "+ctx.message.created_at.ctime())
    await ctx.send(auth.name+" a dégagé "+invite.name+" de "+ri.name+"\n")


@bot.event
async def on_ready():
    print('bot started')


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')

bot.run(TOKEN)
