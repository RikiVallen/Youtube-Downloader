from tkinter.ttk import Style
from pytube import YouTube
from pytube import Search, Channel
from pathlib import Path
import tkinter as tk
from tkinter import filedialog
import os
import datetime
from colorama import init, Fore, Style
init()

## Default Global Variables
data = {
    'audioOnly': False,
    'videoLimit': 5,
    'downloadLocation': str(Path.home() / "Downloads")
    }
 
currentLimit = 5
audioOnly = False

print('Welcome to Youtube Downloader 3000-2 Electric Boogaloo')
print('--------------------------------------------------------')

def main():
    
    while True:
        print('[1] Search\n[2] Configure\n[3] Exit')
        print('--------------------------------------------------------')
        try:
            menuChoice = int(input("> "))
        except:
            print("Invalid Choice")
        print('--------------------------------------------------------')
   
        if menuChoice == 1:
            if not search():
                print("See ya! press any key to quit")
                input("> ")
                clearConsole()
                break
                

        elif menuChoice == 2:
            options()
        elif menuChoice == 3:
            break
        else:
            print(Fore.RED, 'That option does not exist')
            print(Fore.RESET, '--------------------------------------------------------')


def search():
    
    print('Enter a name or URL')
    searchText = input('> ')
    print('--------------------------------------------------------')

    if searchText[0:32] == "https://www.youtube.com/watch?v=":
        
  
        downloaded = urlSearch(searchText)       
    else:
        youtubeSearch = Search(searchText)
        searchResults = youtubeSearch.results[:data['videoLimit']]
        displayResults(searchResults)
        downloaded = chooseVideo(searchResults)

    if downloaded:
        print('Downloaded to location: ', data['downloadLocation'])
        print('--------------------------------------------------------')
    
    print('\nDownload another video? (y/n)')
    continueDownloading = input("> ").lower()
    if continueDownloading == 'y':
        return True
    else:
        return False
        
             
def urlSearch(searchText):

    yt = YouTube(searchText)
    print(f'Downloading {yt.title}...')
    print('--------------------------------------------------------')


    if data['audioOnly']:
        yt.streams.filter(only_audio=audioOnly).first().download(data['downloadLocation'])    
    else:
        yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download(data['downloadLocation'])
    return True


def displayResults(results):

    videoCount = 1

    for video in results:
        channelName = getChannelName(video.channel_id)
        videoLength = getVideoLength(video.length)
        colorOutput(video, videoCount)
        print(Style.RESET_ALL, end="")
        print("    Length:\t", end="")
        print(f' {videoLength}')
        print(Style.RESET_ALL, end="")
        print("    Channel:\t", end="")
        print(Fore.MAGENTA, f'{channelName}')
        print(Style.RESET_ALL)
        

        videoCount += 1

def getVideoLength(seconds):
    return str(datetime.timedelta(seconds = seconds))

def getChannelName(channel_id):
    channelUrl =  f'https://www.youtube.com/channel/{channel_id}'
    channel = Channel(channelUrl)
    return channel.channel_name

def colorOutput(video, count):
    videoTitle = (video.title[0:75])

    print(f'[{count}] {videoTitle}\t', end="")
    if int(video.views) > 100000:
        print(Fore.GREEN, f'Views: {video.views}')
        
    elif int(video.views) < 1000:
        print(Fore.RED, f'Views: {video.views}')
        
    else:
        print(Fore.YELLOW, f'Views: {video.views}')
        

def chooseVideo(results):

    print('Enter the video number you wish to download')
    try:
        videoChoice = int(input('> '))
    except:
        print('No Video Selected\n')
        return
    url = "www.youtube.com/watch?v=" + results[videoChoice - 1].video_id
    yt = YouTube(url)

    print('--------------------------------------------------------')
    print(f'Downloading {results[videoChoice - 1].title}...')
    print('--------------------------------------------------------')

    if data['audioOnly']:
        yt.streams.filter(only_audio=True).first().download(data['downloadLocation'])    
    else:
        yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download(data['downloadLocation'])


def options():

    while True:
        print('[1] Track Download Limit:\t', data['videoLimit'])
        print('[2] Audio Only Mode:\t\t', data['audioOnly'])
        print('[3] Set Download Location:\t', data['downloadLocation'])
        print('--------------------------------------------------------')
        try:
            option = int(input('> '))
        except:
            break

        if option == 1:
            print('Track Download Limit:\t', data['videoLimit'])
            try:
                data['videoLimit'] = int(input('> '))
            except:
                print('Invalid Option')
                break
        elif option == 2:
            print('Toggle Audio Only Mode:\t\t', data['audioOnly'])
            try:
                data['audioOnly'] = not data['audioOnly']
            except:
                print('Invalid Option')
                break
        elif option == 3:
            print('Set Download Location:\t\t', data['downloadLocation'])
            try:
                root = tk.Tk()
                root.withdraw()
                data['downloadLocation'] = filedialog.askdirectory()
                if data['downloadLocation'] == "":
                    data['downloadLocation'] = str(Path.home() / "Downloads")
                root.destroy()
            except:
                print('Invalid Option')
                break
        print('--------------------------------------------------------')

def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)

main()

    


