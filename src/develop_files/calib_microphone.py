#!/usr/bin/env python3.9

from faster_whisper import WhisperModel
from std_msgs.msg import String, Int32  # Import ROS messages of type String and Int32
import speech_recognition as sr
import pyttsx3



def main():

    recognizer = sr.Recognizer()

    model = WhisperModel("large-v3", device="cpu", compute_type="int8")



    print("microfono escuchando...")
    while True:
        with sr.Microphone() as mic:

            recognizer.adjust_for_ambient_noise(mic, duration=0.2)
            print("Recording for 4 seconds...")
            audio = recognizer.listen(mic, timeout=4)


            with open("speech.wav", "wb") as f:
                f.write(audio.get_wav_data())


            segments, info = model.transcribe(
                "speech.wav",
                beam_size=5,
                language="es"
            )

            str_list = []
            for segment in segments:
                print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
                str_list.append(segment.text)
                
            print(" ")
            message = " ".join(str_list)
            print(message)

        
    



if __name__ == '__main__':
    main()
