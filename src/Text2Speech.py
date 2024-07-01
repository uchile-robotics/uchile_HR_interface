#!/usr/bin/env python3.9

import rospy  
import rospkg
import numpy as np
from std_msgs.msg import String, Int32  
import sounddevice as sd
import soundfile as sf
import torch
from TTS.api import TTS

# Get device
device = "cuda" if torch.cuda.is_available() else "cpu"

class Speech(object):
    def __init__(self, args):
        super(Speech, self).__init__()
        self.args = args
        print("modelo ini")
        self.language = 'es'
        if self.language == 'es':
            self.tts = TTS("tts_models/es/css10/vits").to(device)
        elif self.language == 'en':
            self.tts = TTS("tts_models/en/ljspeech/vits--neon").to(device)
        self._speech_sub = rospy.Subscriber("/say", String, self.Say)
         

    def Say(self, msg):
        print("The method was called!")
        text = msg.data
        # Text to speech to a file
        self.tts.tts_to_file(text=text, file_path="output.wav")
        
        data, fs = sf.read("output.wav", dtype='float32')  
        sd.play(data, fs)
        sf.write("output.wav", data, fs)

    def Stop(self):
        sd.stop()

def main():
    rospy.loginfo("tts_node started!")
    rospy.init_node('speech_2_text_node')  # Create and register the node!
    obj = Speech('args')  # Instanciate speech
    rospy.spin()  # ROS function that prevents the program from ending - must be used with Subscribers

if __name__ == '__main__':
    main()
