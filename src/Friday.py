import pyttsx3
import speech_recognition as sr
from datetime import date
import time
import webbrowser
import datetime
from pynput.keyboard import Key, Controller
import pyautogui
import sys
import subprocess
import os
from os import listdir
from os.path import isfile, join
import smtplib
import wikipedia
import Gesture_Controller
#import Gesture_Controller_Gloved as Gesture_Controller
import app
from threading import Thread

# -------------Object Initialization---------------
today = date.today()
r = sr.Recognizer()
keyboard = Controller()
engine = pyttsx3.init('sapi5')
engine = pyttsx3.init()
voices = engine.getProperty('voices')
# Configure for female voice
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 170)    # Speed of speech
engine.setProperty('volume', 1.0)  # Volume level

# ----------------Variables------------------------
file_exp_status = False
files = []
path = ''
is_awake = True  # Bot status

# ------------------Functions----------------------
def reply(audio):
    app.ChatBot.addAppMsg(audio)
    print(audio)
    engine.say(audio)
    engine.runAndWait()

def wish():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        reply("Good Morning!")
    elif hour >= 12 and hour < 18:
        reply("Good Afternoon!")
    else:
        reply("Good Evening!")
    reply("Heyy my name is Friday!, how may I help you?")

# Set Microphone parameters
with sr.Microphone() as source:
    r.energy_threshold = 500
    r.dynamic_energy_threshold = False

# Audio to String
def record_audio():
    with sr.Microphone() as source:
        r.pause_threshold = 0.8
        voice_data = ''
        audio = r.listen(source, phrase_time_limit=5)

        try:
            voice_data = r.recognize_google(audio)
        except sr.RequestError:
            reply('Sorry, my service is down. Please check your internet connection.')
        except sr.UnknownValueError:
            print('Cannot recognize the command.')
            pass
        return voice_data.lower()

