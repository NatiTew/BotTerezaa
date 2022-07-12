# from replit import db
# keys = db.keys()
# for row in keys:
#   del db[row]

import os
import numpy as np
import random
import discord
from os import system
from time import sleep
from keepAlive import keep_alive
from discord.ext import commands
from replit import db
from discord.ext.commands import has_permissions, MissingPermissions

my_secret = os.environ['Token']

listA1 = []
listB1 = []
listC1 = []

client = commands.Bot(command_prefix='+')

valueArr = random.sample(range(300), 300)
np.random.shuffle(valueArr)

@client.event
async def on_ready():
    print(f'Successfully logged in as {client.user}')

def chData(name:str):
  keys = db.keys()
  for row in keys:
    if row == name:
      return True
  return False

@client.command()
async def info(ctx):
  async for message in ctx.channel.history(limit=1):
    await message.delete()
  await ctx.send("❈────────•✦•กระดานคำสั่ง•✦•────────❈\n"
                  "+whoami          → เช็คสถานะแอดมิน\n"
                  "+add <@name> 1   → เพิ่ม point (เฉพาะแอดมิน)\n"
                  "+cut <@name> 1   → ลด point (เฉพาะแอดมิน)\n\n"
                  "(ทุกคนสามารถใช้ได้ทุกคน)\n\n"
                  "+show        → เช็ค point ตัวเอง\n"
                  "+s <@name>   → เช็ค point คนอื่น\n"
                  "+board       → เปิด LeaderBoard 25 อันดับแรก\n\n"
                  "❈────────•✦•❅•✦•────────❈\n")

def sort_list(list1, list2):
 
    zipped_pairs = zip(list2, list1)
 
    z = [x for _, x in sorted(zipped_pairs)]
     
    return z

def cal_board1():
  global listA1
  global listB1
  global listC1

  listA1 = []
  listB1 = []
  listC1 = []
  
  keys = db.keys()
  for row in keys:
    if row != 'item':
      value = db[row]
      # ch = isinstance(value[1],int)
      ch = 'player' in value
      if ch == True:
        listA1.append(row)
        listB1.append(value[0])
  # print(listA)
  # print(listB)
  listC1 = sort_list(listA1, listB1)
  listC1.reverse()
  
  
@client.command()
@has_permissions(administrator = True)
async def add(ctx, player: discord.Member, input: int):
  sPlayer = str(player.id)
  np = 'n' + str(player.id)
  nPlayer = str(player.name)
  check = False
  keys = db.keys()
  for row in keys:
    if row == sPlayer:
      check = True
      # print(check)
      break
  if check == True:
    value = db[sPlayer]
    value[1] = (value[1] + input)
    # print(value[0])
    db[sPlayer] = value
    db[np] = nPlayer
  else:
    db[np] = nPlayer
    arr = ['player',0]
    arr[1] = input
    # print(arr[0])
    db[sPlayer] = arr
  # print('<@'+ sPlayer +'> add '+ str(input) +'♚DouCoin')
  await ctx.channel.send('<@'+ sPlayer +'> add '+ str(input) +'𝓟')


@add.error
async def add_error(ctx, error):
  if isinstance(error, MissingPermissions):
    text = "Sorry {}, you do not have permissions to do that!".format(ctx.message.author)
    await ctx.send(text)

@client.command()
@has_permissions(administrator = True)
async def cut(ctx, player: discord.Member, input: int): 
  
  sPlayer = str(player.id)
  np = 'n' + str(player.id)
  nPlayer = str(player.name)
  check = False
  keys = db.keys()
  for row in keys:
    if row == sPlayer:
      check = True
      break
  if check == True:
    value = db[sPlayer]
    print(value)
    value[1] = value[1] - input
    if value[1] < 0:
      await ctx.channel.send('Error คะแนนติดลบ')
    else:
      db[sPlayer] = value
      db[np] = nPlayer
      await ctx.channel.send('<@'+ sPlayer +'> del '+ str(input) +'𝓟')
  else:
    await ctx.channel.send('<@'+ sPlayer +'> Not Found')

@cut.error
async def cut_error(ctx, error):
  if isinstance(error, MissingPermissions):
    text = "Sorry {}, you do not have permissions to do that!".format(ctx.message.author)
    await ctx.send(text)

