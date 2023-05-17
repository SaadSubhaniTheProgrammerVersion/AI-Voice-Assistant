from __future__ import print_function
import math
import webbrowser
import random
import os
import datetime
from pygame import mixer  # Load the popular external library
import time
from tkinter import Tk, PhotoImage
import speech_recognition as sr
import subprocess
import pyautogui as pg
from PIL import ImageTk
import pyttsx3
from tkinter import *
from tkinter import messagebox
import pyautogui
import requests
import openai

#global voice settings
voice_variable= 1
first_listen= TRUE
name=""
Chat_GPT= TRUE
engine = pyttsx3.init()
voice = engine.getProperty('voices') #get the available voices
engine.setProperty('voice', voice[voice_variable].id) #changing voice to index 1 for female voice

def speak(text):
    global voice_variable
    global name
    if(voice_variable==1):
        name="Olivia"
    elif(voice_variable==0):
        name="Harry"
    engine.say(text)
    engine.runAndWait()
    print(f"{name}: {text}")  # print what app said


def welcome():
    import imageio
    from tkinter import Tk, Label
    from PIL import ImageTk, Image
    from pathlib import Path
    # video_name = str(Path().absolute()) + '/../wal.mp4'
    # video = imageio.get_reader(video_name)
    # delay = int(1000 / video.get_meta_data()['fps'])

    # def stream(label):
    #     try:
    #         image = video.get_next_data()
    #     except:
    #         video.close()
    #         return
    #     label.after(delay, lambda: stream(label))
    #     frame_image = ImageTk.PhotoImage(Image.fromarray(image))
    #     label.config(image=frame_image)
    #     label.image = frame_image

    if __name__ == '__main__':
        root = Tk()
        root.title("Welcome")
        mixer.init()
        mixer.music.load('AudioUsed\welcomeaudio.mp3')
        mixer.music.play()
        my_label = Label(root)
        my_label.pack()
        # my_label.after(delay, lambda: stream(my_label))
        root.after(8000, root.destroy)  # milliseconds
        root.mainloop()




def get_audio():
    mixer.init()
    mixer.music.load('AudioUsed\Mic2.mp3')
    mixer.music.play()
    r = sr.Recognizer()
    with sr.Microphone() as source:           

        audio = r.listen(source)
        said = ""

        try:
            said = r.recognize_google(audio)
            print(said)
        except Exception as e:
            speak("Sorry I could not understand. Can you please repeat")
            text=get_audio()
            return text

    return said.lower()


