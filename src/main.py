from interaction import Hear, Say
import rospy  # Import ROS for Python
import rospkg

rospy.init_node('listener_2') 


text = Hear()

print(text)

Say(text)

rospy.spin()