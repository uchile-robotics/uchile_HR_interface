#librerias de ROS
import rospy  
import rospkg
import numpy as np
from gtts import gTTS
from playsound import playsound
from std_msgs.msg import String, Int32  
#librerias de sonido
import sounddevice as sd
import soundfile as sf
#for tests 
import time


class Speech(object):
    def __init__(self, args):
        super(Speech, self).__init__()
        self.args = args
        self.language = 'es'
        #self._speech_sub = rospy.Subscriber("/speech", String, self.Say)

        #self.paused = False

    def Say(self, msg):
        print("the method was called!")
        """This method will be called everytime a new speech message is received."""
        text = msg.data
        speech = gTTS(text = text, tld="com.mx" ,lang = self.language, slow = False)
        speech.save("output.wav")

        data, fs = sf.read("output.wav", dtype='float32')  
        sd.play(data, fs)
        # time.sleep(10)
        # self.Stop()


    def Stop(self):
        sd.stop()

def main():
    rospy.init_node('speech_test')  # Create and register the node!
    obj = Speech('args')  #instanciate speech
    rospy.spin()  # ROS function that prevents the program from ending - must be used with Subscribers

if __name__ == '__main__':
    main()