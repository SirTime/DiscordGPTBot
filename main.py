import os
import discord
import openai
from dotenv import load_dotenv
from keep_alive import keep_alive

load_dotenv()  # Load environment variables from .env file

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)
openai.api_key = OPENAI_API_KEY


@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if client.user in message.mentions:  # Check if the bot was mentioned in the message
    prompt = message.content.replace(
      client.user.mention,
      '').strip()  # Remove the bot mention from the message content

    response = openai.Completion.create(
      engine='text-davinci-002',
      prompt=prompt,
      temperature=0.7,
      max_tokens=1024,
      n=1,
      stop=None,
      timeout=15,
    )

    reply = response.choices[0].text.strip()

    await message.channel.send(f'{message.author.mention} {reply}')


keep_alive()
client.run(DISCORD_TOKEN)
