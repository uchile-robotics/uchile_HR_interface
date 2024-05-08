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
        self.model = WhisperModel(self.model_size, device="cpu", compute_type="int8")
        self.args = " "
        
        # Publish a message
        
        self.pub = rospy.Publisher("/speech", String, queue_size=10)
        rospy.init_node('speech_hearing_topic', anonymous=True)  # Create and register the node!


    def hear_audio(self, audio_file):
        """Este método trasnforma el audio escuchado a texto"""
        
        #Read message from audio file
        segments, info = self.model.transcribe(
            audio_file,
            beam_size=5
        )
        
        str_list = []
        for segment in segments:
            print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
            str_list.append(segment.text)
            
            
        message = " ".join(str_list)
        print(message)

        #message = "linea de prueba linea de prueba linea de prueba linea de prueba"
        
        msg = String()
        msg.data = message
        #msg.data = "Linea de prueba"
        print("")

        rospy.loginfo("Publisher node started")

        self.pub.publish(msg)
        print("mensaje publicado")
        


def main():
    
    audio_sample = "/home/robotica02/projects_ws/src/uchile_hr_interface/src/audio_samples/audio_rosa.m4a"
    obj = Hear('args')
    obj.hear_audio(audio_sample)


if __name__ == '__main__':
    main()