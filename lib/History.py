#!/usr/bin/python
#
# Author: Huanglin "Lincoln" Xiong
# Email: hxiong@wpi.edu
# Version: Sep 2014
#
# History class, deal with ops to the history files under history directory

import os, datetime, subprocess

# const dictionary to record the entry of history file for further usage
ENTRY_DICT = {
    'INIT':         1,
    'RESTART':      2,
    'RUN_ALL':      3,
    'RUN_TEST':     4,
    'CLASSIFY':     5,
    'REPORT_LAST':  6,
    'REPORT_TEST':  7,
    'TEST_SHOW':    8,
    'REPORT_ALL':   9,
    'ADD_TAGS':     10,
    'DIFF':         11
    }
# const string
CUR = "current"

class History(object):
    """
    History class is the interface to deal with any files under history directory
    @param[in]      entry       refer to the ENTRY_DICT
    """
    def __init__(self, entry):
        self.entry = ENTRY_DICT[entry]
        self.counter = 1
        self.his_dir = os.getcwd() + "/history/"
        # if entry is harness-init, we don't need to do further
        if entry == ENTRY_DICT['INIT']:
            return
        # else we need to get the correct counter
        if CUR in os.listdir(self.his_dir):
            f = open(self.his_dir + CUR, "r+")
            counter_str = f.readline()
            if counter_str.find('\n') != -1:
                # get current counter 1 greater than the previous one
                self.counter = int(counter_str[0 : counter_str.find('\n')])
                f.close()
                if entry == ENTRY_DICT['RESTART']:
                    self.counter += 1
            else:
                # current file is empty in this case, means last time harness might shut incorrectly.
                # so we need to find the correct counter in the history directory
                # But first of all, just swiped out the incorrectly 'current' file
                os.remove(his_dir + CUR)
                for f in os.listdir(his_dir):
                    if 'history_' in f:
                        self.counter = int(f[8:]) + 1
        else:
            # 'current' not in the directory, just in case, we still need to search all history file
            # and get the correct counter
            for f in os.listdir(self.his_dir):
                if 'history_' in f:
                    self.counter = int(f[8:]) + 1

    def initFile(self):
        """
        Create a new 'current' file in history directory.
        Should be called only by INIT and RESTART.
        """
        if self.entry == ENTRY_DICT['INIT']:
            # harness-init, just create a 'current' file and write the log
            subprocess.call(["touch", self.his_dir + CUR])
            f = open(self.his_dir + CUR, 'r+')
            f.write("{0:04d}".format(self.counter) + "\n")
            f.close()
            self.log("Initialize harness.")
        elif self.entry == ENTRY_DICT['RESTART']:
            # other: harness-restart
            # if there already a 'current' in history directory
            if CUR in os.listdir(self.his_dir):
                # change the 'current' file to 'history_'
                subprocess.call(["mv", self.his_dir + CUR, self.his_dir + "history_" + \
                        "{0:04d}".format(self.counter)])
                self.counter += 1
                # create new 'current'
                subprocess.call(["touch", self.his_dir + CUR])
                f = open(self.his_dir + CUR, 'r+')
                f.write("{0:04d}".format(self.counter) + "\n")
                f.close()
                self.log("Restart/Reinitialize harness.")
        else:
            # we suppose not to be here
            print "ERROR: Wrong entry to initFile()"

    def log(self, log_str) :
        """
        interface for logging in 'current' file.
        @param[in]      string      the context of logging information
        """
        f = open(self.his_dir + CUR, 'a')
        f.write(str(datetime.datetime.now()) + "\t" + log_str + "\n")
        f.close()

    def getCounter(self):
        return int(self.counter)
    def __getEntry(self):
        keys = ENTRY_DICT.keys()
        values = ENTRY_DICT.values()
        return keys[values.index(self.entry)]

    def report(self, verbose = False, cur_dir = "."):
        test_dir = cur_dir + "/test/"
        test_unclassify_dir = test_dir + "unclassified/"
        test_pass_dir = test_dir + "passed/"
        test_fail_dir = test_dir + "failed/"
        test_new_dir = test_dir + "new/"
        test_inactive_dir = test_dir + "inactive/"
        test_pass = []
        test_fail = []
        test_unclassify = []
        test_new = []
        test_inactive = []
        if self.entry == ENTRY_DICT['REPORT_LAST'] or self.entry == ENTRY_DICT['REPORT_ALL']:
            for f in os.listdir(test_pass_dir):
                test_pass.append(f)
            for f in os.listdir(test_fail_dir):
                test_fail.append(f)
            for f in os.listdir(test_unclassify_dir):
                test_unclassify.append(f)
            if self.entry != ENTRY_DICT['REPORT_ALL']:
                for f in os.listdir(test_new_dir):
                    test_new.append(f)
                for f in os.listdir(test_inactive_dir):
                    test_inactive.append(f)
            out_str = ""
            if verbose:
                out_str += "\nPassed: "
                for i in test_pass:
                    out_str += i + " "
                out_str += "\nFailed: "
                for i in test_fail:
                    out_str += i + " "
                out_str += "\nUnclassified: "
                for i in test_unclassify:
                    out_str += i + " "
                if self.entry != ENTRY_DICT['REPORT_ALL']:
                    out_str += "\nUnrun: "
                    for i in test_new:
                        out_str += i + " "
                    out_str +="\nInactive: "
                    for i in test_inactive:
                        out_str += i + " "
            total = len(test_pass) + len(test_fail) + len(test_unclassify) + len(test_new) +\
                    len(test_inactive)
            if self.entry == ENTRY_DICT['REPORT_LAST']:
                report_str = "{6}: Total test: {0}, Passed: {1}/{0}, Failed: {2}/{0}, Unclassified: {3}/{0}, Unrun: {4}/{0}, Inactive: {5}/{0}.".\
                        format(total, len(test_pass), len(test_fail), len(test_unclassify), \
                        len(test_new), len(test_inactive), self.__getEntry())
            elif self.entry == ENTRY_DICT['REPORT_ALL']:
                report_str = "{4}: Runned: {0}, Passed: {1}/{0}, Failed: {2}/{0}, Unclassified: {3}/{0}".\
                        format(total, len(test_pass), len(test_fail), len(test_unclassify), \
                        self.__getEntry())
            self.log(report_str 
                    #+ out_str          # XXX: haven't decided to add this to history file
                    )
            print report_str
            print out_str
        else:
            print "ERROR: Wrong entry!"
            quit()

    def report_test(self, test, detail = False):
        if self.entry == ENTRY_DICT['REPORT_TEST']:
            # XXX: for now, this function just return the corresponding line of history of test
            print "===== Generate report for test {0} =====".format(test)
            num_run = 0
            num_pass = 0
            num_fail = 0
            for f in os.listdir(self.his_dir):
                h = open(self.his_dir + f, 'r')
                out_str = ""
                line_no = 0
                for line in h:
                    line_no += 1
                    if "\"{0}\"".format(test) in line:
                        out_str += "@{0}:    {1}".format(line_no, line)
                        if 'TEST RUN:' in line:
                            num_run += 1
                        elif 'TEST PASS:' in line:
                            num_pass += 1
                        elif 'TEST FAIL:' in line:
                            num_fail += 1
                if out_str != "":
                    print self.his_dir + f + ":"
                    print out_str,
            # add this feature to show how many times this test ran, passed, failed
            if detail:
                print "{0} runs {1} times, pass {2} times, fail {3} times.".format(test, num_run, \
                        num_pass, num_fail)

        else:
            print "ERROR: Wrong entry!"
            quit()
