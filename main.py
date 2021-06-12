import os #hides token
import discord
import random
import local_database
import youtube_dl
import asyncio
import time
import tenor
#from commands import run_commands
from zenquote import get_quote
from keep_alive import keep_alive
from discord.ext import commands
#https://discord.com/oauth2/authorize?client_id=851180231800520734&permissions=2148005952&scope=bot

start_time = time.time();
###########################################################################

youtube_dl.utils.bug_reports_message = lambda: ''
ytdl_format_options = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}
ffmpeg_options = {
    'options': '-vn'
}
ytdl = youtube_dl.YoutubeDL(ytdl_format_options)
class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = ""
    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]
        filename = data['title'] if stream else ytdl.prepare_filename(data)
        return filename

###########################################################################

bot = commands.Bot(command_prefix="!", case_insensitive = True)
#word_monitor = ["Conan"]

#word_responses = ["Detective Conan is not even a good show kappa"]

@bot.event
async def on_ready():
  #time program uptime
  
  #set status of client
  await bot.change_presence(status=discord.Status.online, activity=discord.Game('with your heart'))

  print('Logged in as' )
  print(bot.user.name)
  print(bot.user.id)
  print('------')



@bot.command()
async def hello(ctx):
    await ctx.send('안녕하세요!')

@bot.command()
async def inspire(ctx):
  quote = get_quote() 
  embed = discord.Embed(title="", description= quote, color = 0xcc99cc)
  await ctx.send(embed=embed)

@bot.command()
async def commands(ctx):
  embedret = discord.Embed(title="IU - List of Commands", description="prefix: !", color = 0xcc99cc)
  embedret.add_field(name="!hello", value="IU says hello back", inline=False)
  embedret.add_field(name="!inspire", value="IU inspires you", inline=False)
  embedret.add_field(name="!flipcoin", value="IU flips a coin", inline=False)
  embedret.add_field(name="!uptime", value="IU's uptime", inline=False)
  embedret.add_field(name="!gif <terms..>", value="Get a gif based on search terms", inline=False)
  await ctx.send(embed=embedret)

"""@bot.command()
async def play(ctx, arg):
  if arg == "palette":
    await ctx.send("https://www.youtube.com/watch?v=d9IxdwEFk1c")"""

@bot.command()
async def flipcoin(ctx):
  if random.randint(1, 2) == 1:
    side = "Heads"
  else:
    side = "Tails"

  ret = side + ", " + local_database.getFlipCoinResponse()
  embed = discord.Embed(title="", description=ret,color = 0xcc99cc)
  await ctx.send(embed=embed)

@bot.command()
async def kumiko(ctx):
  await ctx.send('https://imgur.com/FPjjOuh')

@bot.command()
async def gif(ctx, *, arg):
  gif = tenor.getGif(arg);
  embedret = discord.Embed(title="", description=arg, color = 0xcc99cc)
  embedret.set_image(url=gif)
  await ctx.send(embed=embedret)

@bot.command()
async def uptime(ctx):

  elapsed_time = time.time() - start_time
  days = 0
  if elapsed_time >= 86400:
    days = int(elapsed_time / 86400)
  elapsed = time.strftime("%H hours, %M minutes and %S seconds.", time.gmtime(time.time() - start_time))
  if days == 0:
    ret = f"I've been singing for {elapsed}"
  else:
    ret = f"I've been singing for {days} days, {elapsed}"
  embed = discord.Embed(title="", description=ret,color = 0xcc99cc)
  await ctx.send(embed=embed)

####################################################################
#voice channel commands
@bot.command(name='join', help='Tells the bot to join the voice channel')
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send("{} is not in a channel!".format(ctx.message.author.name))
        return
    else:
        channel = ctx.message.author.voice.channel
    await channel.connect()

@bot.command(name='leave', help='To make the bot leave the voice channel')
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()
    else:
        await ctx.send("But I'm not in a channel...")

@bot.command(name='play_song', help='To play song')
async def play(ctx,url):
    try :
        server = ctx.message.guild
        voice_channel = server.voice_client
        async with ctx.typing():
            filename = await YTDLSource.from_url(url, loop=bot.loop)
            voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=filename))
        await ctx.send('**Now playing:** {}'.format(filename))
    except:
        await ctx.send("The bot is not connected to a voice channel.")
###################################################################

keep_alive()
#runs the bot
bot.run(os.environ['token']) #token is generated by discord


'''
@client.event  
async def on_message(message):

  
  if message.author == client: #does nothing if the message is from the bot/client
    return
  
  

  msg = message.content.lower() #sets message to lowercase

  #responds with Hello! if someone types $hello
  if msg.startswith('!hello'):
    await message.channel.send('안녕하세요!')
  
  if msg.startswith('!inspire'):
    quote = get_quote()
    await message.channel.send(quote)

  if msg.startswith('!kumiko'):
    await message.channel.send('https://imgur.com/FPjjOuh')
  #if any(word in msg for word in word_monitor):
  #  await message.channel.send(random.choice(word_responses))
  await client.process_commands(message)
'''

