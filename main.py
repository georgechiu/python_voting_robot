#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2018年12月27日

@author: George Chiu
'''


from robot_sohu import Voting_Robot_Sohu
from robot_yidian import Voting_Robot_Yidian

if __name__ == '__main__':
    # robot = Voting_Robot_Sohu()
    robot = Voting_Robot_Yidian()
    robot.start()