import discord
from discord.ext import commands
import asyncio
import datetime

countcommand= "!msgcount" #choose a command to activate count function
token = "" #token goes here

client = discord.Client()
bot = commands.Bot(command_prefix='?', description='A simple discord python bot')


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    if message.content.startswith(countcommand):
        inp = message.content
        if message.content.endswith(countcommand): #if the command is all the message says, retrieve data for self
            user = str(message.author.display_name)
        else: #if the command includes more than just the message, take that as the user to retrieve for
            inp = inp.split(" ", maxsplit=1)
            user = inp[1]
        print("Retrieving {}'s data for {}, in {}. Command: '{}'.".format(user, message.author.name, message.server.name, inp))
        await countmessages(user, message.author, message) #call the count message function

    elif message.content.startswith('!sleep'):
        await client.delete_message(message)
        await asyncio.sleep(5)
        await client.send_message(message.channel, 'Done sleeping')

async def countmessages(user, mauthor, message): #function to retrieve the message count
    counter = 0
    start_time = datetime.datetime.now()
    await client.delete_message(message)
    #the temporary message which
    tmp = await client.send_message(message.channel, 'Calculating messages...')
    for channel in message.server.channels:
        async for log in client.logs_from(channel, limit=50000):
            if str(log.author.display_name).startswith(user):
                counter += 1
    end_time = datetime.datetime.now()
    uptime = end_time - start_time
    print("Retrieved {}'s data for {}, in {}. Took {}.".format(user, message.author.name, message.server.name, uptime))
    await client.edit_message(tmp, '{} has posted {} messages. Took {} seconds.'.format(user, counter, uptime))

client.run(token)
