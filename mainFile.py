from gtts import gTTS
import random
from playsound import playsound
import speech_recognition as sr
import os


# create recognizer and mic instances
recognizer = sr.Recognizer()
microphone = sr.Microphone()


def respondHelper(keyword):
    prefile = "responsetextfiles/"
    if keyword == "special":
        f = open(prefile + "sassy.txt")
        linenum = random.randint(0, 4)
    elif keyword == "hello":
        f = open(prefile + "greeting.txt")
        linenum = random.randint(0, 11)
    else:
        print("well, the keywords weren't chosen")
        return

    for i, line in enumerate(f):
        if i == linenum:
            return line
        elif i > linenum:
            break
    f.close()


def listeningNow(microphone, recognizer):
    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    # let's have a listen
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    print("Say something")
    try:
        googleGuess = recognizer.recognize_google(audio)
        print("Did you say: " + googleGuess)
    except sr.RequestError:
        # API was unreachable or unresponsive
        print("API unavailable")
        googleGuess = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        print("Sorry, I couldn't understand that")
        googleGuess = "Sorry, I couldn't understand that"
    return str(googleGuess)


def recognize_speech_from_mic(recognizer, microphone):
    """Transcribe speech from recorded from `microphone`.

    Returns a dictionary with three keys:
    "success": a boolean indicating whether or not the API request was
               successful
    "error":   `None` if no error occured, otherwise a string containing
               an error message if the API could not be reached or
               speech was unrecognizable
    "transcription": `None` if speech could not be transcribed,
               otherwise a string containing the transcribed text
    """
    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    # adjust the recognizer sensitivity to ambient noise and record audio
    # from the microphone
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    # set up the response object
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    # try recognizing the speech in the recording
    # if a RequestError or UnknownValueError exception is caught,
    #     update the response object accordingly
    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    return response


def respond(keyword):
    # here is where we respond
    # we get the phrase from the respondHelper function, passing in the keyword (i.e. "hello")
    phrase = respondHelper(keyword)
    tts = gTTS(phrase, 'en')

    # For whatever reason, running the program multiple times
    # with the same response.mp3 file causes it to stop working.
    # It seems changing the file name resolves this issue.
    r1 = str(random.randint(1, 1000000))
    r2 = str(random.randint(1, 1000000))
    randfile = r1 + "response" + r2 + ".mp3"
    tts.save(randfile)
    playsound(randfile)
    # We remember to delete the response file after this program finishes.
    # The deletion probably won't show on the windows explorer window
    # until the program ends (either by error or completion)
    os.remove(randfile)


if __name__ == "__main__":
    # keywords are special words which we can have special actions for if we hear them
    keywordlist = ["special", "hello"]
    done = False
    while not done:
        for j in range(6):  # we'll loop to keep checking for input
            print("Say something!")
            # here, we call our function to grab our words and transcribe it,
            # passing into "guess" a dictionary of values to work with
            guess = recognize_speech_from_mic(recognizer, microphone)
            if guess["transcription"]:
                break
            if not guess["success"]:
                break
            print("I didn't catch that. What did you say?\n")
        # if there was an error, stop break out of loop
        if guess["error"]:
            print("ERROR: {}".format(guess["error"]))
            break
        if guess["transcription"]:  # i.e. if the value of "transcription" != None
            audioTranscribed = str(guess["transcription"])
            print("You said: " + audioTranscribed)
            if audioTranscribed in keywordlist:  # if it's a word in our special keywords list
                for i in range(5):
                    try:
                        respond(audioTranscribed)
                        break
                    except:
                        print("response failed, trying again")
                        pass
            elif audioTranscribed == "close program":
                done = True
            # if neither if nor elif, then we'll listen again for more input
