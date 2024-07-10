#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-

import rospy
from std_msgs.msg import String
import smach
import smach_ros
import sys
import os

# Añadir la ruta de 'conversation_smach' al path de Python
sys.path.append(os.path.join(os.path.dirname(__file__), 'conversation_smach'))

from conversation_smach.search import NLPProcessor

# Definir el estado que publica en el tópico speech


class HearState(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['heared', 'timeout'], output_keys=['heared_data'])
        self.subscriber = None
        self.detected_speech = None

    def execute(self, userdata):
        rospy.loginfo('Esperando mensaje en el tópico /recognized_speech...')
        self.detected_speech = None
        self.subscriber = rospy.Subscriber('/recognized_speech', String, self.callback)

        # Esperar hasta que se reciba un mensaje o hasta que pase el timeout (10 segundos en este caso)
        timeout = rospy.Time.now() + rospy.Duration(10)
        while not rospy.is_shutdown() and self.detected_speech is None and rospy.Time.now() < timeout:
            rospy.sleep(0.1)

        self.subscriber.unregister()

        if self.detected_speech is not None:
            userdata.heared_data = self.detected_speech
            rospy.loginfo(self.detected_speech)
            return 'heared'
        else:
            return 'timeout'

    def callback(self, msg):
        self.detected_speech = msg.data

class Instruction_command_state(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['go_to_ollama'], input_keys=['input_data'], output_keys=['command'])
        self.nlp_model = NLPProcessor()

    def execute(self, userdata):
        command = self.nlp_model.process_query(userdata.heared_data)
        rospy.loginfo("El comando que entrega ollama es: %s", command)
        userdata.command = command
        return 'go_to_'



def main():
    rospy.init_node('smach_speech_node')

    # Crear una máquina de estado SMACH
    sm = smach.StateMachine(outcomes=["go_to_"])

    # Añadir estados a la máquina de estado
    with sm:
        smach.StateMachine.add('HEAR', HearState(), transitions={'heared':'Commands', 'timeout':'HEAR'}, remapping={'heared_data':'heared_data'})
        smach.StateMachine.add('Commands', Instruction_command_state(), transitions={'go_to_':'go_to_'}, remapping={'input_data':'heared_data', 'command':'command'})
        #smach.StateMachine.add('SPEECH', SpeechByInput(), transitions={'succeeded':'succeeded'}, remapping={'input_data':'ollama_answer'})

    # Ejecutar la máquina de estado
    outcome = sm.execute()

if __name__ == '__main__':
    main()
