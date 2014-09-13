#!/usr/bin/python
#
# Author: Huanglin "Lincoln" Xiong
# Email: hxiong@wpi.edu
# Version: Sep 2014
#
# History class, deal with ops to the history files under history directory

import os, datetime, subprocess

ENTRY_DICT = {
    'INIT':         1,
    'RESTART':      2,
    'RUN_ALL':      3,
    'RUN_TEST':     4
    }
 
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
                counter = int(counter_str[0 : counter_str.find('\n')]) + 1
                f.close()
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
        Create a new 'current' file in history directory
        """
        if self.entry == ENTRY_DICT['INIT']:
            # harness-init, just create a 'current' file and write the log
            subprocess.call(["touch", self.his_dir + CUR])
            f = open(self.his_dir + CUR, 'r+')
            f.write(str(self.counter) + "\n")
            f.close()
            self.log("Initialize harness.")
        elif self.entry == ENTRY_DICT['RESTART']:
            # other: harness-restart
            # if there already a 'current' in history directory
            if CUR in os.listdir(self.his_dir):
                # change the 'current' file to 'history_'
                subprocess.call(["mv", self.his_dir + CUR, self.his_dir + "history_" + \
                        str(self.counter)])
                self.counter += 1
                # create new 'current'
                subprocess.call(["touch", self.his_dir + CUR])
                f = open(self.his_dir + CUR, 'r+')
                f.write(str(self.counter) + "\n")
                f.close()
                self.log("Restart/Reinitialize harness.")
        else:
            # we suppose not to be here
            print "ERROR: Wrong entry to initFile()"

    def log(self, log_str):
        """
        interface for logging in 'current' file
        @param[in]      string      the context of logging information
        """
        f = open(self.his_dir + CUR, 'a')
        f.write(str(datetime.datetime.now()) + "\t" + log_str + "\n")
        f.close()
