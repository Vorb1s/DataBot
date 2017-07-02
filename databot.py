import discord
from discord.ext import commands
import asyncio
import datetime
import pickle


try:
    msgData = pickle.load(open('msgData.obj', 'rb')) 
except:
    msgData = [[],[]]
    
countcommand= "!msgtotal" #choose a command to activate count
trackcommand = "!msgtrack" #the command to start tracking a user
token = "MzI5NTAwNzk4Njg3OTAzNzQ4.DDmBDQ.KnKS_TYWfFvsDJ579GyjjRMQCMk" #token goes here

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

    elif message.content.startswith(trackcommand):
        await client.delete_message(message)
        await trackmessages(message)
        
    
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

async def trackmessages(message):
    start_time = datetime.datetime.now()
    user = message.author
    server = message.server
    sid = server.id
    uid = user.id
    newuser = False;

    tmp = await client.send_message(message.channel, "Counting {}'s messages...".format(user.display_name))#temp message
    if sid in msgData[0]:  #If the server is already loaded
        sindex = msgData[0].index(sid)
        if uid in msgData[1][sindex][0]:  #if the user already has data in that server
            print ("Retrieving data for {} in server {}.".format(user.name, message.server.name))
            uindex = msgData[1][sindex][0].index(uid)

        else:
            sindex = msgData[0].index(sid)
            msgData[1][sindex][0].append(uid)
            uindex = msgData[1][sindex][0].index(uid)
            userData = [[] for i in range(2)]
            msgData[1][sindex][1][uindex] = userData
            newuser = True
            print ("Getting new data for {} in server {}.".format(user.name, message.server.name))

    else:
        try:
            print ("Getting new data for {} in new server {}.".format(user.name, message.server.name))
            msgData[0].append(sid)
            sindex = msgData[0].index(sid)
            msgData[1].append([[],[]])
            msgData[1][sindex][0].append(uid)
            uindex = msgData[1][sindex][0].index(uid)
            userData = [[] for i in range(2)]
            msgData[1][sindex][1].append(userData)
            newuser = True
        except:
            print ('Something failed lol')
            
    if newuser == True:        
        for channel in server.channels:
            async for log in client.logs_from(channel, limit=100000):
                if log.author == user:
                    msgData[1][sindex][1][uindex][1].append([message.channel, message.timestamp])
    else:
        lastmsgtimestamp = msgData[1][sindex][1][uindex][1][-1][1]
        for channel in server.channels:
            async for log in client.logs_from(channel, limit=100000, after = lastmsgtimestamp):
                if log.author == user:
                    msgData[1][sindex][1][uindex][1].append([message.channel, message.timestamp])

    userMessages = len(msgData[1][sindex][1][uindex][1])
    end_time = datetime.datetime.now()
    uptime = end_time - start_time
    await client.edit_message(tmp, '{} has posted {} messages. Took {} seconds.'.format(user.display_name, userMessages, uptime))

    file_pi = open('msgData.obj', 'wb')
    pickle.dump(msgData, file_pi) 

client.run(token)
