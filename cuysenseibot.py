import discord
from discord.ext import commands, tasks
import random
import asyncio
import os
import datetime
import time
import youtube_dl
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from io import BytesIO
from discord.utils import get
import traceback
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()

##################################################################################################################################
#variables comunes
###################################################################################################################################
invocacion = ["cuysenseibot", "Cuysenseibot", "CuySenseibot","CuySenseiBot", "diosabot"]
starter_hola = ["Aqui estoy para servirte", "Si? que deseas?", "lo siento la flojera me gana XD"]
saludos = ["hola","holas", "holitas", "holiwis", "saluditos", "saludos","hi"]
uwu = ["UwU", "OwO"]
respuestas = ["Es cierto", "Es definitivamente un así", "Sin duda", "Ni tu te la crees", "Como yo lo veo, parece que sí", "Muy probable", "El panorama parece ligeramente favorable", "Tiene una pinta a que si",
                "Pregunta de nuevo más tarde", "La respuesta no te gustara, mejor olvidalo", "Intenta otra vez", "Pregunta de nuevo más tarde", "Mejor no decirte ahora", "No puede hacerse realidad ni en tus sueños",
                "Concéntrate y pregunta otra vez", "No cuentes con ello", "Mi respuesta es no", "Mis fuentes dicen que no", "Olvidelo amigo", "Muy dificil", "Buena pregunta xd"]
ilegal = ['loli', 'fbi', 'ilegal','menor', 'niña', 'FBI', 'LOLI', 'ONU', 'ILEGAL', 'Loli']
estado = ['divertirse UwU', 'engordar, digo comer', 'dormir', 'lo que Maya juega','romperte el kokoro xd']
discordban = ["https://discord.gg", "discord.gg"]
numeracion = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26"]
queue = []
###########################################################################################################################################

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', description = "Soy el orgullo de mi creador UwU, para invocar al bot usar '!'",intents=intents)



####################################
#muestra su estado listo en consola
##############################################################################
@tasks.loop(seconds=18000)
async def cambiar_estado():
    await bot.change_presence(activity=discord.Game(name=random.choice(estado)))    
    #type=discord.ActivityType.listening o streaming o gamin

@bot.event
async def on_ready(): 
    print(f'Su {bot.user} esta listo para funcionar')
    cambiar_estado.start()
#   borrar_canciones.start()


#@bot.event
#async def on_member_join(member):
#    role = discord.utils.get(member.server.roles, id="723695124315373578")
#    print(f'alguien entro')
#    await bot.add_roles(member, role)

##############################################################################

@bot.command()
async def imagen(ctx):
  user = ctx.author

  base = Image.open("afondo.png")
  fotoperfil = user.avatar_url_as(size = 128)
  data = BytesIO(await fotoperfil.read())
  pfp = Image.open(data)
  pfp = pfp.resize((260,260))
  
  # Open the input image as numpy array, convert to RGB
  npImage=np.array(pfp)
  h,w=pfp.size
  # Create same size alpha layer with circle
  alpha = Image.new('L', pfp.size,0)
  draw = ImageDraw.Draw(alpha)
  draw.pieslice([0,0,h,w],0,360,fill=255)
  # Convert alpha Image to numpy array
  npAlpha=np.array(alpha)
  # Add alpha layer to RGB
  npImage=np.dstack((npImage,npAlpha))
  #  Save with alpha
  Image.fromarray(npImage).save('zresult.png')
  
  pfp2 = Image.open('zresult.png')
  base.paste(pfp2, (382,42), pfp2)
  base.save("zbienvenida.png")

  img = Image.open("zbienvenida.png")
  draw = ImageDraw.Draw(img)
    #font = ImageFont.truetype(<font-file>, <font-size>)
  font = ImageFont.truetype("font.otf", 52)
  W, H = (1024,500) #dimenciones de afondo.png
  mensaje1 = f'Saluditos! {ctx.message.author.name}'
  mensaje2 = f'Bienvenido a {ctx.guild.name} UwU'
  mensaje3 = f'Contigo ya {ctx.guild.member_count} somos Marisaurios'
  w, h = draw.textsize(mensaje1,font=font)
  #draw.text((x, y),"Sample Text",(r,g,b))
  draw.text(((W-w)/2, 315),mensaje1,(255,0,0),font=font) 
  w, h = draw.textsize(mensaje2,font=font)
  draw.text(((W-w)/2, 315+(h+8)),mensaje2,(0,0,255),font=font)
  w, h = draw.textsize(mensaje3,font=font)
  draw.text(((W-w)/2, 315 +(h+8)*2),mensaje3,(0,255,0),font=font)
  img.save("zbienvenida.png")
  await ctx.send(file = discord.File("zbienvenida.png"))
  os.remove('zresult.png')
  os.remove("zbienvenida.png")
  
