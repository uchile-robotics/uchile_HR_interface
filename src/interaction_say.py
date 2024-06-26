import rospy  # Import ROS for Python


from std_msgs.msg import String, Int32 # Import ROS messages of type String and Int32




def Say(mensaje: str):

    pub = rospy.Publisher("/say", String, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    
    rospy.loginfo("Sending message..")
    msg = String()
    msg.data = mensaje
    pub.publish(msg)
