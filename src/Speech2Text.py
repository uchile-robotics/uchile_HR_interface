#!/usr/bin/env /usr/bin/python3.8

import rospy  # Import ROS for Python
import rospkg
import numpy as np
import re
from faster_whisper import WhisperModel
from std_msgs.msg import String, Int32, Bool # Import ROS messages of type String, Int32, and Bool
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
        self.listening = False
        
        # Publish a message
        self.pub = rospy.Publisher("/recognized_speech", String, queue_size=0)
        rospy.init_node('speech_hearing_topic', anonymous=True)  # Create and register the node!
        
        # Subscribe to the "listening" topic
        self.sub = rospy.Subscriber("/listening", Bool, self.callback_listening)
        
        with sr.Microphone() as mic:
            print('Calibrating...')
            self.recognizer.adjust_for_ambient_noise(mic, duration=10)
            print('Calibrated!')
            print('Energy threshold:', self.recognizer.energy_threshold)
    
    def callback_listening(self, msg):
        self.listening = msg.data
        rospy.loginfo(f"Listening status changed: {self.listening}")
        
    def get_language(self):
        return self.language
    
    def Hear(self):
        """Este método transforma el audio escuchado a texto"""
        if self.listening == False:
            pass
        
        elif self.listening:
            self.listening = False
            with sr.Microphone() as mic:
                try:
                    print("Listening for speech...")
                    audio = self.recognizer.listen(mic)
                except sr.WaitTimeoutError:
                    print("Listening timed out while waiting for phrase to start.")
                    return
                except sr.UnknownValueError:
                    print("No voice detected.")
                    return
                
                with open("speech.wav", "wb") as f:
                    f.write(audio.get_wav_data())
            
                audio_file = "speech.wav"
                
                # Read message from audio file
                print("Recognizing...")
                segments, info = self.model.transcribe(
                    audio_file,
                    beam_size=5
                )
                
                # Define the language detected
                self.language = info.language
                
                str_list = []
                
                print(f"Confidence: {info.language_probability}")
                if info.language_probability >= 0.7:
                    for segment in segments:
                        print(segment.text)
                        str_list.append(segment.text)
                        
                    message = " ".join(str_list)
                    print("Recognized!")
                    
                    msg = String()
                    msg.data = message
                    self.pub.publish(msg)
                    return message
        else:
            return

def main():
    obj = SpeechTotext()
    rospy.loginfo("Speech to text node started, waiting for listening signal...")
    
    while not rospy.is_shutdown():
        try:
            obj.Hear()
        except KeyboardInterrupt:
            rospy.loginfo("Shutting down speech to text node.")
            break
        except sr.UnknownValueError:
            print("No voice detected.")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")

if __name__ == '__main__':
    main()
