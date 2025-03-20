# Made by Juliano E. S. Padua
import pandas as pd
import matplotlib.pyplot as plt
from utils import load_config
import datetime
import os
import yaml

script_dir = os.path.dirname(os.path.abspath(__file__))

config = load_config()

# initialize paths from config
data_raw_path = os.path.join(script_dir, config['paths']['data_raw'])
data_processed_path = os.path.join(script_dir, config['paths']['data_processed'])
images_path = os.path.join(script_dir, config['paths']['images'])
report_path = os.path.join(script_dir, config['paths']['report'])
addons_path = os.path.join(script_dir, config['paths']['addons'])

# your code starts here
current_datetime = datetime.datetime.now()
print(f"Project 'p03-web-report' initialized on 2025-03-20 12:44:41")
