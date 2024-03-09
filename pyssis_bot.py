#!/usr/bin/env python3

import os
# discord
import discord
from discord.ext import commands
# json
import json
# time
import time
import random

OurIntents = discord.Intents.default()
OurIntents.message_content = True

bot = commands.Bot(command_prefix='!', intents=OurIntents)


DISCORD_TOKEN = None


mode_list = ['idle', 'battle']
battle_next = ['idle', 'defense', 'evade', 'attack', 'powerattack']

# dimeritium - metal that supress magic
# mythril - weapon/shield material

# list of buffs

# make json serializable
class Player:
    def __init__(self, name, discord_id):
        self.name = name
        self.owner = discord_id
        self.params = {}
        self.params['health'] = 100
        self.params['last_provoke'] = 0
        self.params['stamina'] = 10
        self.params['mode'] = 'idle'
        self.params['battle_mode'] = 'normal'

    def to_dict(self):
        return {'name': self.name, 'owner': self.owner, 'params': self.params}
    def from_dict(self, d):
        self.name = d['name']
        self.owner = d['owner']
        self.params = d['params']


class PlayersDB:
    def __init__(self):
        self.players = {}
        self.load_json()
    def add_player(self, player):
        self.players[player.owner] = player
        self.save_json()
    def get_player(self, discord_id):
        if discord_id in self.players:
            return self.players[discord_id]
        return None

    def load_json(self, filename='players.json'):
        if not os.path.isfile(filename):
            print(f'File {filename} not found')
            return
        with open (filename, 'r') as f:
            j = json.load(f)
            for k, v in j.items():
                print(f'k: {k}, v: {v}')
                # now iterable is a dict of dicts
                player = Player('', 0)
                player.from_dict(v)
                # convert string to int
                player.owner = int(k)
                self.players[player.owner] = player


    def save_json(self, filename='players.json'):
        with open (filename, 'w') as f:
            j = {}
            for k, v in self.players.items():
                j[k] = v.to_dict()
            json.dump(j, f)

PLAYERS = PlayersDB()

# on ready
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

# help command
@bot.command(name='helpme')
async def helpme(ctx):
    message = '!create имяперсонажа - создать персонажа прикрепленного к вашему Discord аккаунту\n'
    message += '!stats - показать статы вашего персонажа (только в личку)\n'
    message += 'Если вы в стойле, то лечится и чинится надо в публичном канале. Если вы в пустоши, можете общаться с ботом в личку, вас не видят\n'
    message += '!heal - прилечь поспать и восстанавливать здоровье (будет восстанавливать random(1-15)% каждые 5 минут)\n'
    message += '!list - DEBUG, список игроков\n'
    message += '!id - мой Discord ID\n'
    message += '--- режим боя ---\n'
    message += '---- команды боя в личку бота ----\n'
    message += '!defend - оборона, стандартный удар противника наносит 0 урона, силовой удар - половину урона. stamina-1\n'
    message += '!evade - третичная вероятность исходов(увернулся и ответил, увернулся, не успел увернутся): ответный удар на 5-15%, уклонение, получение двукратного урона. stamina-1\n'
    message += '!attack имяперсонажа - нанести стандартный удар, урон 5-30%. stamina-1\n'
    message += '!powerattack имяперсонажа - нанести силовой удар, урон 15-45%. После удара игрок будет дезориентирован на один ход. stamina-2\n'
    message += '---- публичные команды боя ----\n'
    message += '!approach @DiscordID - приблизится к другому игроку\n'
    message += '!distance @DiscordID - отдалиться от другого игрока\n'
    message += '!provoke @DiscordID - провоцировать другого игрока\n'
    message += '!fight @DiscordID - начать пошаговую битву'
    message += '--- режим порнобитвы ---\n'
    message += 'делать?'
    await ctx.send(message)


PROVOKELIST = []

# check if player has person
async def check_player(ctx):
    player = PLAYERS.get_player(ctx.author.id)
    if player is None:
        await ctx.send(f'У вас нет персонажа')
        return None
    return player

# provoke
@bot.command(name='provoke')
async def provoke(ctx, name):
    player = await check_player(ctx)
    if player is None:
        return
    # check if last provoke was less than 5 minutes ago
    if 'last_provoke' in player.params:
        if time.time() - player.params['last_provoke'] < 60:
            await ctx.send(f'Вы уже провоцировали недавно, подождите')
            return
    # random PROVOKELIST
    rndidx = random.randint(0, len(PROVOKELIST)-1)
    #await ctx.send(f'{ctx.author.name} тест {name}')
    message = f'{ctx.author.name} {PROVOKELIST[rndidx]} {name}'
    player.params['last_provoke'] = time.time()
    await ctx.send(message)

# create character
@bot.command(name='create')
async def create(ctx, name):
    # check if player already has character
    player = PLAYERS.get_player(ctx.author.id)
    if player is not None:
        await ctx.send(f'У вас уже есть персонаж {player.name}')
        return
    player = Player(name, ctx.author.id)
    PLAYERS.add_player(player)
    await ctx.send(f'Персонаж {name} создан')

# list
@bot.command(name='list')
async def list(ctx):
    message = 'Список игроков:\n'
    for k, v in PLAYERS.players.items():
        message += f'{v.name} owned by ({v.owner})\n'
    await ctx.send(message)

# id
@bot.command(name='id')
async def id(ctx):
    await ctx.send(f'Ваш Discord ID: {ctx.author.id}')

# stats
@bot.command(name='stats')
async def stats(ctx):
    player = await check_player(ctx)
    if player is None:
        return
    # dont show stats in public
    if ctx.guild is not None:
        await ctx.send('Посмотреть статы можно только в личку')
        return
    message = f'Персонаж {player.name}:\n'
    for k, v in player.params.items():
        message += f'{k}: {v}\n'
    await ctx.send(message)

# on message
@bot.event
async def on_message(message):
    print(f'{message.author} sent: {message.content}')
    if message.author == bot.user:
        return
    await bot.process_commands(message)


def get_token():
    global DISCORD_TOKEN
    # check if file .token exists
    if os.path.isfile('.token'):
        with open('.token', 'r') as f:
            DISCORD_TOKEN = f.read().strip()
    else:
        DISCORD_TOKEN = os.environ.get('DISCORD_TOKEN')
    return DISCORD_TOKEN

    
def main():
    global PROVOKELIST
    # get token
    token = get_token()
    if token is None:
        print('No token found')
        return
    # load players
    PLAYERS.load_json()
    # load provoke list from provokelist.json
    try:
        with open('provokelist.json', 'r') as f:
            PROVOKELIST = json.load(f)
    except:
        print('No provokelist.json found')
    # list of players
    print('Players:')
    for k, v in PLAYERS.players.items():
        print(f'{v.name} owned by ({v.owner})')
    # add commands
    bot.run(token)

if __name__ == '__main__':
    main()
    

