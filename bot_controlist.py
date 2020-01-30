# bot.py

import os
import json
import yaml
import datetime
import discord
import time
from copy import deepcopy
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

global PATH, BIGDATA, MAX_BEFORE_BACKUP, MAX_BEFORE_MSG, ROLES_LIST, MANUAL_BACKUP

MANUAL_BACKUP = False
PATH = 'score.yml'
MAX_BEFORE_BACKUP = 30*60
MAX_BEFORE_MSG = 5


with open(PATH) as f:
    data = yaml.load(f, Loader=yaml.FullLoader)
    BIGDATA = data

    ROLES_LIST = []
    for n in data:
        ROLES_LIST.append(n["name"])


def backup_score():
    with open('score.yml', mode="r+") as f:
        data = yaml.dump(BIGDATA, f)


def check_roles(member):
    i = 0
    for r in member.roles:
        if r.name in ROLES_LIST:
            i += 1
    return i


def get_rol(member):
    for r in member.roles:
        if r.name in ROLES_LIST:
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
            if r.name in ROLES_LIST:
                if i == 0:
                    txt += ":trophy: "
                txt += "**"+r.name + "**"
                if i == 0:
                    txt += " :trophy:"
                txt += " : "+str(len(r.members))+"\n"
                i += 1
        await ctx.send(txt)

    else:
        role = None
        i = 0
        test = ""
        for n in arr:
            test += n
        test.replace(" ", "").lower()
        for r in ctx.guild.roles:
            name = r.name.replace(" ", "").lower()
            if test in "team":
                break
            if (test in name) or (test == r.mention):
                if r.name in ROLES_LIST:
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
    print("list asked at "+ctx.message.created_at.ctime()+" by "+str(ctx.message.author))


@bot.command(name='ping', help='Pong!')
async def ping(ctx):
    await ctx.send("Pong!")


def sort_data(d):
    return d["score"]


@bot.command(name='score', help='Affiche le score actuel de chaque equipe')
async def score(ctx):
    copydata = deepcopy(BIGDATA)
    copydata.sort(key=sort_data, reverse=True)
    txt = "**__Liste des scores__ :** \n"
    i = 0
    for d in copydata:
        txt += " - "
        if i == 0:
            txt += ":trophy: "
        txt += "**"+d["name"] + "**"
        if i == 0:
            txt += " :trophy:"
        txt += ": "+str(d["score"])+"\n"
        i += 1
    await ctx.send(txt)


@bot.command(name='back', help='Enregistre le score actuel. Activé : '+str(MANUAL_BACKUP))
async def backup(ctx):
    if MANUAL_BACKUP:
        backup_score()
        await ctx.send("backed")


@bot.command(name='limit', help='Affiche les différentes limites')
async def limit(ctx):
    txt = "Les backup des scores se font toute les "+str(MAX_BEFORE_BACKUP)+" secondes, quand un message est recu\n"
    txt += "Limite antispam : "+str(MAX_BEFORE_MSG)+" secondes d'attente PAR EQUIPE avant de recevoir un point"
    await ctx.send(txt)


@bot.command(name='join', help="Permet de faire rejoindre dans sa propre team. Ne marche que si l'auteur de la commande est dans une team et si l'invité n'en a pas")
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


def score_management(message):
    role = get_rol(message.author)
    if role is not None:
        for d in BIGDATA:
            if(role.name == d["name"]):
                if(d["lastmsg"] is None):
                    d["lastmsg"] = time.time()
                lmsg = time.time()-d["lastmsg"]
                if lmsg >= MAX_BEFORE_MSG:
                    d["score"] += 1
                    d["lastmsg"] = time.time()


def reponses_timbot(message):
    if "timbot" in message.content.lower():
        if "merci" in message.content.lower():
            return"Mais de rien, "+str(message.author.display_name)+"!"
        if "hein" in message.content.lower() and "?" in message.content.lower():
            if message.author.id == 123742890902945793:
                return "Mais oui, évidemment "+str(message.author.display_name)+"!"
            else:
                return "Pourquoi tu me demande? J'ai l'air d'être ton ami?"


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    msg = reponses_timbot(message)
    if msg is not None:
        await message.channel.send(msg)
    score_management(message)

    back = time.time()-os.path.getmtime(PATH)
    if back >= MAX_BEFORE_BACKUP:
        backup_score()
        print("backing")
    await bot.process_commands(message)


@bot.event
async def on_command_error(ctx, error):
    # if isinstance(error, commands.errors.CheckFailure):
    #     await ctx.send('You do not have the correct role for this command.')
    print(error)

bot.run(TOKEN)
