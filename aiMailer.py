import pyttsx3 #library for text to speech 
import datetime # module to get time for greetings and wish
import speech_recognition as sr # to identify the audio input from the user
import smtplib 
from email.message import EmailMessage
from tkinter import* 
from tkinter import simpledialog
import re
import os 
userName = os.environ.get('Email')
passWord= os.environ.get('PASSWORD')

 
engine =  pyttsx3.init('sapi5') # pyttsx3.init() factory function to get a reference to a pyttsx3. 
#sapi5 is one of the TTS(text to speech ) engine in pyttsx3 
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[0].id)
#let's create the speak function 

#to respond to user 
def speak(audio):
    engine.say(audio)
    engine.runAndWait() #to make audio audible in the system

# for general etiquettes
def wishMe():
    hour = (datetime.datetime.now().hour) #typcasting of hour in integers 
    if(hour>=0 and hour <12):
        speak("Good Morning sir")
    elif hour >=12 and hour <=14:
        speak("Good Afternoon sir")
    elif hour >14 and hour <=18:
        speak("Good everning sir")
    elif hour >18 and hour <20:
        speak("Hello Sir ")
    elif hour >=20 and hour <=24:
        speak("Good Night sir")
    #assistant introducing itself
    speak("how can I help you, Sir?")
def listenCommand():
    r= sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening")
        r.pause_threshold=1
        r.energy_threshold=400
        audio= r.listen(source)

    try:
        print("Analyzing your command....")
        query= r.recognize_google(audio, language='en-in')
        print("You Said ", query )

    except Exception as e:
        # print(e)
        print("Please repeat your Command..")
        return "None"
    return query



#taking email as input from tkinter GUI 
def takeEmail():
    screen=  Tk()
    screen.withdraw()
    email_input= simpledialog.askstring(title= "Email input field", prompt="Enter Reciever's Email ID") 
    if (validateEmail(email_input)):
        ans= email_input 
    else:
        speak("Invalid email, try again")
        exit()
    return ans

#validating email 
def validateEmail(id): 
    pattern= r"^[a-zA-Z0-9.%-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$" #creating regular expresion 
    if re.match(pattern, id):
        return True
    return False



#sending mail using smtp with TLS security layer
def sendEmail(to, subject,  content):
    em= EmailMessage()
    em['From']=userName
    em['To']= to
    em['Subject']=subject
    em.set_content(content)
     
    server = smtplib.SMTP("smtp.gmail.com", 587 )
     
    server.starttls() #establishing secure connection with TLS which is more secure version of SSL
    server.login(userName, passWord)
    server.sendmail(userName, to, em.as_string())
    server.close()


    
   
   



 
if __name__=="__main__":
   wishMe()
#    takeEmail()
   query= listenCommand().lower() 
   #logic for the tasks, identification of tasks and performance 
   if 1:
    if "send email" in query:
        try:
            speak("who is the reciever?")
            to= takeEmail()
            speak("what is your Subject")
            subject = listenCommand()
            speak("What should I write in mail?")
            content = listenCommand()
            sendEmail(to , subject, content)
            speak("Your Email has been sent")
        except Exception as e:
            print("Sorry, unable to send. Please try latter") 
             


   