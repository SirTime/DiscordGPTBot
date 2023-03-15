import os
import discord
import openai
import logging
import random
import asyncio
from dotenv import load_dotenv
from keep_alive import keep_alive

load_dotenv()  # Load environment variables from .env file

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)
openai.api_key = OPENAI_API_KEY

logging.basicConfig(filename='discord_bot.log', level=logging.ERROR,
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')

statuses = [    '20 questions',    'Round of trivia',    'Would You Rather',    'Round of Rock, Paper, Scissors',    'Tic-Tac-Toe',    'Hangman',    'Blackjack',    'Chess',    'Minesweeper',    'Connect Four',    'Roulette',    'Truth or Dare',    'Simon Says',    'Bingo',    'Charades',    'Pictionary',    'Hangman',    'Uno',    'Checkers',    'Jenga',    'Scrabble',    'Battleship',    'Crossword Puzzle',    'Mastermind',    'Poker',    'Bridge',    'Memory',    'Dominos',    'Solitaire',    'Go Fish',    'Hangman',    'Snakes and Ladders',    'Monopoly',    'Clue',    'Risk',    'Stratego',    'War',    'Magic: The Gathering',    'Dungeons & Dragons',    'Settlers of Catan',    'Carcassonne',    'Ticket to Ride',    'Pandemic',    'Betrayal at Baldurs Gate',    'Munchkin',    'Fluxx',    'Exploding Kittens',    'Cards Against Humanity',    'Quiplash',    'Fibbage',    'Drawful',    'Trivia Murder Party',    'Push the Button',    'Keep Talking and Nobody Explodes',    'Among Us',    'Fall Guys',    'Fortnite',    'Minecraft',    'Roblox',    'Stardew Valley']
# Add more statuses as desired

async def change_status():
    await client.wait_until_ready()
    while not client.is_closed():
        status = random.choice(statuses)
        await client.change_presence(activity=discord.Game(name=status), status=discord.Status.online)
        print(f'Status changed to {status}')
        await asyncio.sleep(86400)  # Sleep for 24 hours (in seconds)
      
@client.event
async def on_ready():
    print('Bot is ready.')
    client.loop.create_task(change_status())

async def generate_response(prompt):
    try:
        response = await openai.Completion.create(
          engine='text-davinci-002',
          prompt=prompt,
          temperature=0.7,
          max_tokens=1024,
          n=1,
          stop=None,
          timeout=15,
        )

        reply = response.choices[0].text.strip()
        if len(reply) > 2000:
            reply = reply[:1997] + '...'
        
        if "code" in reply:
            reply = "```\n" + reply + "\n```"

        return reply

    except openai.error.InvalidRequestError as e:
        logging.error("InvalidRequestError: " + str(e))
        return "There was an error with the OpenAI API request. Please check your API key and try again."

    except openai.error.AuthenticationError as e:
        logging.error("AuthenticationError: " + str(e))
        return "There was an authentication error with the OpenAI API request. Please check your API key and try again."

    except openai.error.APIConnectionError as e:
        logging.error("APIConnectionError: " + str(e))
        return "There was an error connecting to the OpenAI API. Please check your internet connection and try again."

    except openai.error.OpenAIError as e:
        logging.error("OpenAIError: " + str(e))
        return "There was an error with the OpenAI API request. Please try again later."

@client.event
async def on_message(message):
    # Check if the message is a direct message to the bot or a mention in a server channel
    if isinstance(message.channel, discord.DMChannel) or (client.user in message.mentions and isinstance(message.channel, discord.TextChannel)):
        # Remove the mention of the bot from the message content
        prompt = message.content.replace(client.user.mention, '').strip()

        # Call the OpenAI API to generate a response
        response = openai.Completion.create(
            engine="davinci",
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        )

        # Send the response back to the channel or DM
        await message.channel.send(response.choices[0].text)

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if client.user in message.mentions:  # Check if the bot was mentioned in the message
    prompt = message.content.replace(
      client.user.mention,
      '').strip()  # Remove the bot mention from the message content

    funny_prompt = f"Write a funny but accurate response, under 2000 characters, to: {prompt}?"

    if prompt.lower() == "prompts":
      await message.channel.send("Here are some prompts you can ask me:\n- Tell me a joke\n- What's the weather like in New York City?\n- Who won the last Super Bowl?\n- What is the capital of France?\n- What's the highest mountain in the world?\n- Who created you?\n- Who owns you?\n- Can you show me a link?")
      return

    if prompt.lower() == "review":
      await message.channel.send("Sure! You can review me here : https://top.gg/bot/1084360000916439050#reviews")
      return

    if prompt.lower() == "website":
      await message.channel.send("Sure! You can find my website here : https://discordgpt.framer.website/")
      return

    if prompt.lower() == "invite":
      await message.channel.send("Sure! You can invite me here : https://discord.bots.gg/bots/1084360000916439050")
      return

    if prompt.lower() in ["who is your girlfriend?", "who is your girlfriend?", "who is your gf?", "who is your gf", "who is ur gf?", "who is ur gf"]:
      await message.channel.send("Rizzz#3485")
      return

    if prompt.lower() in ["who is Timepass?", "what is Timepass?", "who is Timepass", "what is timepass", "who is Timepass#4446", "who is Timepass#4446"]:
      await message.channel.send("He is my master.")
      return

    if prompt.lower() in ["who created you", "who created you?", "who developed you", "who programmed you", "who designed you", "who built you", "who authored you", "who constructed you", "who invented you", "who fabricated you", "who engineered you", "who developed you?", "who programmed you?", "who designed you?", "who built you?", "who authored you?", "who constructed you?", "who invented you?", "who fabricated you?", "who engineered you?", "who owns you", "who owns you?", "who made you", "who made you?", "who is your owner", "who is your owner?", "who is your father", "who is your father?", "who is your creator", "who is your creator?", "who is your daddy", "who is your daddy?", "who is your friend?", "who is your friend", "who is your best friend?", "who is your best friend", "owner"]:
      await message.channel.send("Timepass#4446")
      return

    response = openai.Completion.create(
      engine='text-davinci-002',
      prompt=funny_prompt,
      temperature=0.7,
      max_tokens=1024,
      n=1,
      stop=None,
      timeout=15,
    )

    reply = response.choices[0].text.strip()
    if len(reply) > 2000:
            reply = "Due to discord word limitations, I can only type upto 2000 characters."

    if "code" in prompt.lower():
      reply = "```\n" + reply + "\n```"
    
    await message.channel.send(f'{message.author.mention}:  {reply}')

keep_alive()
client.run(DISCORD_TOKEN)


