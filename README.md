# vpn-user-count
Count number of users per profile in ASA syslog

#### Local data

Create a file `server.json` containg your syslog server and username:

```
{
	"SERVER": "hostname.domain",
	"USERNAME": "my_username"
}
```

Use ssh keys to login to your syslog server.

Create a file `groups.yml` containing the VPN Groups you are interested in:
```
---
- 'Group_BYOD'
- 'Group_CORP'
```

#### Source Logfiles
We are analysing loglines like this, pulling out a unique list of users per group and printing the results.
`Apr  2 09:09:50 vpn_hostname.domain %ASA-5-722033: Group <GROUP_NAME> User <USER_NAME> IP <IP_ADDRESS> MESSAGE`

To get this, we need to pass the filename and its path on the syslog server to the script:
`python vpn_user_count.py -f 'vpn_hostname.domain.log' -p '/var/log/syslog-ng/VPN/'`

#### Running the script
This will print CSV style output for each log in the local dir. 
```
$ python vpn_user_count.py -f 'vpn_hostname.domain.log' -p '/var/log/syslog-ng/VPN/'
Date, Group_BYOD, Group_CORP, 
2020-04-01,99, 737, 
2020-04-02,119, 859, 
```
#### To do
- Update get_logs to action the -d flag and grab more than just yesterday's logs
- Dump output to local .csv