# Executes Commands (input: string)
def respond(voice_data):
    global file_exp_status, files, is_awake, path
    print(voice_data)
    voice_data = voice_data.replace('friday', '').strip()
    app.eel.addUserMsg(voice_data)

    if not is_awake:
        if 'wake up' in voice_data:
            is_awake = True
            wish()
    elif 'close this tab' in voice_data:
        try:
            with keyboard.pressed(Key.ctrl):
                keyboard.press('w')
                keyboard.release('w')
            reply('The tab has been closed.')
        except:
            reply('I encountered an error while trying to close the tab Please help me.')

    # STATIC CONTROLS
    elif 'hello' in voice_data:
        wish()

    elif 'what is your name' in voice_data:
        reply('My name is Friiday!')

    elif 'date' in voice_data:
        reply(today.strftime("%B %d, %Y"))

    elif 'time' in voice_data:
        reply(str(datetime.datetime.now()).split(" ")[1].split('.')[0])

    elif 'open my insta' in voice_data:
        reply('Opening Instagram')
        webbrowser.open('https://www.instagram.com')

    elif 'open my facebook' in voice_data:
        reply('Opening Facebook')
        webbrowser.open('https://www.facebook.com')
    
    elif 'open paint' in voice_data:
        reply('Opening Paint')
        try:
            # Using the built-in Paint application path in Windows
            os.startfile('mspaint')
        except:
        # Alternative method using subprocess
            subprocess.Popen('mspaint')
    elif 'close paint' in voice_data:
        reply('Closing Paint')
        try:
        # Using taskkill to close Paint
            subprocess.run('taskkill /f /im mspaint.exe', shell=True)
        except:
           reply('Paint is not running or could not be closed')


    elif 'search' in voice_data:
        search_query = voice_data.replace('search', '').strip()
        if search_query:
            reply(f'Searching for {search_query}')
            url = f'https://google.com/search?q={search_query}'
            try:
                webbrowser.get().open(url)
                reply('Here is what I found.')
            except:
                reply('Hey!,Please check your internet connection.')
        else:
            reply('What would you like me to search for?')

    elif 'location' in voice_data:
        reply('Sir Which place are you looking for?')
        temp_audio = record_audio()
        app.eel.addUserMsg(temp_audio)
        reply('Locating...')
        url = f'https://google.nl/maps/place/{temp_audio}/&amp;'
        try:
            webbrowser.get().open(url)
            reply('Look! ,This is what I found.')
        except:
            reply('Hey , Please check your internet connection.')

    elif ('bye' in voice_data) or ('by' in voice_data):
        reply("Goodbye Sir! Have a nice day.")
        is_awake = False

    elif ('exit' in voice_data) or ('terminate' in voice_data):
        if Gesture_Controller.GestureController.gc_mode:
            Gesture_Controller.GestureController.gc_mode = 0
        app.ChatBot.close()
        sys.exit()

    # DYNAMIC CONTROLS
    elif 'launch gesture recognition' in voice_data:
        if Gesture_Controller.GestureController.gc_mode:
            reply('Gesture recognition is already active.')
        else:
            gc = Gesture_Controller.GestureController()
            t = Thread(target=gc.start)
            t.start()
            reply('Launched successfully.')

    elif ('stop gesture recognition' in voice_data) or ('top gesture recognition' in voice_data):
        if Gesture_Controller.GestureController.gc_mode:
            Gesture_Controller.GestureController.gc_mode = 0
            reply('Gesture recognition stopped.')
        else:
            reply('Gesture recognition is already inactive.')

    elif 'copy' in voice_data:
        with keyboard.pressed(Key.ctrl):
            keyboard.press('c')
            keyboard.release('c')
        reply('Copied.')

    elif 'paste' in voice_data:
        with keyboard.pressed(Key.ctrl):
            keyboard.press('v')
            keyboard.release('v')
        reply('Pasted.')

    # File Navigation (Default Folder set to C://)
    elif 'list' in voice_data:
        counter = 0
        path = 'C://'
        files = listdir(path)
        filestr = ""
        for f in files:
            counter += 1
            print(f"{counter}:  {f}")
            filestr += f"{counter}:  {f}<br>"
        file_exp_status = True
        reply('These are the files in your root directory.')
        app.ChatBot.addAppMsg(filestr)

    elif file_exp_status:
        counter = 0
        if 'open' in voice_data:
            if isfile(join(path, files[int(voice_data.split(' ')[-1]) - 1])):
                os.startfile(path + files[int(voice_data.split(' ')[-1]) - 1])
                file_exp_status = False
            else:
                try:
                    path = path + files[int(voice_data.split(' ')[-1]) - 1] + '//'
                    files = listdir(path)
                    filestr = ""
                    for f in files:
                        counter += 1
                        filestr += f"{counter}:  {f}<br>"
                        print(f"{counter}:  {f}")
                    reply('Opened successfully.')
                    app.ChatBot.addAppMsg(filestr)

                except:
                    reply('You do not have permission to access this folder.')

        if 'back' in voice_data:
            filestr = ""
            if path == 'C://':
                reply('Sorry, this is the root directory.')
            else:
                a = path.split('//')[:-2]
                path = '//'.join(a)
                path += '//'
                files = listdir(path)
                for f in files:
                    counter += 1
                    filestr += f"{counter}:  {f}<br>"
                    print(f"{counter}:  {f}")
                reply('Okay.')
                app.ChatBot.addAppMsg(filestr)

    else:
        reply('I am not programmed to handle this request.')

# ------------------Driver Code--------------------

# Add voice diagnostic function to list available voices
def list_available_voices():
    print("Available voices:")
    print("------------------------")
    for idx, voice in enumerate(voices):
        print(f"Voice {idx}:")
        print(f" - ID: {voice.id}")
        print(f" - Name: {voice.name}")
        print(f" - Languages: {voice.languages}")
        print(f" - Gender: {voice.gender}")
        print("------------------------")

# Uncomment the following line to see available voices
# list_available_voices()

t1 = Thread(target=app.ChatBot.start)
t1.start()

# Lock main thread until Chatbot has started
while not app.ChatBot.started:
    time.sleep(0.5)

wish()
voice_data = None
while True:
    if app.ChatBot.isUserInput():
        # Take input from GUI
        voice_data = app.ChatBot.popUserInput()
    else:
        # Take input from Voice
        voice_data = record_audio()

    # Process voice_data
    if 'friday' in voice_data:
        try:
            # Handle sys.exit()
            respond(voice_data)
        except SystemExit:
            reply("okay byeee")
            break
        except Exception as e:
            print(f"EXCEPTION raised while closing: {e}")
            break