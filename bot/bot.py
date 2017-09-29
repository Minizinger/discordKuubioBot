import discord
import asyncio
from horsebase import HorseBase

client = discord.Client()
hb = HorseBase()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    if message.author == client.user:
            return
    if message.content.startswith('!help'):
        await client.send_message(message.server, '!horse to post a :horse: \n !totalhorses for amout of :horse: posted on this server \n !myhorses to tell how many :horse: you posted \n !tophorses to see who posted the most :horse:')
    if message.content.startswith('!horse'):
        await client.send_message(message.server, ':horse:')
    if message.content.startswith('!totalhorses'):
        await client.send_message(message.server, 'Total amount of ' + str(hb.getTotalHorses(message.server)) + ' :horse: posted in this channel')
    if message.content.startswith('!myhorses'):
        author = (message.author.nick if message.author.nick else message.author.name)
        myhorses = hb.getMyHorses(message.server, author)
        await client.send_message(message.server, author + ', you have posted ' + myhorses['month'] + ' :horse: this month and ' + myhorses['total'] + ' :horse: since the beginning of time.')
    if message.content.startswith('!tophorses'):
        tophorses = hb.getTopHorses(message.server, 3)
        if len(tophorses['month']) == 0 and len(tophorses['alltime']) == 0:
            return
        message = ""
        if len(tophorses['month']) > 0:
            message += "Top posters of this month are: \n"
            for m in tophorses['month']:
                message += m[0] + " with " + m[1] + " :horse: \n"
        if len(tophorses['alltime']) > 0:
            message += "All time top posters are: \n"
        for m in tophorses['alltime']:
                message += m[0] + " with " + m[1] + " :horse: \n"
        await client.send_message(message.server, message)
    if '🐴' in message.content or 'horse' in message.content.lower():
        if '🐴' in message.content:
            hb.addHorseToDB(message.server, message.timestamp, message.author.nick if message.author.nick else message.author.name)
        await client.add_reaction(message, '🐴')
    if 'hi kuubio' in message.content.lower():
        await client.send_message(message.server, 'HI KUUBIO! :horse:')

client.run('bot token here')
