import discord
import asyncio
import logging
from horsebase import HorseBase
import os

client = discord.Client()
hb = HorseBase()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@client.event
async def on_ready():
    logging.info('------')
    logging.info('Logged in as')
    logging.info(client.user.name)
    logging.info(client.user.id)
    logging.info('------')

@client.event
async def on_message(message):
    if message.author == client.user:
            return
    elif message.content.startswith('!help'):
        logging.info('Found !help')
        await client.send_message(message.server, '!horse to post a :horse: \n!totalhorses for amout' +
        ' of :horse: posted on this server \n!myhorses to tell how many :horse: you posted \n!tophorses' +
        ' to see who posted the most :horse:')
        logging.info('Finished !help')
    elif message.content.startswith('!horse'):
        logging.info('Found !horse')
        await client.send_message(message.server, ':horse:')
        logging.info('Finished !horse')
    elif message.content.startswith('!totalhorses'):
        logging.info('Found !totalhorses')
        await client.send_message(message.server, 'Total amount of ' +
        str(hb.getTotalHorses(message.server.name)) + ' :horse: posted in this channel')
        logging.info('Finished !totalhorses')
    elif message.content.startswith('!myhorses'):
        logging.info('Found !myhorses')
        author = (message.author.nick if message.author.nick else message.author.name)
        myhorses = hb.getMyHorses(message.server.name, author)
        await client.send_message(message.server, author + ', you have posted ' +
        str(myhorses['month']) + ' :horse: this month and ' + str(myhorses['total']) +
        ' :horse: since the beginning of time.')
        logging.info('Finished !myhorses')
    elif message.content.startswith('!tophorses'):
        logging.info('Found !tophorses')
        tophorses = hb.getTopHorses(message.server.name, 3)
        if len(tophorses['month']) == 0 and len(tophorses['alltime']) == 0:
            return
        msg = ""
        if len(tophorses['month']) > 0:
            msg += "Top posters of this month are: \n"
            for m in tophorses['month']:
                msg += m[0] + " with " + str(m[1]) + " :horse: \n"
        if len(tophorses['alltime']) > 0:
            msg += "All time top posters are: \n"
        for m in tophorses['alltime']:
                msg += m[0] + " with " + str(m[1]) + " :horse: \n"
        await client.send_message(message.server, msg)
        logging.info('Finished !tophorses')
    elif '🐴' in message.content or 'horse' in message.content.lower():
        logging.info('Found horse in a message')
        if '🐴' in message.content:
            hb.addHorseToDB(message.server.name, message.timestamp, message.author.nick if message.author.nick else message.author.name)
        await client.add_reaction(message, '🐴')
        logging.info('Finished horse')
    else:
        logging.info('No horses found in message')
    if 'hi kuubio' in message.content.lower():
        logging.info('Found hi kuubio')
        await client.send_message(message.server, 'HI KUUBIO! :horse:')
        logging.info('Finished hi kuubio')

client.run(os.environ.get('DISCORD_TOKEN'))
