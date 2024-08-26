#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-

import rospy
import smach
import smach_ros
from states import *
from move_to import *
from conversation_smach.search import NLPProcessor



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
        smach.State.__init__(self, outcomes=['go_to'], input_keys=['heared_data'], output_keys=['command'])
        self.nlp_model = NLPProcessor()

    def execute(self, userdata):
        command = self.nlp_model.process_query(userdata.heared_data)
        rospy.loginfo("El comando que entrega ollama es: %s", command)
        userdata.command = command
        return 'go_to'
    
    
class Nav1(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['Conversation'], input_keys=['command'])
        

    def execute(self, userdata):
        print(userdata.command)

        if userdata.command == "Kitchen":
            rospy.loginfo("Bender fue a la cocina")
            m = Move()
            x = 2.501
            y = 0.190
            w = 0.0
            m.set_pose(x,y,w) 
            m.go()
            return 'Conversation'
        elif userdata.command == "Bathroom":
            rospy.loginfo("Bender fue al baño")
            m = Move()
            x = 1.695
            y = 2.03
            w = 0.0
            m.set_pose(x,y,w) 
            m.go()
            return 'Conversation'
        elif userdata.command == "Livingroom":
            rospy.loginfo("Bender fue a la sala de estar")
            #m = Move()
            #x = 2.501
            #y = 0.190
            #w = 0.0
            #m.set_pose(x,y,w) 
            #m.go()
            return 'Conversation'
        elif userdata.command == "Bedroom":
            rospy.loginfo("Bender fue al dormitorio")
            #m = Move()
            #x = 2.501
            #y = 0.190
            #w = 0.0
            #m.set_pose(x,y,w) 
            #m.go()
            return 'Conversation'
        else:
            rospy.loginfo("Bender no hace nada")
            #m = Move()
            #x = 3.00
            #y = 0.590
            #w = 0.0
            #m.set_pose(x,y,w) 
            #m.go()
            return 'Conversation'





def main():
    rospy.init_node('smach_go')

    # Crear una máquina de estado SMACH
    sm = smach.StateMachine(outcomes=['succeeded', 'timeout']) 

    # Añadir estados a la máquina de estado
    with sm:
        smach.StateMachine.add('Hear', HearState(), transitions={'heared':'Commands', "timeout":"Hear"}, remapping={'heared_data':'heared_data'})
        smach.StateMachine.add('Commands', Instruction_command_state(), transitions={'go_to':'GoTo'}, remapping={'heared_data':'heared_data', "command":"command"})
        smach.StateMachine.add('GoTo', Nav1(), transitions={'Conversation':'Conver'}, remapping={'command':'command'})
        smach.StateMachine.add('Conver', SpeechByString("llegue a la cocina"), transitions={'succeeded':'succeeded'}, remapping={'input_data':'input_data'})


    # Ejecutar la máquina de estado
    outcome = sm.execute()
    rospy.loginfo(f"State machine outcome: {outcome}")

if __name__ == '__main__':
    main()