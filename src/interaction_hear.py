##interaction
import rospy  # Import ROS for Python

from std_msgs.msg import String, Int32 # Import ROS messages of type String and Int32





def Hear():
    rospy.init_node('hearing_test', anonymous=True)
    text = rospy.wait_for_message("/recognized_speech", String)
    rospy.loginfo("mensaje recibido")
    #heared = text.data
    heared = "hola edu"
    return heared
    









#Ollama.send(Hear())