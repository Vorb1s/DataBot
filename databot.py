import discord
from discord.ext import commands
import asyncio
import datetime

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
    if message.content.startswith('!test'):
        #stores the number of messages
        counter = 0
        start_time = datetime.datetime.now()
        await client.delete_message(message)
        #the temporary message which
        tmp = await client.send_message(message.channel, 'Calculating messages...')
        for channel in message.server.channels:
            async for log in client.logs_from(channel, limit=50000):
                if log.author == message.author:
                    counter += 1
        end_time = datetime.datetime.now()
        uptime = end_time - start_time
        print('Got data for {}, in {}. Took {}.'.format(message.author.name, message.server.name, uptime))
        await client.edit_message(tmp, '{}, you have {} messages. Took {} seconds.'.format(message.author.display_name, counter, uptime))
    elif message.content.startswith('!sleep'):
        await client.delete_message(message)
        await asyncio.sleep(5)
        await client.send_message(message.channel, 'Done sleeping')

client.run('MzI5NTAwNzk4Njg3OTAzNzQ4.DDTXQw.u1Xpgh7wheexFLooG0bBycypSOI')