@client.command()
async def show(ctx):
  sPlayer = str(ctx.author.id)
  np = 'n' + str(ctx.author.id)
  nPlayer = str(ctx.author.name)
  check = False
  keys = db.keys()
  for row in keys:
    if row == sPlayer:
      check = True
      break
  if check == True:
    value = db[sPlayer]
    db[np] = nPlayer
    print(sPlayer)
    await ctx.channel.send('<@'+ sPlayer +'> have '+ str(value[1]) + ' 𝓟')
  else:
    await ctx.channel.send('Not Found')
   
@client.command()
async def s(ctx, player: discord.Member):
  sPlayer = str(player.id)
  np = 'n' + str(player.id)
  nPlayer = str(player.name)
  check = False
  keys = db.keys()
  for row in keys:
    if row == sPlayer:
      check = True
      break
  if check == True:
    value = db[sPlayer]
    db[np] = nPlayer
    await ctx.channel.send(nPlayer +' have '+ str(value[1]) + ' 𝓟')
  else:
    await ctx.channel.send('Not Found')

@client.command()
async def board(ctx):
  async for message in ctx.channel.history(limit=1):
    await message.delete()
  cal_board1()
  print(listC1)
  embed = discord.Embed(title=f"{'----------<Leader Board>----------'}", description=('แสดง Top25'),color=discord.Color.red())
  num = 0
  while num < len(listC1):
    value = db[listC1[num]]
    nameDis = str(listC1[num])
    embed.add_field(name=str(value[1]) + ' 𝓟' , value=f"{'<@'+nameDis+'>'}")
    num += 1
  await ctx.send(embed=embed)

@client.command()
async def b(ctx):
  await ctx.channel.send('ขอเวลาบอทคิดแปปนึง')
  cal_board1()
  #print(listC)
  output = " ----------<Leader Board>---------- \n"
  output = output + " ถ้าชื่อใครไม่ขึ้นให้ใช้คำสั่ง +show ก่อนแล้วมาลองใหม่ \n"
  num = 0
  while num < len(listC1):
    value = db[listC1[num]]
    nameDis = str(listC1[num])
    np = 'n' + nameDis
    #print(np)
    keys = db.keys()
    #print(keys)
    check = False
    for row in keys:
      if row == np:
        check = True
        break
    if check == True:
      nameDis = db[np]
      output = output + ''+ str(value[1]) + '𝓟 ของ ' +nameDis + ' \n'
    else:
      output = output + ''+str(value[1]) + '𝓟 ของ ' + '<@'+nameDis+'> \n'
    num += 1
    if num%25 == 0:
      await ctx.send('```' + output + '```' )
      output = " ----------<Leader Board>---------- \n"
      output = output + " ถ้าชื่อใครไม่ขึ้นให้ใช้คำสั่ง +show ก่อนแล้วมาลองใหม่ \n"
    elif num == len(listC1):
      await ctx.send('```' + output + '```' )
      output = " ----------<Leader Board>---------- \n"
      output = output + " ถ้าชื่อใครไม่ขึ้นให้ใช้คำสั่ง +show ก่อนแล้วมาลองใหม่ \n"

@client.command(pass_context = True)
@has_permissions(administrator = True)
async def whoami(ctx):
  await ctx.send('คุณเป็น administrator')

@whoami.error
async def whoami_error(ctx, error):
  if isinstance(error, MissingPermissions):
    text = "Sorry {}, you do not have permissions to do that!".format(ctx.message.author)
    await ctx.send(text)

@client.command()
async def restart(ctx): 
  await ctx.channel.send('Test Restart')
  print("\n\nRESTARTING NOW\n\n\n")
  await ctx.channel.send('kill process')
  print('kill')
  system('kill 1')
  await ctx.channel.send('sleep')
  print('sleep')
  sleep(7)
  await ctx.channel.send('restart')
  print('restart')
  system("python main.py")

keep_alive()
try:
    client.run(my_secret)
except discord.errors.HTTPException:
  print("\n\n\nBLOCKED BY RATE LIMITS\nRESTARTING NOW\n\n\n")
  system("python restarter.py")
  
  
  