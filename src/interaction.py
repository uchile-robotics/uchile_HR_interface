##interaction
import rospy  # Import ROS for Python
import rospkg

from std_msgs.msg import String, Int32 # Import ROS messages of type String and Int32

import time




def Hear():
    
 
    text = rospy.wait_for_message("/recognized_speech", String)
    rospy.loginfo("mensaje recibido")
    heared = text.data
    return heared
    


def Say(mensaje: str):

    pub = rospy.Publisher("/say", String, queue_size=10)
    
    rospy.loginfo("Sending message..")
    msg = String()
    msg.data = mensaje
    pub.publish(msg)







#Ollama.send(Hear())