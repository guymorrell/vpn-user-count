#/usr/bin/env python

import os
from datetime import datetime, date, timedelta
from argparse import ArgumentParser
import json

with open ("server.json", "rt") as server_f:
    server_d = json.load(server_f)
SERVER = server_d['SERVER']
USERNAME = server_d['USERNAME']
def get_logs():
    parser = ArgumentParser("Usage:")
    parser.add_argument('-p', '--path', type=str, default='/var/log/syslog-ng/',
                        help='Path [OPTIONAL]')
    parser.add_argument('-s', '--server', type=str, default=SERVER,
                        help='Servername [OPTIONAL]')
    parser.add_argument('-f', '--file', type=str, default='switch.log',
                        help='Filename [OPTIONAL]')
    parser.add_argument('-d', '--days', type=int, default=0,
                        help='How many days [OPTIONAL]')
    args = parser.parse_args()
    now = datetime.now()
    # logs rotate at 06:00, today's date is always yesterday's log
    today_ymd = now.strftime("%Y")+"-"+now.strftime("%m")+"-"+now.strftime("%d")+".gz"
    server_path = args.server+':'+args.path
    logfile = args.file+'-'+today_ymd
    arg = "scp "+USERNAME+'@'+server_path+logfile+" ./"
    if not os.path.exists(logfile):
        print("Copying "+logfile)
        os.system(arg)

get_logs()
