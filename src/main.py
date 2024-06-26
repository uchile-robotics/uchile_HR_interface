from interaction_hear import Hear
from interaction_say import Say
import rospy  # Import ROS for Python
import rospkg


#rospy.init_node('main_test', anonymous=True)

text = Hear()

print(text)

Say(text)

#rospy.spin()