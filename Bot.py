import discord
from decouple import config
from playwright.async_api import async_playwright, expect
from discord import FFmpegPCMAudio
from discord.ext import commands, tasks
import os
import random
import string
import re





intents = discord.Intents.default()
intents.members = True
client = discord.Client()
bot = commands.Bot(command_prefix="!")
queue = []
variFodase = False



async def pasta_ale():
    global nome_ale
    number_of_strings = 1
    length_of_string = 15
    for x in range(number_of_strings):
        nome_ale = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length_of_string))
    

def check_queue(ctx):
    voice = ctx.guild.voice_client
    source = queue.pop(0)
    player = voice.play(source)
    


async def apaga_arquivo():
    for i in os.listdir(luga_destinado):
        os.remove(os.path.join(luga_destinado, i))
    os.rmdir(luga_destinado)

async def musica_nome():
    global retorno
    # Nome Musica --------------------------------------------------------------------
    frase  = nome_file
    remover = ['10convert.com', '_']
    lista_frase = frase.split()
    result = [palavra for palavra in lista_frase if palavra.lower() not in remover]
    retorno = ' '.join(result)
    index = retorno.index('.')
    retorno = retorno[:index]
    #----------------------------------------------------------------------------------   



async def wmusic(link_musica):
    try:
        async with async_playwright() as p:
            nav = await p.chromium.launch()
            pagina = await nav.new_page()
            await pagina.goto(link_musica)
            crl = pagina.url
            crl2 = crl.replace("https://www.youtube.com", "https://www.csyoutube.com")
            await pagina.goto(crl2)
            async with pagina.expect_download() as download_info:
                await pagina.locator('xpath=//*[@id="youtubeDownloadUrls2"]/tr[1]/td[5]/button').click()
            global nome_file
            global luga_destinado
            download = await download_info.value
            path = await download.path()
            nome_file = download.suggested_filename
            luga_destinado = "./" + "fodase" + "/"
            musica_caminho = os.path.join(luga_destinado, nome_file)
            await download.save_as(musica_caminho)
            #time.sleep(2)
    except Exception:
        os.system("playwright install")



async def pesquisa_y3(nome):
    try:
        async with async_playwright() as p:
            nav =  await p.chromium.launch()
            pagina = await nav.new_page()
            await pagina.goto("https://www.youtube.com/results?search_query=" + nome)
            await pagina.locator(':nth-match(h3:has(a#video-title), 1)').click()
            fodase = pagina.url
            fodase2 = fodase.replace("https://www.youtube.com", "https://www.csyoutube.com")
            await pagina.goto(fodase2)
            async with pagina.expect_download() as download_info:
                await pagina.locator('xpath=//*[@id="youtubeDownloadUrls2"]/tr[1]/td[5]/button').click()
            global nome_file
            global luga_destinado

            download = await download_info.value
            path = await download.path()
            nome_file = download.suggested_filename
            luga_destinado = "./" + nome_ale + "/"
            musica_caminho = os.path.join(luga_destinado, nome_file)
            await download.save_as(musica_caminho)
    except Exception:
        os.system("playwright install")
    






@bot.event
async def on_ready():
    print("tá funcionando")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    await bot.process_commands(message)



@bot.command(name="play", aliases=["p", "P", "tocar"])
@commands.cooldown(1, 30, commands.BucketType.guild)
async def play(ctx, *, musica):
    if (ctx.author.voice):
        global variFodase
        voice2 = client.get_channel('id')
        channel = ctx.message.author.voice.channel

        try:
            voice = await channel.connect()
            await ctx.guild.change_voice_state(channel=channel, self_deaf=True)
        except Exception:
            voice = ctx.guild.voice_client

        if voice.is_playing() == False:
            msg = await ctx.send("Aguarde um pouco...")
            #await queue_(ctx=ctx, musica=musica)
            if variFodase != True:
                await pasta_ale()
                variFodase = True
            
            
            if ".com" in musica:
                await wmusic(link_musica=musica)
            else:
                pesquisa = musica
                fodase = re.sub(r"\s+", "+", pesquisa)
                await pesquisa_y3(nome=fodase)

            source = FFmpegPCMAudio(luga_destinado + nome_file)
            player = voice.play(source, after=lambda x=None: check_queue(ctx))#, after=lambda x=None: check_queue(ctx, ctx.message.guild.id)
            await musica_nome()
            await msg.delete()
            await ctx.send("*Tocando agora " + retorno + "!*")
            
        else:
            #await queue_(ctx=ctx, musica=musica)
            await ctx.send("Já tem uma música tocando... Espere acabar!")
    else:
        await ctx.send("Entre em um canal de voz!")



@bot.command(name="queue", aliases=["fila", "Q", "q"])
async def queue_(ctx, *, musica):
    global queue
    if ".com" in musica:
        await wmusic(link_musica=musica)
    else:
        pesquisa = musica
        fodase = re.sub(r"\s+", "+", pesquisa)
        await pesquisa_y3(nome=fodase)

    source = FFmpegPCMAudio(luga_destinado + nome_file)
    queue.append(source)
    await ctx.send("Música adicionada")


@bot.command(name="pause", aliases=["pa", "pausa"])
async def pause(ctx):
    #voice = discord.utils.get(client.voice_clients,guild=ctx.guild)
    voice = ctx.guild.voice_client
    if voice.is_playing():
        voice.pause()
        await ctx.send("Música pausada!")
    else:
        await ctx.send("Não tem musica tocando!")


@bot.command(name="resume", aliases=["continuar", "R", "r"])
async def resume(ctx):
    #voice = discord.utils.get(client.voice_clients,guild=ctx.guild)
    voice = ctx.guild.voice_client
    if voice.is_paused():
        voice.resume()
        await ctx.send("A música está despausada!")


@bot.command(name="stop", aliases=["parar", "S", "s"])
async def stop(ctx):
    #voice = discord.utils.get(client.voice_clients,guild=ctx.guild)
    voice = ctx.guild.voice_client
    voice.stop()
    await ctx.send("A música foi parada!")


    
@bot.command(name="l", aliases=["leave", "sair"])
async def leave(ctx):
    voice = ctx.guild.voice_client
    if (ctx.author.voice) or voice.is_connected():
        await voice.disconnect()
        await ctx.send("Desconectado!")
        await apaga_arquivo()
    else:
        await ctx.send("Não estou em um canal de voz!")





@bot.command(name="cmds", aliases=["commands", "comanndos", "ajuda"])
async def send_help(ctx):

    await ctx.send("""
```
Comandos:
!p (!play, !tocar)-- Toca a musica
!s (!stop, !parar) -- Parar a música
!pa (!pause, !pausa) -- Pausar uma música
!l (!leave, !sair) -- Sair do canal de voz
!r (!resume, !continuar) -- Continuar a música
!q (!queue, !lista) -- Adiciona uma musica a fila
```
    """)

@tasks.loop(seconds=2)
async def check_vc(ctx):
    voice = ctx.guild.voice_client
    if voice.is_paused() or voice.is_playing() == False:
        await voice.disconnect()
        await apaga_arquivo()
        





    


TOKEN = config("TOKEN")
bot.run(TOKEN)