def success():
    def help():
        mixer.init()
        mixer.music.load('AudioUsed\Mouse.mp3')
        mixer.music.play()
        time.sleep(1)
        speak("Click on the Listen button to give me orders. Here is a list of things I can perform for you")
        messagebox.showinfo("List of Things I can do", "I can perform the following tasks for you:\n"
                                                        "1. Open Windows Apps\n"
                                                        "2. Perform Calculations\n"
                                                        "3. Check Weather\n"
                                                        "4. Play a song on Spotify\n"
                                                        "5. Search on Google\n"
                                                        "6. Search on Youtube\n"
                                                        "7. Play Voice Controlled Games\n"
                                                        "8. Change my voice\n")

    def quit():
        mixer.init()
        mixer.music.load('AudioUsed\Mouse.mp3')
        mixer.music.play()
        time.sleep(1)
        import tkinter as tk
        speak("Are you sure you want to exit the application?")
        MsgBox = tk.messagebox.askquestion('Exit Application', 'Are you sure you want to exit?',
                                           icon='warning')
        if MsgBox == 'yes':
            mixer.init()
            mixer.music.load('AudioUsed\Mouse.mp3')
            mixer.music.play()
            time.sleep(1)
            mixer.init()
            mixer.music.load('AudioUsed\Bye.mp3')
            mixer.music.play()
            time.sleep(1)
            speak("See you again!")
            root.destroy()
            exit()
        else:
            mixer.init()
            mixer.music.load('AudioUsed\Mouse.mp3')
            mixer.music.play()
            time.sleep(1)
            speak("returning back!")
            tk.messagebox.showinfo('Return', 'Going back to the app!')

    def startgame():
        Button(root, text="LISTEN", bg="black", fg="yellow", font=myFont, height=3, width=18, command=Listen).place(
            x=57, y=447)
        Button(root, text="QUIT", bg="black", fg="yellow", font=myFont, height=3, width=18, command=quit).place(x=557,
                                                                                                                y=447)
        Button(root, text="HELP", bg="black", fg="yellow", font=myFont, height=3, width=18, command=help).place(x=957,
                                                                                                                  y=607)

        def activateme():
            hour = int(datetime.datetime.now().hour)
            if hour >= 0 and hour < 12:
                speak("Good Morning!")
            elif hour >= 12 and hour < 18:
                speak("Good Afternoon!")
            else:
                speak("Good Evening!")
            speak("Hey, what's up? My name is Olivia. Press the Listen button to give me orders!")

        activateme()

    def get_daily_forecast(location):
        with open('accuweatherkey.txt', 'r') as file:
            key = file.read().strip()
        api_key = key

        url = f"http://dataservice.accuweather.com/locations/v1/cities/search?q={location}&apikey={api_key}"
        response = requests.get(url)

        try:
            location_key = response.json()[0]["Key"]
        except Exception:
            speak(f"No results for {location}")
            return
        
        url = f"http://dataservice.accuweather.com/forecasts/v1/daily/1day/{location_key}?apikey={api_key}&metric=true"
        response = requests.get(url)
        forecast_info = response.json()

        # date = forecast_info["DailyForecasts"][0]["Date"]
        min_temp = forecast_info["DailyForecasts"][0]["Temperature"]["Minimum"]["Value"]
        max_temp = forecast_info["DailyForecasts"][0]["Temperature"]["Maximum"]["Value"]
        day_text = forecast_info["DailyForecasts"][0]["Day"]["IconPhrase"]
        night_text = forecast_info["DailyForecasts"][0]["Night"]["IconPhrase"]

        speak(f"Forecast for {location}:")
        speak(f"Minimum Temperature: {min_temp}°C")
        speak(f"Maximum Temperature: {max_temp}°C")
        speak(f"Daytime Weather: {day_text}")
        speak(f"Nighttime Weather: {night_text}")

    def check_stop(text):
        if "stop" in text:
            speak("Ok, I am stopping now.")
            return True
        else:
            return False
    
    def ChatGPT(prompt):
        with open('gptkey.txt', 'r') as file:
            key = file.read().strip()
        openai.api_key =key
        response = openai.Completion.create(model="text-davinci-003", prompt=prompt, temperature=1, max_tokens=256)
        response=(str(response['choices'][0]['text']).replace("\n",""))
        return response
    
    def Listen():
        global first_listen
        global Chat_GPT
        Chat_GPT=TRUE

        
        
        while True:
            def there_exists(terms):
                for term in terms:
                    if term in text:
                        return True
            

            
            if(first_listen==TRUE):
                speak("What do you want me to do?")
            
            print("Listening...")
            first_listen=FALSE
            text = get_audio().lower()
            # open notepad
            if there_exists(["open notepad"]):
                Chat_GPT=FALSE
                subprocess.Popen("notepad.exe")
                time.sleep(2)
                speak("What would you like me to note down here?")
                text = get_audio().lower()  # calling function
                pg.write(text)
                speak("I have noted it down successfully!")
            # microsoft office files
            # word
            WORD_STRS = ["open microsoft word", "open word", "microsoft word"]

            for phrase in WORD_STRS:
                if phrase in text:
                    Chat_GPT=FALSE
                    pyautogui.hotkey("winleft", "r")
                    pyautogui.typewrite("WINWORD.EXE")
                    pyautogui.press("enter")
                    time.sleep(5)
                    pg.press("enter")
                    # for writing anything down in microsoft word file
                    speak("What would you like me to note down here?")
                    text = get_audio().lower()  # calling function
                    pg.write(text)
                    speak("I have written it down successfully!")
            # powerpoint
            PPT_STRS = ["open microsoft powerpoint", "open powerpoint","powerpoint","make a presentation"]
            for phrase in PPT_STRS:
                if phrase in text:
                    Chat_GPT=FALSE
                    pyautogui.hotkey("winleft", "r")
                    pyautogui.typewrite("powerpnt.exe")
                    pyautogui.press("enter")
            CALC_STRS = ["open calculator"]
            for phrase in CALC_STRS:
                if phrase in text:
                    Chat_GPT=FALSE
                    subprocess.Popen('C:\\Windows\\System32\\calc.exe')
                    speak("I can perform addition, subtraction, multiplication and some trigonometric calculation")
                    speak("What do you want me to perform here?")
                    text = get_audio()
                    if check_stop(text):
                        return
                    # addition
                    if there_exists(["+"]):
                        last_term = text.split("+ ")[-1]
                        last_int = int(last_term)
                        first_term = text.split(" +")[+0]
                        first_int = int(first_term)
                        result = first_int + last_int
                        for x in first_term:
                            pg.press(x)
                        pg.press("+")
                        for y in last_term:
                            pg.press(y)
                        pg.press("enter")
                        speak("%s equals %d." % (text, result))
                        # subtraction
                    if there_exists(["-"]):
                        last_term = text.split("- ")[-1]
                        last_int = int(last_term)
                        first_term = text.split(" -")[+0]
                        first_int = int(first_term)
                        result = first_int - last_int
                        for x in first_term:
                            pg.press(x)
                        pg.press("-")
                        for y in last_term:
                            pg.press(y)
                        pg.press("enter")
                        speak("%d minus %d equals %d." % (first_int, last_int, result))
                        # multiplication ---> user must say "multiplied by"
                    if there_exists(["x"]):
                        last_term = text.split("x ")[-1]
                        last_int = int(last_term)
                        first_term = text.split(" x")[+0]
                        first_int = int(first_term)
                        result = first_int * last_int
                        for x in first_term:
                            pg.press(x)
                        pg.press("*")
                        for y in last_term:
                            pg.press(y)
                        pg.press("enter")
                        speak("%d multiplied by %d equals %d." % (first_int, last_int, result))
                        # trigonometry
                    if there_exists(["sin", "sign"]):
                        if there_exists("g"):
                            term = text.split("sign ")[-1]
                            term_float = float(term)
                            result = math.sin(math.radians(term_float))
                            for x in term:
                                pg.press(x)
                            pg.press("s")
                            speak("sine of %.1f is %.2f." % (term_float, result))
                        else:
                            term = text.split("sin ")[-1]
                            term_float = float(term)
                            result = math.sin(math.radians(term_float))
                            for x in term:
                                pg.press(x)
                            pg.press("s")
                            speak("sine of %.1f is %.2f." % (term_float, result))
                        # user must say "cos" and then number
                    if there_exists(["cos", "cause", "call", "cosine"]):
                        if there_exists(["cos"]):
                            term = text.split("cos ")[-1]
                            term_float = float(term)
                            result = math.cos(math.radians(term_float))
                            for x in term:
                                pg.press(x)
                            pg.press("o")
                            speak("cosine of %.1f is %.2f." % (term_float, result))
                        elif there_exists(["cause"]):
                            term = text.split("cause ")[-1]
                            term_float = float(term)
                            result = math.cos(math.radians(term_float))
                            for x in term:
                                pg.press(x)
                            pg.press("o")
                            speak("cosine of %.1f is %.2f." % (term_float, result))
                        else:
                            term = text.split("call ")[-1]
                            term_float = float(term)
                            result = math.cos(math.radians(term_float))
                            for x in term:
                                pg.press(x)
                            pg.press("o")
                            speak("cosine of %.1f is %.2f." % (term_float, result))
                        # user must say "what is tangent of" and then number. There is a certain restriction for the word "tangent"
                    if there_exists(["tangent"]):
                        if there_exists("of"):
                            term = text.split("of ")[-1]
                            term_float = float(term)
                            result = math.tan(math.radians(term_float))
                            for x in term:
                                pg.press(x)
                            pg.press("t")
                            speak("tangent of %.1f is %.2f." % (term_float, result))
                        else:
                            term = text.split("tangent ")[-1]
                            term_float = float(term)
                            result = math.tan(math.radians(term_float))
                            for x in term:
                                pg.press(x)
                            pg.press("t")
                            speak("tangent of %.1f is %.2f." % (term_float, result))
            if there_exists(["what's the time","time"]):
                Chat_GPT=FALSE
                strTime = datetime.datetime.now().strftime("%I:%M %p")
                speak(f"It is {strTime} right now")
                

            if there_exists(["what's the date","date","today"]):
                Chat_GPT=FALSE
                strDate = datetime.datetime.now().strftime("%d %B %Y")
                speak(f"Today is {strDate}")



    # type app name and wait for search result
            if there_exists(["check weather", "raining", "sunny", "rain","cloudy","weather"]):
                Chat_GPT=FALSE
                speak("Which city would you like to check the weather for?")
                text = get_audio().lower()
                if check_stop(text):
                        return
                get_daily_forecast(text)

            if there_exists(["spotify","music","open spotify","play a song","song"]):
                Chat_GPT=FALSE
                url=f"https://open.spotify.com/search"
                teb_times=0
                webbrowser.get().open(url)
                time.sleep(3)
                speak("Would you like to search for a song or an artist?")
                text = get_audio().lower()  # calling function
                if check_stop(text):
                    return

                if there_exists(["song"]):
                    tab_times=3
                    speak("What song would you like to play?")
                    text = get_audio().lower()  # calling function
                    if check_stop(text):
                        return
                elif there_exists(["artist"]):
                    tab_times=2
                    speak("What artist would you like to play?")
                    text = get_audio().lower()  # calling function
                    if check_stop(text):
                        return

                search_term = text
                pg.write(text)
                pg.press("enter")
                #enter a delay of 1 second
                time.sleep(3)
                for i in range (tab_times):
                    pg.press("tab")
                pg.press("Enter")
                speak(f'Playing {search_term} on spotify')


                    # new youtube
            if there_exists(["youtube", "open youtube","youtube.com","You tube"]):
                Chat_GPT=FALSE
                url = f"https://youtube.com"
                webbrowser.get().open(url)
                time.sleep(2)
                speak("What would you like me to search?")
                text = get_audio().lower()  # calling function
                if check_stop(text):
                    return
                search_term = text
                pg.press("tab")
                pg.press("tab")
                pg.press("tab")
                pg.press("tab")
                pg.write(text)
                time.sleep(1)
                pg.press("enter")
                speak(f'Here is what I found for {search_term} on youtube')
                # choice of videos
                speak(f'Which result would you like to watch? The first one or the second one?')
                text = get_audio().lower()
                if check_stop(text):
                    return
                # plays the first video if demanded
                PLAY_STRS = ["first"]
                for phrase in PLAY_STRS:
                    if phrase in text:
                        speak("I am playing the first search result")

                        if pyautogui.size() == (1920, 1080):
                            pyautogui.click(650,300)
                        elif pyautogui.size() == (2560, 1440):
                            pyautogui.click(800,400)

                        else:
                            speak("Sorry, I am unable to play the video. Please try again later.")
                # plays second video if demanded
                PLAYZ_STRS = ["second"]
                for phrase in PLAYZ_STRS:
                    if phrase in text:
                        speak("I am playing the second search result")
                        if pyautogui.size() == (1920, 1080):
                            pyautogui.click(700,600)
                        elif pyautogui.size() == (2560, 1440):
                            pyautogui.click(900,750)
                        else:
                            pg.press("enter")
                            pg.press("tab")
                            pg.press("tab")
                            pg.press("tab")
                            pg.press("tab")
                            pg.press("enter")

            if there_exists(["what is your name","your name"]):
                global name
                speak("My name is " + name + " and I am your personal assistant")
                Listen()
            # 5: search google
            if there_exists(["google","search on the internet","look up on the internet","internet","search"]):
                Chat_GPT=FALSE
                url = f"https://google.com"
                webbrowser.get().open(url)
                speak("What would you like me to search?")
                text = get_audio().lower()  # calling function
                if check_stop(text):
                    return
                search_term = text
                pg.write(text)
                pg.press("enter")
                speak(f'Here is what I found for {search_term} on google')
           
            if there_exists(["change voice","switch voice","change to male voice","male voice","change assistant voice","male voice"]):
                Chat_GPT=FALSE
                global voice_variable
                voice_variable= int(not(voice_variable))
                engine = pyttsx3.init()
                voice = engine.getProperty('voices') #get the available voices
                engine.setProperty('voice', voice[voice_variable].id) #changing voice to index 1 for female voice 0 for male
                first_listen= TRUE
                Listen()

            if there_exists(["instagram","insta","open instagram","instagram.com"]):
                Chat_GPT=FALSE
                url = f"https://instagram.com"
                webbrowser.get().open(url)

            if there_exists(["facebook","fb","open facebook","facebook.com"]):
                Chat_GPT=FALSE
                url = f"https://facebook.com"
                webbrowser.get().open(url)

            if there_exists(["open an application","appliction","app"]):
                Chat_GPT=FALSE
                speak("Which application would you like to open?")
                text = get_audio().lower()
                if check_stop(text):
                    return
                pyautogui.press('win')
                time.sleep(1)
                pyautogui.write(text)
                time.sleep(1.5)
                pyautogui.press('enter')

            if there_exists(["launch"]):
                Chat_GPT=FALSE
                last_term = text.split("launch ")[-1]
                if(last_term=='launch'):
                    speak("Sorry I could not understand")
                    return
                speak(f"Launching {last_term}")
                pyautogui.press('win')
                time.sleep(1)
                pyautogui.write(last_term)
                time.sleep(1.5)
                pyautogui.press('enter')


            GAME_STRS = ["game","play","games","games"]
            for phrase in GAME_STRS:
                if phrase in text:
                    Chat_GPT=FALSE
                    speak("We can play the guessing number game. Would you like to play?")
                    text = get_audio().lower()
                    if check_stop(text):
                        return
                    if there_exists(["yes","let's play","game","sure"]):
                        hidden = random.randrange(10, 30)
                        lives = 5
                        speak("We will now play a guessing number game.")
                        speak("guess a number from 10 to 30")
                        while (lives > 0):
                            if lives == 1:
                                speak("You have %d life left." % (lives))  # for one life
                                print("You have %d life left." % (lives))
                            else:
                                speak("you have %d lives left." % (lives))  # for lives>1
                                print("You have %d life left." % (lives))
                            print("Guess now...")
                            text = get_audio()
                            if text.isdigit():
                                guess = int(text)
                                if guess == hidden:
                                    print("Congratulations! You have guessed it")
                                    speak("Congratulations! You have guessed it")
                                    break
                                else:
                                    if guess > hidden:
                                        speak("Sorry, my number is smaller than %s." % guess)
                                        lives = lives - 1
                                    if guess < hidden:
                                        speak("Sorry, my number is greater than %s." % guess)
                                        lives = lives - 1
                                if lives == 0 and guess != hidden:
                                    print("You have lost the game!")
                                    speak("You have lost the game!")
                            else:
                                speak("Please respond with a number only")
                                lives = lives - 1
                                if lives == 0:
                                    print("You have lost the game!")
                                    speak("You have lost the game!")

            if Chat_GPT==TRUE:
                        prompt = text
                        speak(f"Searching the Web for {text}")
                        response = ChatGPT(prompt)
                        speak(response)
                    
                    

            EXIT_STRS = ["exit", "quit", "go offline"]
            for phrase in EXIT_STRS:
                if phrase in text:
                    mixer.init()
                    mixer.music.load('AudioUsed\Bye.mp3')
                    mixer.music.play()
                    time.sleep(1)
                    speak("See you again!")
                    exit()
            break

            

    def button():
        Button(root, text="CONTINUE", bg="black", fg="yellow", font=myFont, height=2, width=15, command=cont).place(
            x=415, y=329)
        speak("click on the continue button to proceed further!")

    def cont():
        mixer.init()
        mixer.music.load('AudioUsed\Mouse.mp3')
        mixer.music.play()
        time.sleep(1)
        root.destroy()

    # root = Tk()
    # root.title("Introduction")
    # label1 = Label(root, )
    # C = Canvas(root, bg="blue", height=450, width=500)
    # filename = PhotoImage(file="ImagesUsed\down.png")
    # background_label = Label(root, image=filename)
    # background_label.place(x=0, y=0, relwidth=1, relheight=1)
    # C.pack()
    # root.geometry("1024x707")
    # topFrame = Frame(root)
    # topFrame.pack()
    # bottomFrame = Frame(root)
    # bottomFrame.pack(side=BOTTOM)
    import tkinter.font as font
    # myFont = font.Font(weight="bold")
    # root.after(5000, button)
    # root.mainloop()
    root = Tk()
    root.title("Voice Recognition App")
    label1 = Label(root, )
    C = Canvas(root, bg="blue", height=450, width=500)
    filename = PhotoImage(file="ImagesUsed\Robot.png")
    background_label = Label(root, image=filename)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    C.pack()
    root.geometry("1200x800")
    topFrame = Frame(root)
    topFrame.pack()
    bottomFrame = Frame(root)
    bottomFrame.pack(side=BOTTOM)
    import tkinter.font as font
    myFont = font.Font(weight="bold")
    Button(root, text="ACTIVATE ME", bg="black", fg="yellow", font=myFont, height=3, width=18, command=startgame).place(
        x=304, y=147)

    root.mainloop()


