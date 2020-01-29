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


def num(rol):
    return len(rol.members)


@bot.command(name='list', help='Répond avec la liste des teams si passé sans argument, Répond avec la liste des membres d\'une team passée en argument')
async def list_role(ctx, *arr):
    l = len(arr)
    if l == 0:
        roles = ctx.guild.roles
        roles.sort(key=num, reverse=True)
        txt = "__**Liste des equipes**__\n"
        i = 0
        for r in roles:
            if r.name in roles_list:
                if i == 0:
                    txt += ":trophy: "
                txt += "**"+r.name + "**"
                if i == 0:
                    txt += " :trophy:"
                txt += " : "+str(len(r.members))+"\n"
                i += 1
        await ctx.send(txt)
        print("list asked at "+ctx.message.created_at.ctime()+" by "+str(ctx.message.author))
    else:
        role = None
        msg = ""
        i = 0
        print("Megaping lancé")
        test = ""
        for n in arr:
            test += n
        test.replace(" ", "").lower()
        for r in ctx.guild.roles:
            name = r.name.replace(" ", "").lower()
            if test in "team":
                break
            if (test in name) or (test == r.mention):
                if r.name in roles_list:
                    role = r
                    i += 1
        if i == 0:
            await ctx.send("Nom d'équipe pas trouvé, veuillez réessayer")
        elif i > 1:
            await ctx.send("Nom trop vague, veuillez réessayer")
        elif role is not None:
            txt = "__**Liste des membres de la "+role.name+" :**__\n"
            for r in role.members:
                txt += "  -"+r.name + "\n"
            if len(role.members) == 0:
                txt += "Personne :("
            await ctx.send(txt)
        else:
            await ctx.send("Fail")


@bot.command(name='ping', help='Pong!')
async def ping(ctx, *arr):
    await ctx.send("Pong!")


@bot.command(name='rejoin', help="Permet de faire rejoindre dans sa propre team. Ne marche que si l'auteur de la commande est dans une team et si l'invité n'en a pas")
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


@bot.command(name='degage', help="Permet de kick quelquun de sa propre team (marche sur soi meme). Ne marche que si l'auteur et le kické sont de la meme team")
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
    # if isinstance(error, commands.errors.CheckFailure):
    #     await ctx.send('You do not have the correct role for this command.')
    print(error)

bot.run(TOKEN)
