#!/usr/bin/env /usr/bin/python3.8

import rospy  # Import ROS for Python
import rospkg
import numpy as np
import re
from faster_whisper import WhisperModel
from std_msgs.msg import String, Int32 # Import ROS messages of type String and Int32
import speech_recognition as sr
import pyttsx3  
import time

class SpeechTotext(object):
    def __init__(self):
        super(SpeechTotext, self).__init__()
        self.model_size = "large-v3" # tiny.en, tiny, base.en, base, small.en, small, medium.en, medium, large-v1, large-v2, large-v3, large, distil-large-v2, distil-medium.en, distil-small.en, distil-large-v3
        self.model = WhisperModel(self.model_size, device="cuda", compute_type="int8")
        self.recognizer = sr.Recognizer()
        self.language = ""
        
        # Publish a message
        self.pub = rospy.Publisher("/recognized_speech", String, queue_size=10)
        rospy.init_node('speech_hearing_topic', anonymous=True)  # Create and register the node!
        with sr.Microphone() as mic:
            print('Calibrating...')
            self.recognizer.adjust_for_ambient_noise(mic, duration=10)
            print('Calibrated!')
        
    def get_language(self):
        return self.language
    
    def Hear(self):
        """Este método trasnforma el audio escuchado a texto"""
        with sr.Microphone() as mic:            
            print("Recording...")
            audio = self.recognizer.listen(mic, phrase_time_limit=15, timeout=5)

            with open("speech.wav", "wb") as f:
                f.write(audio.get_wav_data())
        
            
            
        audio_file = "speech.wav"
        
        #Read message from audio file
        print("Recognizing...")
        segments, info = self.model.transcribe(
            audio_file,
            beam_size=5
        )
        
        #Define the language detected
        self.language = info.language
        
        str_list = []
        for segment in segments:
            print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
            str_list.append(segment.text)
            
        message = " ".join(str_list)
        print("Recognized!")
        
        msg = String()
        msg.data = message
        #msg.data = "Linea de prueba"

        rospy.loginfo("Publisher node started")
        self.pub.publish(msg)
        return message

def main():
    obj = SpeechTotext()
    rospy.loginfo("Speech to text node started, listening...")
    rate = rospy.Rate(0.1)  # Adjust the rate as needed (0.1 Hz = 10 seconds)
    
    while not rospy.is_shutdown():
        try:
            obj.Hear()
            rate.sleep()
        except KeyboardInterrupt:
            rospy.loginfo("Shutting down speech to text node.")
            break

        except sr.UnknownValueError:
                        # Si el audio no contiene voz inteligible, continuar
                        print("No voice detected.")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")

if __name__ == '__main__':
    main()
