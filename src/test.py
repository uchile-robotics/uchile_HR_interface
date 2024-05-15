""""Esta es una prueba de llamar las funciones externamente"""

#librerias de ROS
import rospy  
import rospkg
import numpy as np
from gtts import gTTS
from playsound import playsound
from std_msgs.msg import String, Int32
#el modulo de speech
from TTS import Speech 
#Prueba
import time

#para hacer una clase que implemente el speech para probar
class Random:
    def __init__(self, args):
        super(Random, self).__init__()
        self.args = args
        self._speech_sub = rospy.Subscriber("/speech", String, self.Do)

    def Do(self, msg):
        #to use init attributes there's a need to instanciate
        sp = Speech("noargs")
        sp.Say(msg)
        time.sleep(5)
        sp.Stop()

def main():
    rospy.init_node('speech_test')  # Create and register the node!
    obj = Random('args')  #instanciate speech
    rospy.spin()  # ROS function that prevents the program from ending - must be used with Subscribers

if __name__ == '__main__':
    main()