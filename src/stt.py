#una version muy sencilla para play el speech
import rospy  # Import ROS for Python
import rospkg
import numpy as np
from gtts import gTTS
from playsound import playsound
from std_msgs.msg import String, Int32  # Import ROS messages of type String and Int32


class Speech(object):
    def __init__(self, args):
        super(Speech, self).__init__()
        self.args = args
        self.language = 'es'

        # Subscribe to speech messages
        self._speech_sub = rospy.Subscriber("/speech", String, self.Say)


    def Say(self, msg):
        """This method will be called everytime a new speech message is received."""

        #habria que decir el canal en el que esta el texto msg.algo
        text = msg.data
        
        #Lo que usa la libreria
        speech = gTTS(text = text, tld="com.mx" ,lang = self.language, slow = False)

        speech.save("output.wav")

        #como reproducimos el archivo?
        playsound('output.wav')
        


def main():
    rospy.init_node('speech_test')  # Create and register the node!

    obj = Speech('args')  # Create an object of type Joy_Template, defined above

    rospy.spin()  # ROS function that prevents the program from ending - must be used with Subscribers

if __name__ == '__main__':
    main()