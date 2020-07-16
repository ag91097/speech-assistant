import pyttsx3                         # pip install pyttsx3
import speech_recognition as sr        # pip install speechRecognition
import datetime
import wikipedia                       # pip install wikipedia
from pygame import mixer               # pip install --user pygame
import webbrowser
import os
import time
import requests
import config

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print(voices)
# print(voices[0].id)
engine.setProperty('voice', voices[0].id)

#  FUNCTIION THAT WILL SPEAK THE PASSED TEXT
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

# FUNCTION TO WISH AS PROGRAMS STARTS.
def welcome():

    hour =  int(datetime.datetime.now().hour)
   
    if(hour>=0 and hour<12):
        speak("Good Morning!")

    elif(hour>=12 and hour<18):
        speak("Good Afternoon!")

    else:
        speak("Good Evening!")

    time.sleep(2)
    speak("Please tell how may I help you?")

# FUNCTION TO TAKE SPEECH COMMANDS FROM MICROPHONE
def takeCommand():
    # take input from microphone and returns string output
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening....")
        r.pause_threshold = 1
        audio = r.listen(source)
    
    try:
        print("Recognizing.....")
        query = r.recognize_google(audio, language='en-in')
        # print("User said: ", query)
        print(f"User said: {query}\n")
        time.sleep(2)

    except Exception as e:
        print(e)
        print("Sorry , say that again please..")
        time.sleep(1)
        return ""
    
    return query


# file-> file which I am going to play as a reminder
# fileStopcode-> command that I have to speak/write to stop that file.  
def remindMe(file, fileStopcode):
    mixer.init()
    mixer.music.load(file)
    mixer.music.play(-1)       # -1: to play file indefinitely. 
    while True:
        # inputStopcode = input(f"enter {fileStopcode} to stop sound\n")
        inputStopcode = takeCommand().lower()
        if fileStopcode in inputStopcode:
            mixer.music.stop()
            break

def log_now(entries):
    # I will enter all the logs inside a file.
    with open("mylogs.txt", "a") as f:  
        # along with the message. I am mentioning the (timestamp) date and time using datetime module.
        f.write(f"{entries} {datetime.datetime.now()}\n")

def todoRead():
    f = open("todo.txt", "r")
    isPresent = False
    for line in f:
        isPresent = True
        print(line)
        speak(line)
    f.close()
    if isPresent == False:
        speak("You have no notes added yet.")

def todoWrite():
    f = open("todo.txt", "a")
    newReminder = ""
    while newReminder == "":
            speak("What should I add for you?")
            newReminder = takeCommand()
            if "nothing" in newReminder or "go back" in newReminder:
                f.close()
                speak("No note added this time.")
                return
    f.write(f"\n{newReminder}")
    f.close()
    speak("Note successfully added")

def givenews():
    url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={config.apiKey_news}"
    response = requests.get(url)
    data = response.json()
    data = data["articles"]
    flag = True
    count = 0
    for items in data:
        count += 1
        if count > 10:
            break
        print(items["title"])
        to_speak = items["title"].split(" - ")[0]
        if flag:
            speak("Today's top ten Headline are : ")
            flag = False
        else:
            speak("Next news :")
        speak(to_speak)

def giveWeather():
    speak("Tell me a city name")
    city = ""
    while city is "":
        city = takeCommand().lower()
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={config.apiKey_weather}"
    response = requests.get(url)
    data = response.json()
    print(city)
    if data['cod'] == str(404):
        speak("Could not found any data")
        giveWeather()
    else:    
        temperature = data['main']['temp']
        humidity = data['main']['humidity']
        weather = data['weather'][0]['description']
        speak(f"Current temperature in {city} is {temperature} degree celcius")
        speak(f"Current humidity in {city} is {humidity} percent")
        speak(f"Current weather in {city} is {weather}")


# MAIN PROGRAM 
def main():
    # Wish user function
    welcome()

    # Variables for Healthy Programmer Concept
    init_water = time.time()
    init_eyes  = time.time()
    init_activity = time.time()
    # Variables holding time duration to remind user for each task.
    waterDuration = 45*60
    eyesDuration =  30*60
    activityDuration = 60*60
    stopReminder = 'completed'

    while True:

        # Logic for healty programmer.
        if time.time() - init_water > waterDuration:
            print(f"Time to drink water. Speak {stopReminder} to stop reminder")
            remindMe('water.mp3', stopReminder)
            init_water = time.time()
            log_now('Drank water at')
              
        if time.time() - init_eyes > eyesDuration:
            print(f"Time for eye relaxation. Speak {stopReminder} to stop alarm")
            remindMe('eyes.mp3', stopReminder)
            init_eyes = time.time()
            log_now('Eyes exercise done at')

        if time.time() - init_activity > activityDuration:
            print(f"Time to do some activity. Speak {stopReminder} to stop alarm")
            remindMe('activity.mp3', stopReminder)
            init_activity = time.time()
            log_now('Physical activity done at')

        # Getting a string query, after my command is recognized.
        query = takeCommand().lower()
        
        # Logic for executing tasks based on query

        if 'wikipedia' in query:
            speak("Searching Wikipedia...")
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences = 2)
            speak("According to wikipedia")
            print(results)
            speak(results)
        
        elif 'open youtube' in query:
            url = "youtube.com"
            chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
            webbrowser.get(chrome_path).open(url)
        
        elif 'open google' in query:
            url = "google.com"
            chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
            webbrowser.get(chrome_path).open(url)
             
        elif 'search' in query:
            speak("What do you want to search?")
            search_term = takeCommand()
            url = f"https://google.com/search?q={search_term}"
            chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
            webbrowser.get(chrome_path).open(url)
            speak(f"Here's something I have found for {search_term} on google")

        elif 'location' in query:
            speak("What do you want to search?")
            search_term = takeCommand()
            url = f"https://google.nl/maps/place/{search_term}/&amp;"
            chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
            webbrowser.get(chrome_path).open(url)
            speak(f"Here is the location of {search_term}")
            

        elif 'play music' in query:
            music_dir = 'G:\\Audio\\VOICE'
            songs = os.listdir(music_dir)
            print(songs)
            os.startfile(os.path.join(music_dir, songs[0]))
        
        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir the time is {strTime}")

        elif 'open chrome' in query:
            chromePath = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
            os.startfile(chromePath)

        elif 'headlines' in query or 'news' in query or 'headline' in query:
            givenews()
        
        elif 'quit' in query or 'exit' in query or 'close' in query or 'bye' in query:
            speak("Have a good day, going offline")
            exit()
        
        elif 'todo' in query or 'note' in query or 'notes' in query:
            question = "Do you want to read notes or create new notes?"
            speak(question)
            answer = takeCommand().lower()
            if 'create' in answer or 'new' in answer:
                todoWrite()
            else:
                speak("Searching for the notes")
                todoRead()
        
        elif 'weather' in query or 'temperature' in query:
            giveWeather()


if __name__ == "__main__":
    main()