#################################
#comandos
#######################################################################################################
@bot.command(help="Permite que ella escriba lo que tu escribes")
@commands.has_permissions(administrator=True)
async def echo(ctx, *, arg):
  time.sleep(0.2)
  await ctx.message.delete()
  if ctx.message.attachments:
    attachment = ctx.message.attachments[0]
    await attachment.save(attachment.filename)
    archivo = discord.File(f"{attachment.filename}")
    os.remove(f"{attachment.filename}")
    await ctx.send(arg, file = archivo)
  else :
    await ctx.send(arg)
  print(arg)

@bot.command(help="Escribe tu confesion")
async def confesion(ctx, *, arg):
  time.sleep(0.2)
  await ctx.message.delete()
  channel = bot.get_channel(824906651341553705)
  embed = discord.Embed(
    title = "Nueva confesión:",
    colour = discord.Colour.green(),
    description = f'{arg}'
  )
  embed.set_footer(text=f'Por anonimo el {time.strftime("%d-%m-%Y a las %H:%M")}')
  await channel.send(embed=embed)
  
@bot.command(help="hablo del mas alla")
@commands.has_permissions(administrator=True)
async def mari(ctx,canal, *, arg):
  time.sleep(1)
  await ctx.message.delete()
  for guild in bot.guilds:
        channel = get(guild.text_channels, name=f'{canal}')
        if channel is not None:
            if ctx.message.attachments:
              attachment = ctx.message.attachments[0]
              await attachment.save(attachment.filename)
              archivo = discord.File(f"{attachment.filename}")
              await channel.send(arg, file = archivo)
              os.remove(f"{attachment.filename}")
            else :
              await channel.send(arg)
            
            

@bot.command(help="muestra el link de invitacion a discord",aliases=['discord','server'])
async def invitacion(ctx):
  await ctx.send('El link de invitacion al server es: http://discord.gg/35PUYMK')
  
@bot.command(help="ip del server de minecraft",aliases=['maincra','ip'])
async def minecraft(ctx):
  await ctx.send('IP: marisaurios.myddns.rocks')
  
@bot.command(help="muestra las redes de marilya",aliases=['youtube', 'facebook', 'instagram','yt','fb', 'ig'])
async def redes(ctx):
  await ctx.send('- Twitch : https://www.twitch.tv/soy_marilya\n - YouTube : https://bit.ly/2N1fOVI\n- Facebook : https://www.facebook.com/SoyMarilya\n- Instagram: https://www.instagram.com/soy_marilya/?hl=es-la\n- Tiktok: https://www.tiktok.com/@soy_marilya')
  
@bot.command(help="manda patas xd")
async def patas(ctx, *args):
  dir = "patas"
  file_name = random.choice(os.listdir(dir))
  foto = discord.File(f"{dir}/{file_name}")
  async with ctx.typing():
    await ctx.send(file =foto)
    
@bot.command(help="mari fuera de contexto",aliases=['random'])
async def contexto(ctx, *args):
  dir = "contexto"
  file_name = random.choice(os.listdir(dir))
  archivo = discord.File(f"{dir}/{file_name}")
  async with ctx.typing():
    await ctx.send(file =archivo)
    
@bot.command(help="Sustos que dan gusto",aliases=['susto','sustos','asustame'])
async def sustilya(ctx, *args):
  dir = "sustilya"
  file_name = random.choice(os.listdir(dir))
  archivo = discord.File(f"{dir}/{file_name}")
  async with ctx.typing():
    await ctx.send(file =archivo)
    
@bot.command(help="Clips dando paltasa",aliases=['palta','aguacatilya'])
async def paltilya(ctx, *args):
  dir = "paltilya"
  file_name = random.choice(os.listdir(dir))
  archivo = discord.File(f"{dir}/{file_name}")
  async with ctx.typing():
    await ctx.send(file =archivo)

@bot.command(help="Manda video random de nuestra diosa bailando",aliases=['bailame','baile'])
async def baila(ctx, *args):
  dir = "bailame"
  if not args:
    file_name = random.choice(os.listdir(dir))
    video = discord.File(f"{dir}/{file_name}")
  elif args[0] == "bbcita":
    video = discord.File(f"{dir}/bbcita bb lin.mp4")
  elif args[0] == "niconiconi":
    video = discord.File(f"{dir}/Nico Nico Niii.mp4")
  elif args[0] == "mufin":
    video = discord.File(f"{dir}/mufin.mp4")
  elif args[0] == "vaquita":
    video = discord.File(f"{dir}/la vaquita.mp4")
  elif args[0] == "mufin":
    video = discord.File(f"{dir}/mufin.mp4")
  elif args[0] == "pudrete":
    video = discord.File(f"{dir}/pudranse todos.mp4")
  else:
    file_name = random.choice(os.listdir(dir))
    video = discord.File(f"{dir}/{file_name}")
    await ctx.channel.send(f'Lo siento no encontre eso pero te pondre algo random xd')
  async with ctx.typing():
    await ctx.send(file =video)

