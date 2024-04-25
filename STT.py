#una version muy sencilla para play el speech
import rospy  # Import ROS for Python
import rospkg
import numpy as np
from faster_whisper import WhisperModel
from std_msgs.msg import String, Int32  # Import ROS messages of type String and Int32




class Hear(object):
    def __init__(self, args):
        super(Hear, self).__init__()
        self.model_size = "large-v3"
        self.language = 'es'
        self.model = WhisperModel(self.model_size, device="cpu", compute_type="int8")
        self.args = " "
        
        # Publish a message
        self.pub = rospy.Publisher("/speech", String, queue_size=10)


    def hear_audio(self, audio_file):
        """This method will be called everytime a new speech message is received."""
        
        #Read message from audio file
        segments, info = self.model.transcribe(
            audio_file,
            beam_size=5,
            language="es"
        )
        
        str_list = []
        for segment in segments:
            print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
            str_list.append(segment.text)
            
            
        message = " ".join(str_list)

        self.pub.publish(message)
        


def main():
    rospy.init_node('speech_hearing_topic')  # Create and register the node!

    obj = Hear('args')  # Create an object of type Joy_Template, defined above

    rospy.spin()  # ROS function that prevents the program from ending - must be used with Subscribers

if __name__ == '__main__':
    main()