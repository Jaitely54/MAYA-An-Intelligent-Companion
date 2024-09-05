import os
import pygame
import speech_recognition as sr
 

def speak(data):
    voice = 'en-US-AvaNeural'
    command = f'edge-tts --voice "{voice}" --text "{data}" --write-media "data.mp3"'
    os.system(command)

    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load("data.mp3")
    try:
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

    except Exception as e:
        print(e)
    finally:
        pygame.mixer.music.stop()
        pygame.mixer.quit()

def takecmd():
    """
    This function initializes a speech-to-text using the speech_recognition library.

    It uses the microphone to capture audio and recognizes the spoken command using the Google Speech Recognition API.

    Returns:
        str: The recognized speech command if successful, otherwise None.
    """

    # Create a recognizer object
    r = sr.Recognizer()

    # Use the microphone as the audio source
    with sr.Microphone() as src:
        print("Aura: Awaiting for command...")

        # Set the pause threshold to 2 seconds
        r.pause_threshold = 2

        # Set the energy threshold to 300
        r.energy_threshold = 300

        # Listen for the user's input for a maximum duration of 4 seconds
        audio = r.listen(src, 0, 4)

    try:
        print("Understanding...")

        # Recognize the speech using Google Speech Recognition
        # The recognized speech is in the 'en-in' language
        query = r.recognize_google(audio, language="en-in")

        print(f"User: {query}\n")
    except Exception as e:
        print("Aura: Aayien!! ?")
        return "None"

    return query


if __name__ == "__main__":
    speak("Hello, my name is Maya. How can I help you?")

    while True:
        # query = takecmd().lower()
        query = "hello Maya, how are you"


        if "hello" in query:
            speak("hey Jaitely, its a new day and I am here to help you.")
