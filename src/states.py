#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-

import sys
import os

# Añadir la ruta de 'conversation_smach' al path de Python
sys.path.append(os.path.join(os.path.dirname(__file__), 'conversation_smach'))
sys.path.append('/home/bender/bender_noetic/src/high/uchile_high/uchile_states/src/uchile_states/navigation')

sys.path.append('/home/bender/bender_noetic/src/high/uchile_high/bender_skills/src/bender_skills')

import rospy
from std_msgs.msg import String
import smach
import smach_ros
from move_to import *
from conversation_smach.search import NLPProcessor



# Definir el estado que publica en el tópico speech
class SpeechByInput(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['succeeded'], input_keys=['input_data'])

    def execute(self, userdata):
        rospy.loginfo('Publicando en el tópico /say: %s', userdata.input_data)
        pub = rospy.Publisher('/say', String, queue_size=10)
        rospy.sleep(1)  # Esperar un momento para asegurarse de que el nodo está conectado
        pub.publish(userdata.input_data)
        rospy.sleep(len(userdata.input_data)/20)
        return 'succeeded'
    
class SpeechByString(smach.State):
    def __init__(self, speech_text):
        smach.State.__init__(self, outcomes=['succeeded'])
        self.speech_text = speech_text

    def execute(self, userdata):
        rospy.loginfo('Publicando en el tópico /say: %s', self.speech_text)
        pub = rospy.Publisher('/say', String, queue_size=10)
        rospy.sleep(1)  # Esperar un momento para asegurarse de que el nodo está conectado
        pub.publish(self.speech_text)
        rospy.sleep(len(self.speech_text)/20)
        return 'succeeded'


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




class ConversationState(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['succeeded'], input_keys=['command'], output_keys=['ollama_answer'])
        self.nlp_processor = NLPProcessor()

    def execute(self, userdata):
        rospy.loginfo('Procesando comando con Ollama: %s', userdata.command)
        ollama_answer = self.nlp_processor.process_query(userdata.command)
        rospy.loginfo('Respuesta de Ollama: %s', ollama_answer)
        userdata.ollama_answer = ollama_answer
        return 'succeeded'
    
class Instruction_command_state(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['go_to_'], input_keys=['heared_data'], output_keys=['command'])
        self.nlp_model = NLPProcessor()

    def execute(self, userdata):
        command = self.nlp_model.process_query(userdata.heared_data)
        rospy.loginfo("El comando que entrega ollama es: %s", command)
        userdata.command = command
        return 'go_to'
    
class MoveTo(smach.State):
    def __init__(self):
        smach.State.__init__(self, input_keys=['command'], outcomes=['succeeded'])
    def execute(self, userdata):
        if userdata.command == "Go to the kitchen.":
            m = Move()
            x = -0.3029
            y = 1.81
            w = 0.955
            m.set_pose(x,y,w) 
            m.go()
            return 'succeeded'
        else:
            m = Move()
            x = -0.7029
            y = 1.31
            w = 0.955
            m.set_pose(x,y,w) 
            m.go()
            return 'succeeded'



def main():
    rospy.init_node('smach_speech_node')

    # Crear una máquina de estado SMACH
    sm = smach.StateMachine(outcomes=['succeeded', 'timeout'])

    # Añadir estados a la máquina de estado
    with sm:
        # smach.StateMachine.add('HEAR', HearState(), transitions={'heared':'Conversation', 'timeout':'HEAR'}, remapping={'heared_data':'command'})
        # smach.StateMachine.add('Conversation', ConversationState(), transitions={'succeeded':'SPEECH'}, remapping={'command':'command', 'ollama_answer':'ollama_answer'})
        smach.StateMachine.add('SPEECH', SpeechByString('Hola Soy Bender'), transitions={'succeeded':'succeeded'})

    # Ejecutar la máquina de estado
    outcome = sm.execute()

if __name__ == '__main__':
    main()