@bot.command(help="limpiar chat")
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=1):
  await ctx.channel.purge(limit=amount + 1)
  await ctx.channel.send(f'Se eliminaron {amount} mensajes')

@bot.command(help="botar a alguien del server")
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
  await member.kick(reason=reason)
  channel = bot.get_channel(771857809234198538)
  await channel.send(f'{member.mention} ha sido botado del server')

@bot.command(help="banear alguien del server")
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
  await member.ban(reason=reason)
  channel = bot.get_channel(771857809234198538)
  await channel.send(f'{member.mention} ha sido botado del server')

@bot.command(help="desbanear alguien del server")
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):
  banned_users = await ctx.guild.bans()
  member_name, member_discriminator = member.split('#')
  for ban_entry in banned_users:
      user = ban_entry.user
      if(user.name, user.discriminator) == (member_name, member_discriminator):
          await ctx.guild.unban(user)
          channel = bot.get_channel(771857809234198538)
          await channel.send(f'Se desbaneo a {user.mention}')
          return
          


@bot.command(help="prueba si el bot esta activo y te dice su ping de respuesta")
async def ping(ctx):
  await ctx.send(f'Pong! {round(bot.latency*1000)}ms')


@bot.command(help="dice el tamaño de su banana")
async def banana(ctx):
  dir = "banana"
  file_name = random.choice(os.listdir(dir))
  archivo = discord.File(f"{dir}/{file_name}")
  embed = discord.Embed(
    title = f"La banana de {ctx.message.author.name} mide {random.choice(numeracion)} cm.",
    colour = discord.Colour.random()
  )
  embed.set_image(url=f"attachment://{file_name}")
  await ctx.send(embed=embed, file=archivo)
  

@bot.command(aliases=['8ball', 'fortuna', 'pregunto'], help="preguntale algo de verdadero o falso")
async def caracola(ctx, *, pregunta):
  time.sleep(0.2)
  await ctx.message.delete()
  embed = discord.Embed(
    title = f"Preguntaste: {pregunta}",
    colour = discord.Colour.random(),
    description = f"Respuesta: {random.choice(respuestas)}"
  )
  embed.set_footer(text=f"Pregunta de {ctx.message.author.name}",icon_url="https://i.imgur.com/KqcY83X.jpeg")
  await ctx.send(embed=embed)

@bot.command(help="Resuelve operaciones basicas: + - * /")
async def resuelve(ctx, num1: float, signo:str, num2: float):
  if signo == '+':
    await ctx.send(num1 + num2)
  if signo == '-':
    await ctx.send(num1 - num2)
  if signo == '*':
    await ctx.send(num1 * num2)
  if signo == '/':
    if num2 == 0:
      await ctx.send("ah sos re troll")
    else:
      await ctx.send(num1 / num2)

@bot.command(help="Muestra informacion relevante del server")
async def info(ctx):
  embed = discord.Embed(title=f"{ctx.guild.name}", description="Holas", timestamp=datetime.datetime.utcnow(),color=discord.Color.blue())
  embed.add_field(name="Dia de creación", value=f"{ctx.guild.created_at}")
  embed.add_field(name="Dueño", value=f"{ctx.guild.owner}")
  embed.add_field(name="Region", value=f"{ctx.guild.region}")
  embed.set_thumbnail(url=f'{ctx.guild.icon_url}')
  await ctx.send(embed=embed)
###########################################################################################################################################


@bot.event
async def on_message(message):

  msg = message.content
  
  if message.channel.id == 757386257071603713: #el chat de anuncios
    emoji = bot.get_emoji(817242560036077588) #
    await message.add_reaction(emoji)
    emoji = bot.get_emoji(810202319144353803) #
    await message.add_reaction(emoji)
  
  elif message.channel.id == 845845985988706315: #el chat de spam
      return
  
  elif message.author == bot.user:
      return
  
  #elif message.author.id == 732802604530401331: 
      #return
  
  elif any(word in msg for word in discordban):
    await message.channel.purge(limit= 1)
    await message.channel.send(f'Se elimino el mensaje por hacer spam de otro server')

  elif any(word in msg for word in invocacion):
    await message.channel.send(random.choice(starter_hola))

  elif any(word in msg for word in uwu):
    await message.channel.send(random.choice(uwu))
    
  elif any(word in msg for word in ilegal):
    await message.channel.send("https://tenor.com/view/fbi-raid-swat-gif-11500735")
  

  await bot.process_commands(message)

############################################################################################
#youtube_dl.utils.bug_reports_message = lambda: '' #anula ver los errores y procesos de todo f

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
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
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)




