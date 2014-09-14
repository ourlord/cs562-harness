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
        if directory == "new":
            continue
        for f in os.listdir(test_dir + directory):
            subprocess.call(["mv", test_dir + directory + "/" + f, test_dir + "/new/"])

def initRunAllTest(cur_dir = "."):
    test_dir = cur_dir + "/test/"
    for f in os.listdir(test_dir + "/inactive/"):
        subprocess.call(["mv", test_dir + "/inactive/" + f, test_dir + "/new/"])
    if os.listdir(test_dir + "/new/") == "":
        print "ERROR: There is no test files can be run!"
        quit()

def run_test(test_file, counter, cur_dir = "."):
    test_dir = cur_dir + "/test/new/"
    test_unclassify_dir = cur_dir + "/test/unclassified/"
    result_dir = cur_dir + "/results/unclassified/"
    # run the test file and put the output to the results
    subprocess.call([test_dir + test_file, ">", result_dir + test_file + "_{0:4d}".format(counter)])
    # move the test file to unclassified
    subprocess.call(["mv", test_dir + test_file, test_unclassify_dir])

