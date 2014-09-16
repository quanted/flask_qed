#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import subprocess

def sam():

    curr_dir = os.path.dirname(os.path.realpath(__file__))
    exe = "SuperPRZMPesticide.exe"
    sam_path = os.path.join(curr_dir, 'bin', 'ubertool_superprzm_src', 'Debug', exe)
    # print sam_path
    sam_args = os.path.join(curr_dir, 'bin')
    a = subprocess.Popen(sam_path + " " + sam_args)
    a.wait()

    print "Done"

    return "Done!"