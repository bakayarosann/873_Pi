#!/usr/bin/env python
import requests
username = '3130103047'
password = 'do not tell you'
payload ={'action':'login','username':username,'password':password,'ac_id':'3','user_ip':'','nas_ip':'','user_mac':'','save_me':'1','ajax':'1'}
url = "https://net.zju.edu.cn/cgi-bin/srun_portal"
res = requests.post(url, data = payload)

# print res.text

