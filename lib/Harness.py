#!/usr/bin/python
#
# Author: Huanglin "Lincoln" Xiong
# Email: hxiong@wpi.edu
# Version: Sep 2014
#

import os, subprocess

def swipeHistory(cur_dir = "."):
    his_dir = cur_dir + "/history/"
    for f in os.listdir(his_dir):
        os.remove(his_dir + f)

def swipeResults(cur_dir = "."):
    res_dir = cur_dir + "/results/"
    for directory in os.listdir(res_dir):
        for f in os.listdir(res_dir + directory):
            os.remove(res_dir + directory + f)

def initTestFile(cur_dir = "."):
    test_dir = cur_dir + "/test/"
    for directory in os.listdir(test_dir):
        for f in os.listdir(test_dir + directory):
            subprocess.call(["mv", test_dir + directory + f, test_dir + "/new/"])

def initRunAllTest(cur_dir = "."):
    test_dir = cur_dir + "/test/"
    for f in os.listdir(test_dir + "/inactive/"):
        subprocess.call(["mv", test_dir + "/inactive/" + f, test_dir + "/new/"])
    if os.listdir(test_dir + "/new/") == "":
        print "ERROR: There is no test files can be run!"
        quit()
