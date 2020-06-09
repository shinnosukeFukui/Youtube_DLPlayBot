# -*- coding: utf-8 -*-

import discord
import youtube_dl
import sys

youtube_url = 'URL'

ydl_opts = {
                    'format': 'bestaudio/best',
                    'outtmpl':  "ThirdMK2_music" + '.%(ext)s',
                    'postprocessors': [
                        {'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                         'preferredquality': '192'},
                        {'key': 'FFmpegMetadata'},
                    ],
                }
ydl = youtube_dl.YoutubeDL(ydl_opts)

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    if message.author.bot:
        return
    
    if message.content.startswith("おはよう"):
        await message.channel.send("Hello Youtube, コマンド一覧を観たいときは”list”と入力")
        return
    
    if message.content.startswith("list"):
        await message.channel.send("join:ボイスチャンネルへ参加")
        await message.channel.send("break:ボイスチャンネルから退出")
        await message.channel.send("dl URL:URL先の動画を音声ファイルとしてダウンロード（URLはyoutubeの動画のURLであること）")
        await message.channel.send("play:最後にダウロードされた音声ファイルを再生")
        await message.channel.send("stop:現在再生中の音声ファイルを停止")
        await message.channel.send("pause:一時停止")
        await message.channel.send("resume:再生再開")
        await message.channel.send("upfile:最後にダウンロードされた音声ファイルをテキストチャンネルにアップロード")
        await message.channel.send("end:このbotをログアウト")
        return
    
    if message.content.startswith("join"):
         voice_state = message.author.voice
         if (not voice_state) or (not voice_state.channel):
            await message.channel.send("先にボイスチャンネルに入っている必要があります")
            return
    
         channel = voice_state.channel
         await channel.connect()
         print("connected to:",channel.name)
         return
     
    if message.content.startswith("break"):
         voice_client = message.guild.voice_client
         if not voice_client:
             await message.channel.send("ボイスチャンネルに参加していません")
             return
         await voice_client.disconnect()
         print("disconnect")
         return
         
    if message.content.startswith("dl"):
         msg =  message.content
         msglist = msg.split()
         if len(msglist) < 2 or len(msglist) > 2:
                await message.channel.send("?")
                return
         else :
                 youtube_url = msglist[1]  
                 if ('&list' in youtube_url):
                     await message.channel.send("再生リストは対象外です")
                     return
                 await message.channel.send("ダウンロードを開始します…")
                 
                 meta = ydl.extract_info(youtube_url, download=False) 
                 print ('duration:%s' %(meta['duration']))
                 if meta['duration'] > 3600:
                     await message.channel.send("【エラー】")
                     await message.channel.send("1時間以内の動画にしてください")
                     return
                 ydl.extract_info(youtube_url, download=True)
                 await message.channel.send("ダウンロード完了")
                 return
                 
    if message.content.startswith("play"):
        voice_client = message.guild.voice_client
        
        if not voice_client:
            await message.channel.send("ボイスチャンネルに参加していません")
            return
        
        ffmpeg_audio_source = discord.FFmpegPCMAudio("ThirdMK2_music.mp3")
        await message.channel.send("再生を開始します")
        voice_client.play(ffmpeg_audio_source)
        return
    
    if message.content.startswith("stop"):
        voice_client = message.guild.voice_client
        
        if not voice_client:
            await message.channel.send("ボイスチャンネルに参加していません")
            return
        if not voice_client.is_playing():
            await message.channel.send("再生中ではありません")
            return
        await message.channel.send("再生を停止します")
        voice_client.stop()
        return
    
    if message.content.startswith("pause"):
        voice_client = message.guild.voice_client
        
        if not voice_client:
            await message.channel.send("ボイスチャンネルに参加していません")
            return
        if not voice_client.is_playing():
            await message.channel.send("再生中ではありません")
            return
        if voice_client.is_paused():
            await message.channel.send("一時停止中です")
            return
        await message.channel.send("一時停止します")
        voice_client.pause()
        return
    
    if message.content.startswith("resume"):
        voice_client = message.guild.voice_client
        
        if not voice_client:
            await message.channel.send("ボイスチャンネルに参加していません")
            return
        if not voice_client.is_paused():
            await message.channel.send("再生は停止中ではありません")
            return
        await message.channel.send("再生を再開します")
        voice_client.resume()
        return
    
    if message.content.startswith("upfile"):
        await message.channel.send("現在保存されている音声ファイルをアップロード…")
        await message.channel.send(file=discord.File('ThirdMK2_music.mp3'))
        return
    
    """
    # discordに8MB以上のファイルをアップできないため削除
    mp4ydl = youtube_dl.YoutubeDL({'outtmpl': "ThirdMK2" + '.%(ext)s','format':'137'})
    if message.content.startswith("mp4dl"):
         msg =  message.content
         msglist = msg.split()
         if len(msglist) < 2 or len(msglist) > 2:
                await message.channel.send("?")
                return
         else :
                 youtube_url = msglist[1]  
                 if ('&list' in youtube_url):
                     await message.channel.send("再生リストは対象外です")
                     return
                 await message.channel.send("ダウンロードを開始します…")
                 
                 meta = ydl.extract_info(youtube_url, download=False) 
                 print ('duration:%s' %(meta['duration']))
                 if meta['duration'] >1800:
                     await message.channel.send("【エラー】")
                     await message.channel.send("1時間以内の動画にしてください")
                     return
                 mp4ydl.extract_info(youtube_url, download=True)
                 await message.channel.send("ダウンロード完了")
                 return
             
    if message.content.startswith("mp4upfile"):
        await message.channel.send("現在保存されている動画ファイルをアップロード…")
        await message.channel.send(file=discord.File('ThirdMK2.mp4'))
        return
    """
    
    if message.content.startswith("end"):
            await message.channel.send("お疲れ様でした")
            await client.logout()
            await sys.exit()

 
client.run('TOKEN')
