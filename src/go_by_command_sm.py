#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-

import rospy
import smach
import smach_ros
from states import *
from move_to import *

class Dummy(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['succeeded'])
        
    def execute(self, userdata):
        rospy.loginfo('skibidi')
        return 'succeeded'
    
class Nav1(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['succeeded'])
        
    def execute(self, userdata):
        m = Move()
        x = 2.501
        y = 0.190
        w = 0.0
        m.set_pose(x, y, w) 
        m.go()
        return 'succeeded'

def main():
    rospy.init_node('smach_go')

    # Crear una máquina de estado SMACH
    sm = smach.StateMachine(outcomes=['succeeded', 'timeout'])

    # Añadir estados a la máquina de estado
    with sm:
        smach.StateMachine.add('DummyState', Dummy(), transitions={'succeeded':'GoTo'})
        smach.StateMachine.add('GoTo', Nav1(), transitions={'succeeded':'succeeded'})

    # Ejecutar la máquina de estado
    outcome = sm.execute()
    rospy.loginfo(f"State machine outcome: {outcome}")

if __name__ == '__main__':
    main()
