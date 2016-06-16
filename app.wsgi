#!/usr/bin/python
import os
import sys
import logging
logging.basicConfig(stream=sys.stderr)
# I'm having a hard time getting the environment variable from Apache, so I'll
# just hard-code it for now.
os.environ['FACHME_CONFIG'] = 'config/production.py'
sys.path.insert(0, os.path.dirname(__file__))

from fachme import app as application
