import json
import os
import random
import shutil

import discord
import requests

my_secret = os.environ['token']

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)
  


def getImage():
  api_key = ''    // your api key goes here
  url = "https://api.api-ninjas.com/v1/randomimage"
  headers = {'X-Api-Key': api_key, 'Accept': 'image/png'}

  response = requests.get(url, headers=headers, stream=True)
  with open('img.jpg', 'wb') as out_file:
    shutil.copyfileobj(response.raw, out_file)
    # await channel.send(file=discord.File('img.jpg'))
  return 'img.jpg'


async def getRecipe(query, channel):
  api_key = ''    // your api key goes here
  url = 'https://api.api-ninjas.com/v1/recipe?query={}'.format(query)
  headers = {'X-Api-Key': api_key}
  response = requests.get(url, headers=headers)
  selected_recipe = random.choice(response.json())
  for key, value in selected_recipe.items():
    await channel.send(f"{key.upper()}: {value}")


class Client(discord.Client):

  async def on_ready(self):
    print(f'we have logged in as {self.user}')

  async def on_message(self, message):
    if message.author == self.user:
      return

    if message.content.startswith('$help'):
      await message.channel.send(
          'Commands: \n $help - \n $recipe - gets a random recipe \n $image - to get random image'
      )
    if message.content.startswith('$hello'):
      await message.channel.send('hello')

    # if message.content.startswith('$image'):
    #   await getImage(message.channel)

    if message.content.startswith('$image'):
      image_file = getImage()
      await message.channel.send(file=discord.File(image_file))

    if message.content.startswith('$recipe'):
      query = message.content[len('$recipe'):].strip()
      channel = message.channel
      await getRecipe(query, channel)

    if message.content.startswith('$inspire'):
      quote = get_quote()
      await message.channel.send(quote)

  

intents = discord.Intents.default()
intents.message_content = True
client = Client(intents=intents)
client.run(f'')    // your discord api key goes here
