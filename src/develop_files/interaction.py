#!/usr/bin/env python

import rospy
from std_msgs.msg import String


class SayAndHear:
    def __init__(self):
        rospy.init_node('say_and_hear_node', anonymous=True)
        self.say_pub = rospy.Publisher('/say', String, queue_size=10)
        self.heard_message = "hola"

    def say(self, message):
        rospy.loginfo(message)
        msg = String()
        msg.data = message
        self.say_pub.publish(msg.data)

    def callback(self, msg):
        self.heard_message = msg.data

    def hear(self):
        
        rospy.Subscriber("/recognized_speech", String, self.callback)
        
        #while self.heard_message is None:
        rospy.sleep(0.1)  # Esperar 100 milisegundos

        return self.heard_message






if __name__ == '__main__':
    #rospy.init_node('my_node', anonymous=True)
    obj = SayAndHear()

    while not rospy.is_shutdown():
   
        try:
            received_message = obj.hear()
            print("Received message: ", received_message)
            rospy.sleep(1)
            # Ejemplo de uso de Say
            obj.say(received_message)
        except KeyboardInterrupt:
            rospy.loginfo("Shutting down speech to text node.")
            break

        # Ejemplo de uso de Hear

        
