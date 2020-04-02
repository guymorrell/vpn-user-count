#/usr/bin/env python
import re
import gzip
import yaml
from glob import glob
from get_logs import get_logs

filename, today_ymd = get_logs()
FILE_LIST = glob(filename+"*")

# Create a dict where the keys are VPN Groups and the values are empty lists
# e.g {'Group_CORP': [], 'Group_BYOD': []}
with open('groups.yml') as f:
    groups_l = yaml.load(f, Loader=yaml.FullLoader)
group_d = {}
for key in groups_l:
    group_d.update({key: []})

# Print CSV header
groups_l = list(group_d)
print("Date, ", end ='')
for i in range(len(groups_l)):
    print(groups_l[i]+", ", end='')
print()

def count_vpn(file_arg, group_dict):
    # If it's an old log, we'll need the date
    if file_arg.endswith('.gz'):
        date_l = file_arg.split('-')
        # Assume file ends YYYY-MM-DD.gz 
        date = date_l[-3]+'-'+date_l[-2]+'-'+date_l[-1]
        # remove.gz
        date = date.split('.')[0]
        opener = gzip.open
    else: # only current log isn't zipped and has no date suffix
        opener = open
        date = today_ymd
    # Check each line in the file for all groups in yml file
    with opener(file_arg, 'rt') as f:  
        log_l = f.readlines()
        for line in log_l:
            for key in group_dict:
                if re.search(key, line):
                    words = line.split()
                    # Pull out the user
                    my_list = words[8]
                    # If we've not seen the user before, add them
                    if my_list not in group_dict[key]:
                        group_dict[key].append(my_list)
    print(date+',',end='')
    # Print a count of users for each group, per day
    for k, v in group_dict.items():
        print(str(len(v))+', ',end='')
    print(end='\n')

for my_file in FILE_LIST:
    count_vpn(str(my_file), group_d)