@bot.command(name='play', help='Reproduce musica de la lista de reproduccion, no funciona la reproduccion automatica temporalmente') #funciona
async def play(ctx):
    if not ctx.message.author.voice:
        await ctx.send("No estas conectado a ningun canal de voz")
        return   
    voiceChannel = ctx.message.author.voice.channel
    voicebot = ctx.voice_client
    if voicebot is None:
        await voiceChannel.connect()  
    async with ctx.typing():
        server = ctx.message.guild
        voice_channel = server.voice_client
        player = await YTDLSource.from_url(queue[0], loop=bot.loop) 
        voice_channel.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
        await ctx.send(f'**Ahora sonando:** {player.title}')
        del(queue[0])


@bot.command(name='music',aliases=['m'], help='Reproduce musica de YT buscadas por nombre o url') #funciona, solo falta que continue la lista de reproduccion y borraar las descargadas
async def music(ctx, *, url):
    if not ctx.message.author.voice:
        await ctx.send("No estas conectado a ningun canal de voz")
        return
    global queue
    queue.append(url)
    voiceChannel = ctx.message.author.voice.channel
    voicebot = ctx.voice_client
    if voicebot is None:
        await voiceChannel.connect()  
    async with ctx.typing():
        server = ctx.message.guild
        voice_channel = server.voice_client
        if voice_channel.is_playing(): # cuando s ele agrega mientras suena lo pone en cola
            player = await YTDLSource.from_url(url)
            await ctx.send(f'**Se agrego a la lista de reproduccion:** {player.title}')
            return
        player = await YTDLSource.from_url(queue[0], loop=bot.loop)
        def play_next(ctx): #la principal manda a qui para crear el loopp
            if len(queue) >= 1:
                #player = asyncio.run(YTDLSource.from_url(queue[0], loop=bot.loop)) #no funciona por estar dentro de otro loop
                voice_channel.play(player, after=lambda e: print('Player error: %s' % e) if e else None) # after=lambda e: play_next(ctx)
                del(queue[0])
            else:
                return
        voice_channel.play(player, after=lambda e: play_next(ctx)) #reproduce la cancion  y lambda manda al loop de play_next arriba
        await ctx.send(f'**Ahora sonando:** {player.title}')
        del(queue[0])


@bot.command(name='next',aliases=['n'], help='Salta a la siguiente cancion') #funciona
async def next(ctx):
    server = ctx.message.guild
    voice_channel = server.voice_client
    voiceChannel = ctx.message.author.voice.channel
    async with ctx.typing():
        if not voice_channel.is_playing():
            return await ctx.send('No hay musica actualmente sonando...')
        voice_channel.stop()
        player = await YTDLSource.from_url(queue[0], loop=bot.loop) 
        voice_channel.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
        await ctx.message.add_reaction('⏭')
        await ctx.send(f'**Ahora sonando:** {player.title}')
        del(queue[0])


@bot.command(name='join',aliases=['j'], help='Obliga a que entre al chat de voz') #funciona
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send("No estas conectado a ningun canal de voz")
        return   
    else:
        channel = ctx.message.author.voice.channel
        await channel.connect()


@bot.command(aliases=['l'], help='me obliga a salirme del chat de voz') #funciona
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()
    else:
        await ctx.send("El bot no esta conectado a un canal de voz")


@bot.command(name='pause',aliases=['p'], help='pausa/despausa el audio sonando') #funciona
async def pause(ctx):
    server = ctx.message.guild
    voice_channel = server.voice_client
    if voice_channel.is_playing():
        voice_channel.pause()
        await ctx.send("Se ha pausado la cancion")
        await ctx.message.add_reaction('⏯')
        return
    if voice_channel.is_paused():
        voice_channel.resume()
        await ctx.send("Se ha despausado la cancion")
        await ctx.message.add_reaction('⏯')
        return
    


@bot.command(name='remove',aliases=['r'], help='Remueve una cancion de la lista de espera') #funciona
async def remove(ctx, number: int):
    global queue
    a = number - 1
    try:
        del(queue[int(a)])
        await ctx.send(f'Tu lista de espera es ahora: `{queue}!`')   
    except:
        await ctx.send('Tu lista de espera o esta **vacia** o el index esta **fuera del rango**')

@bot.command(name='view',aliases=['v'], help='Muestra la lista de espera')
async def view(ctx):
    await ctx.send(f'La lista de espera es de: `{queue}!`')


@bot.command(name='stop',aliases=['s'], help='Detiene la musica!')
async def stop(ctx):
    server = ctx.message.guild
    voice_channel = server.voice_client
    voice_channel.stop()
    await ctx.message.add_reaction('⏹')

##############
#token
##############
os.getenv("DISCORD_TOKEN")
########################################################################