# def Ok():
#     uname = e1.get()
#     password = e2.get()
#     if (uname == "" and password == ""):
#         speak("Blank input")
#         messagebox.showinfo("", "Invalid Input")
#     elif (uname == "Saad" and password == "123"):
#         mixer.init()
#         mixer.music.load('AudioUsed\Mouse.mp3')
#         mixer.music.play()
#         messagebox.showinfo("", "Login Success")
#         speak("Welcome")
#         root.destroy()

#         welcome()
#         success()
#     else:
#         speak("Incorrect credentials!")
#         messagebox.showinfo("", "Incorrent Username and/or Password")


# root = Tk()
# C = Canvas(root, bg="blue", height=450, width=500)
# filename = PhotoImage(file="ImagesUsed\lock.png")
# background_label = Label(root, image=filename)
# background_label.place(x=0, y=0, relwidth=1, relheight=1)
# C.pack()
# root.title("Login")
# root.geometry("450x450")
# global e1
# global e2
# Label(root, text="UserName", bg="black", fg="yellow").place(x=70, y=370)
# Label(root, text="Password", bg="black", fg="yellow").place(x=70, y=400)
# e1 = Entry(root)
# e1.place(x=140, y=370)
# e2 = Entry(root)
# e2.place(x=140, y=400)
# e2.config(show="*")
# Button(root, text="Login", command=Ok, height=3, width=13).place(x=300, y=367)
# speak("Please Enter your username and Password")
# welcome()
success()
# root.mainloop()
