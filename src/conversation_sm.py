#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-

import rospy
from std_msgs.msg import String
import smach
import smach_ros
import sys
import os
from states import *

def main():
    rospy.init_node('smach_speech_node')

    # Crear una máquina de estado SMACH
    sm = smach.StateMachine(outcomes=['succeeded', 'timeout'])

    # Añadir estados a la máquina de estado
    with sm:
        smach.StateMachine.add('HEAR', HearState(), transitions={'heared':'Conversation', 'timeout':'HEAR'}, remapping={'heared_data':'command'})
        smach.StateMachine.add('Conversation', ConversationState(), transitions={'succeeded':'SPEECH'}, remapping={'command':'command', 'ollama_answer':'ollama_answer'})
        smach.StateMachine.add('SPEECH', SpeechByInput(), transitions={'succeeded':'succeeded'}, remapping={'input_data':'ollama_answer'})

    # Ejecutar la máquina de estado
    outcome = sm.execute()

if __name__ == '__main__':
    main()
