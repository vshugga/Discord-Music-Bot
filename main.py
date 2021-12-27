import discord
from discord import FFmpegPCMAudio
from discord.ext import commands
import yt_dlp
import time
import os

intents = discord.Intents.default()
intents.members = True
bot_token = ''
size_limit = 20000000
connect_sound = 'fart.ogg'
queues = {}

# Use '!' as the command prefix
client = commands.Bot(command_prefix = '!')


# YoutubeDL options
ydl_opts = {
            'format': 'bestaudio/best', 
            'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            'outtmpl': 'audio/%(id)s.%(ext)s',
            'noplaylist': True
        }

# Parse properties file
def get_properties():
    global bot_token
    with open('properties.txt') as f:
        for line in f:
            if line.startswith('api_key='):
                bot_token = line[8:]
            elif line.startswith('path='):
                local_files = line[5:]
            elif line.startswith('limit='):
                size_limit = line[6:]

# When the bot is ready, recieve commands
@client.event
async def on_ready():
    print("The bot is ready.")

# !play; Play audio
@client.command(pass_context = True)
async def play(ctx, url:str, codec='mp3', quality='192'):
    '''Play a song from YouTube Link/ID'''

    if (ctx.voice_client):

        ydl_opts['postprocessors'][0]['preferredcodec'] = codec
        ydl_opts['postprocessors'][0]['preferredquality'] = quality

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=False)

                await ctx.send("Downloading: " + info_dict['title'] + ".")
                filesize = info_dict['filesize']
                print('File Size: ' + str(filesize))
                if filesize > size_limit:
                    raise Exception("File is too large.")
                else:
                    ydl.download([url])
        except Exception as e:
            await ctx.send("Youtube-DL Error: " + str(e))
            print(e)
            return False

        for f in os.listdir("./audio"):
            if info_dict['id'] in f: # If the ID is in file name, set that as the file to play.
                audio = f
            else:
                try:
                    os.remove("./audio/" + f) # Try to remove files if not in use.
                except Exception as e:
                    print('Not deleting ' + f + ': ' + str(e))

        voice = ctx.guild.voice_client
        guild_id = ctx.message.guild.id

        voice_check = discord.utils.get(client.voice_clients,guild=ctx.guild)
        voice_active = voice_check.is_playing() or voice_check.is_paused()

        if voice_active:
            voice.stop()
        source = FFmpegPCMAudio('./audio/' + audio)
        voice.play(source)
        await ctx.send("Playing: " + info_dict['title'] + ".")
    else:
        await ctx.send("Must be in voice channel to run !play.")

# !queue; Queue audio to be played
@client.command(pass_context = True)
async def queue(ctx, url:str, codec='mp3', quality='192'):
    '''Queue a song to be played next (under development)'''
    pass

# !pause; Pause audio
@client.command(pass_context = True)
async def pause(ctx):
    '''Pause audio'''
    voice = discord.utils.get(client.voice_clients,guild=ctx.guild)
    if voice.is_playing():
        voice.pause()

# !resume; Resume audio
@client.command(pass_context = True)
async def resume(ctx):
    '''Resume paused audio'''
    voice = discord.utils.get(client.voice_clients,guild=ctx.guild)
    if voice.is_paused():
        voice.resume()

# !stop; Stop audio
@client.command(pass_context = True)
async def stop(ctx):
    '''Stop currently playing audio'''
    voice = discord.utils.get(client.voice_clients,guild=ctx.guild)
    voice.stop()

# !join; Join voice channel
@client.command(pass_context = True)
async def join(ctx):
    '''Join a voice channel'''
    if (ctx.voice_client):
        channel = ctx.message.author.voice.channel
        await ctx.send("Bot is already connected to this voice channel: " + str(channel))
        return 

    if (ctx.author.voice):
        channel = ctx.message.author.voice.channel
        voice = await channel.connect()
        await ctx.send("Bot is connected to voice channel: " + str(channel))
        source = FFmpegPCMAudio('./oggs/' + connect_sound) # Play sound on connect
        player = voice.play(source)
    else:
        await ctx.send("Must be in voice channel to run !join.")

# !leave; Leave voice channel
@client.command(pass_context = True)
async def leave(ctx):
    '''Leave a voice channel'''
    if (ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
        await ctx.send("Leaving voice channel.")
    else:
        await ctx.send("Bot is not in a voice channel.")

# !test; ctx is discord messaging
@client.command()
async def test(ctx):
    '''Test command'''
    await ctx.send("Test command functional.")

get_properties()
client.run(bot_token)




'''

# !clear; Clear queue
@client.command(pass_context = True)
async def clear(ctx):
    guild_id = ctx.message.guild.id
    queues[guild_id].clear()
    await ctx.send("Queue cleared.")


def check_queue(ctx, id):
    if queues[id] != []:
        voice = ctx.guild.voice_client
        voice_check = discord.utils.get(client.voice_clients,guild=ctx.guild)
        source = queues[id].pop(0)
        
        #print('Voice paused: ' + str(bool(voice_check.is_paused)))
        #print('Voice playing: ' + str(bool(voice_check.is_playing)))

        #if not (voice_check.is_paused or voice_check.is_playing):
        
        player = voice.play(source, after=lambda x=None: check_queue(ctx, id)) # Queue automatically plays songs remaining in queue
        player = voice.play(source)
        player = voice.play(source)

        return True
'''


