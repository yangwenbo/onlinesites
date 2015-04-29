#!/usr/bin/env python
# encoding: utf-8
import subprocess

#subprocess.Popen(["uwsgi","--ini","mysite_uwsgi.ini"])
subprocess.Popen(["python","sa.py"])
subprocess.Popen(["python","da.py"])