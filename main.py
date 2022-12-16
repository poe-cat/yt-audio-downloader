from tkinter import *
from tkinter import ttk
from pytube import YouTube
from tkinter.messagebox import showinfo, showerror, askokcancel
import threading
import os

def close_window():
    if askokcancel(title='Close Application', message='Do you want to close mp3 downloader?'):
        window.destroy()
def download_audio():

    mp3_link = url_entry.get()
    if mp3_link == '':
        showerror(title='Error', message='Please enter the mp3 URL')
    else:
        try:
            def on_progress(stream, chunk, bytes_remaining):
                total_size = stream.filesize

                def get_formatted_size(total_size, factor=1024, suffix='B'):
                    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
                        if total_size < factor:
                            return f"{total_size:.2f}{unit}{suffix}"
                        total_size /= factor
                    return f"{total_size:.2f}Y{suffix}"

                formatted_size = get_formatted_size(total_size)
                bytes_downloaded = total_size - bytes_remaining
                percentage_completed = round(bytes_downloaded / total_size * 100)
                progress_bar['value'] = percentage_completed
                progress_label.config(text=str(percentage_completed) + '%, File size:' + formatted_size)
                window.update()

            audio = YouTube(mp3_link, on_progress_callback=on_progress)
            output = audio.streams.get_audio_only().download()
            base, ext = os.path.splitext(output)
            new_file = base + '.mp3'
            os.rename(output, new_file)

            showinfo(title='Download complete', message='mp3 has been downloaded successfully.')

            progress_label.config(text='')
            progress_bar['value'] = 0

        except:
            showerror(title='Download Error',
                      message='An error occurred while trying to ' \
                            'download the MP3\nThe following could ' \
                            'be the causes:\n-> Invalid link\n-> No internet connection\n' \
                            'Make sure you have stable internet connection and the mp3 link is valid')

            progress_label.config(text='')
            progress_bar['value'] = 0

def downloadThread():
    t1 = threading.Thread(target=download_audio)
    t1.start()

window = Tk()

window.protocol('WM_DELETE_WINDOW', close_window)

window.title('MP3 Downloader')

window.iconbitmap(window, 'icon.ico')

window.geometry('500x400+430+180')
window.resizable(height=FALSE, width=FALSE)

canvas = Canvas(window, width=500, height=400)
canvas.pack()

"""Styles for the widgets"""
label_style = ttk.Style()
label_style.configure('TLabel', foreground='#000000', font=('OCR A Extended', 15))

entry_style = ttk.Style()
entry_style.configure('TEntry', font=('Dotum', 15))

button_style = ttk.Style()
button_style.configure('TButton', foreground='#000000', font='DotumChe')

logo = PhotoImage(file='mp3_icon.png')
logo = logo.subsample(2, 2)
canvas.create_image(180, 80, image=logo)

mp3_label = ttk.Label(window, text='Downloader', style='TLabel')
canvas.create_window(340, 125, window=mp3_label)

url_label = ttk.Label(window, text='Enter MP3 URL:', style='TLabel')
url_entry = ttk.Entry(window, width=72, style='TEntry')

canvas.create_window(114, 200, window=url_label)
canvas.create_window(250, 230, window=url_entry)

progress_label = Label(window, text='')
canvas.create_window(240, 280, window=progress_label)

progress_bar = ttk.Progressbar(window, orient=HORIZONTAL, length=450, mode='determinate')
canvas.create_window(250, 300, window=progress_bar)

download_button = ttk.Button(window, text='Download MP3', style='TButton', command=downloadThread)
canvas.create_window(240, 330, window=download_button)

window.mainloop()