from pytube import YouTube

def Download(link):
    youtubeObject = YouTube(link)
    youtubeObject = youtubeObject.streams.get_highest_resolution()
    try:
        youtubeObject.download()
    except:
        print("Error while downloading")
        print("Completed")

link = input("Paste YT video link here: ")
Download(link)
