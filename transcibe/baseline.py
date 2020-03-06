import speech_recognition as sr
import datetime

r = sr.Recognizer()

class baseline:
    def __init__(self, key):        
        print("\nbaseline...")
        self.key= key

    def read(self): # update audio to mdeia
        print("readMedia")

        audiofile = sr.AudioFile( "media/" + self.key )

        with audiofile as source:
            audio = r.record(source)

        return audio

    #   transcribe 
    def text(self):
        print("transcribe")

        t1= datetime.datetime.now()
        audio= self.read()

        text=""
        try:
            text= r.recognize_google(audio)
        except:
            print("recognize_google could not recognize")

        t2=  datetime.datetime.now()
        t21 = str( round((t2 - t1).total_seconds(), 2) ) + 's'
        print( t21 )

        print("*********************** baseline text ***********************")
        print(text)
        print("********************************************************")


        return text, t21



if __name__== "__main__":
    filename= 'media/test1.wav'
    text= speech2text(filename)
    
    microphone()

    print("done")