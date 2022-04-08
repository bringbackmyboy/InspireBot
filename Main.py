import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive

client = discord.Client()

sad_words = ['blue', 'dejected', 'depressed', 'despondent', 'down', 'droopy', 'hangdog', 'inconsolable', 'low', 'melancholic', 'melancholy', 'mirthless', 'sad', 'unhappy', 'woebegone', 'woeful'
'dim', 'discomfiting', 'discouraging', 'disheartening', 'dismaying', 'dispiriting', 'distressful', 'distressing', 'upsetting'
'desperate', 'hopeless', 'pessimistic',
'lamentable', 'mournful', 'plaintive', 'sorrowful'
'colorless', 'drab', 'dull']

starter_encouragements = [
  "Cheer up!",
  "Hang in there.",
  "You are a great person / bot!"
]

if "responding" not in db.keys():
  db["responding"] = True

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [encouraging_message]

def delete_encouragment(index):
  encouragements = db["encouragements"]
  if len(encouragements) > index:
    del encouragements[index]
    db["encouragements"] = encouragements

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content

  if msg.startswith('$repeat'):
    await message.channel.send(msg.split("$repeat ",1)[1])

  if msg.startswith('$inspire'):
    quote = get_quote()
    await message.channel.send(quote)
    

  if db["responding"]:
    options = starter_encouragements
    if "encouragements" in db.keys():
      options.extend(db["encouragements"])

    if any(word in msg for word in sad_words):
      await message.channel.send(random.choice(options))

  if msg.startswith("$new"):
    encouraging_message = msg.split("$new ",1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send("New encouraging message added.")

  if msg.startswith("$del"):
    encouragements = []
    if "encouragements" in db.keys():
      index = int(msg.split("$del",1)[1])
      delete_encouragment(index)
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)

keep_alive()
client.run(os.environ['Token'])
