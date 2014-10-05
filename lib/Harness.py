#!/usr/bin/python
#
# Author: Huanglin "Lincoln" Xiong
# Email: hxiong@wpi.edu
# Version: Sep 2014
#
# This library is the api for file movement and creation etc.

import os, subprocess

def swipeHistory(cur_dir = "."):
    his_dir = cur_dir + "/history/"
    for f in os.listdir(his_dir):
        os.remove(his_dir + f)

def swipeResults(cur_dir = "."):
    res_dir = cur_dir + "/results/"
    for directory in os.listdir(res_dir):
        for f in os.listdir(res_dir + directory):
            os.remove(res_dir + directory + "/" + f)

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

def run_test(test_file, counter, test_kind = "new", verbose = False, cur_dir = os.getcwd()):
    test_dir = cur_dir + "/test/" + test_kind + "/"
    test_unclassify_dir = cur_dir + "/test/unclassified/"
    test_time = 1
    if test_kind == "new":
        result_dir = cur_dir + "/results/unclassified/"
    else:
        if test_kind == "passed":
            result_dir = cur_dir + "/results/passed/"
        elif test_kind == "failed":
            result_dir = cur_dir + "/results/failed/"
        elif test_kind == "unclassified":
            result_dir = cur_dir + "/results/unclassified"
        else:
            print "FATAL: Wrong test kind...Harness Abort!"
            return
        # get the correct test time
        for f in os.listdir(result_dir):
            if "{0}_{1:04d}_".format(test_file, counter) in f:
                test_time = int(f[f.rfind("_")+1:]) + 1
    # make test file executable
    subprocess.call(["chmod", "+x", test_dir + test_file])
    # run the test file and put the output to the results
    logfile_name = "{0}{1}_{2:04d}_{3:03d}".format(result_dir, test_file, counter, test_time)
    subprocess.call(["touch", logfile_name])
    with open(logfile_name, 'r+') as logfile:
        os.chdir(test_dir)
        # XXX: do we need to catch any shell exception?
        subprocess.call([test_dir + test_file], stdout = logfile)
    os.chdir(cur_dir)
    if verbose:
        # print out the results of running the test
        with open(logfile_name, 'r') as logfile:
            for line in logfile:
                print line,
    if test_kind == "new":
        # move the test file to unclassified
        subprocess.call(["mv", test_dir + test_file, test_unclassify_dir])
    elif test_time != 1 and (test_kind == "passed" or test_kind == "failed"):
        # Compare the previous test result and current test result, if find different move the
        # the test to unclassified.
        result_dir = "./results/" + test_kind + "/"
        file_pre = "{0}_{1:04d}_{2:03d}".format(test_file, counter, test_time-1)
        if file_pre in os.listdir(result_dir):
            fp = open(result_dir + file_pre, 'r')
        fc = open(logfile_name, 'r')
        # check diff
        for linep, linec in zip(fp, fc):
            if linep != linec:
                # find diff, move test file to unclassified
                subprocess.call(["mv", logfile_name, cur_dir + "/results/unclassified/"])
                subprocess.call(["mv", test_dir + test_file, cur_dir + "/test/unclassified"])


