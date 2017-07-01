import discord
from discord.ext import commands
import asyncio
import datetime

countcommand= "!msgcount" #choose a command to activate count
token =  "" #token goes here

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
        print("{} requested data in {}.".format(message.author.name, message.server.name))
        await client.delete_message(message)

        if len(message.mentions) == 0 and len(message.channel_mentions) == 0:
            await countmessages(message.author, message.author, message.server.channels, message)
        else:
            if len(message.channel_mentions) == 0:
                for n in message.mentions:
                    await countmessages(n, message.author, message.server.channels, message)
            elif len(message.mentions) == 0:
                await countmessages(message.author, message.author, message.channel_mentions, message)
            else:
                for n in message.mentions:
                    await countmessages(n, message.author, message.channel_mentions, message) #call the count message function

    elif message.content.startswith('!sleep'):
        await client.delete_message(message)
        await asyncio.sleep(5)
        await client.send_message(message.channel, 'Done sleeping')

async def countmessages(user, mauthor, SearchChannel, message): #function to retrieve the message count
    counter = 0
    start_time = datetime.datetime.now()
    tmp = await client.send_message(message.channel, "Counting {}'s messages...".format(user.display_name))#temp message
    for channel in SearchChannel:
        async for log in client.logs_from(channel, limit=50000):
            if log.author == user:
                counter += 1
    end_time = datetime.datetime.now()
    uptime = end_time - start_time
    print("Retrieved {}'s data for {}, in {}. Took {}.".format(user.name, message.author.name, message.server.name, uptime))
    await client.edit_message(tmp, '{} has posted {} messages. Took {} seconds.'.format(user.display_name, counter, uptime))

client.run(token)
