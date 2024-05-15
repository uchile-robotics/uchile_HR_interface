#una version muy sencilla para play el speech
import rospy  # Import ROS for Python
import rospkg
import numpy as np
import re
from faster_whisper import WhisperModel
from std_msgs.msg import String, Int32 # Import ROS messages of type String and Int32
import speech_recognition as sr
import pyttsx3  


class SpeechTotext(object):
    def __init__(self):
        super(SpeechTotext, self).__init__()
        self.model_size = "large-v3"
        self.model = WhisperModel(self.model_size, device="cpu", compute_type="int8")
        self.recognizer = sr.Recognizer()
        self.language = ""
        
        # Publish a message
        self.pub = rospy.Publisher("/speech", String, queue_size=10)
        rospy.init_node('speech_hearing_topic', anonymous=True)  # Create and register the node!
        
    def get_language(self):
        
        return self.language
    
    def detect_name(self, text):
        
        #Read message from audio file
        if re.search('bender', text)  or re.search('Bender', text) or re.search('vender', text)  or re.search('Vender', text) or re.search('wender', text)  or re.search('Wender', text):
            return True
        else:
            return False
            
            
    def Hear(self):
        """Este método trasnforma el audio escuchado a texto"""
        
        with sr.Microphone() as mic:

            self.recognizer.adjust_for_ambient_noise(mic, duration=0.2)
            print("Recording for 4 seconds...")
            audio = self.recognizer.listen(mic, timeout=4)


            with open("speech.wav", "wb") as f:
                f.write(audio.get_wav_data())
                
        audio_file = "speech.wav"
        
        #Read message from audio file
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
        print(message)

        #message = "linea de prueba linea de prueba linea de prueba linea de prueba"
        
        if self.detect_name(message):
            
            msg = String()
            msg.data = message
            #msg.data = "Linea de prueba"

            rospy.loginfo("Publisher node started")

            self.pub.publish(msg)
            print("mensaje publicado")
            return message
        
        else:

            print("Mensaje ignorado")
            
            return ""
        


def main():
    
    obj = SpeechTotext()
    obj.Hear()


if __name__ == '__main__':
    main()