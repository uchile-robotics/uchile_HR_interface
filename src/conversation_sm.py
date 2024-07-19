#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-

import rospy
import smach
import smach_ros
from states import *

class Dummy(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['succeeded', 'aborted'])
        
    def execute(self, userdata):
        rospy.loginfo('skibidi')
        rospy.sleep(5)
        return 'succeeded'

def main():
    rospy.init_node('smach_speech_node')

    # Crear una máquina de estado SMACH
    sm = smach.StateMachine(outcomes=['succeeded', 'timeout','aborted'])

    # Añadir estados a la máquina de estado
    with sm:
        smach.StateMachine.add('HEAR', HearState(), 
                               transitions={'heared': 'Conversation', 'timeout': 'HEAR'},
                               remapping={'heared_data': 'command'})
        
        smach.StateMachine.add('Conversation', ConversationState(), 
                               transitions={'succeeded': 'SPEECH'},
                               remapping={'command': 'command', 'ollama_answer': 'ollama_answer'})
        
        smach.StateMachine.add('SPEECH', SpeechByInput(), 
                               transitions={'succeeded': 'Dummy'},
                               remapping={'input_data': 'ollama_answer'})
        
        smach.StateMachine.add('Dummy', Dummy(), 
                               transitions={'succeeded': 'HEAR', 'aborted': 'aborted'})

    # Ejecutar la máquina de estado
    outcome = sm.execute()

if __name__ == '__main__':
    main()
