#!/usr/bin/env python
import RPi.GPIO as GPIO
import time
import socket
import json
import requests
import httplib
import urllib

class HTTPClient(object):

    url_report = "/api/report"
    url_get_data = "/api/data"
    url_push = "/api/push"
    url_poll = "/api/poll"

    def __init__(self, auth_id, auth_key, server_addr):
        self.auth_id = auth_id
        self.auth_key = auth_key
        self.server_addr = server_addr
        self.server_url = "http://{}".format(server_addr)

    def report(self, device_id, data):
        '''
        device_id is an integer
        data is a dictionary
        '''
        packet = {
        "auth_id": self.auth_id,
        "auth_key": self.auth_key,
        "device_id": device_id,
        "payload": data
        }
        try:
            r = requests.post(self.server_url+self.url_report, json.dumps(packet))
        except requests.RequestException as e:
            print(e)
            return False
        print(r.status_code)

    def get_data(self, device_id, limit=200):
        try:
            r = requests.get("{}{}?device_id={}&limit={}".format(self.server_url, self.url_get_data, device_id, limit))
        except requests.RequestException as e:
            print(e)
            return
        try:
            data = json.loads(r.text)
        except json.JSONDecodeError as e:
            print(e)
            return
        if data['code'] == 0:
            return data['data']

#send data to nya.fatmou.se
def send_data1(number): 
    c = HTTPClient(23, "f94d3aa2dcf5b8ee2db0a0d4bdf2a200", "nya.fatmou.se")
    data = {
        "number": number,
        "time": time.time(),
    }
    print(c.report(23, data))
    print(c.get_data(23))

#send data to fat.fatmou.se
def send_data2(count):
    httpClient = None
    try:
        number=''+str(count)
        time_now=''+str(time.time())
        auth_id=14
        device_id=14
        report_id=8
        auth_key='94c75c6f6c67e1a335c724a6ff137a6e'
        payload='{"number": "'+number+'","time": "'+time_now+'" }'
        
        report_data = {
            'auth_id': auth_id,
            'auth_key': auth_key,
            'device_id': device_id,
            'report_id': report_id,
            'payload': payload
        }

        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        httpClient = httplib.HTTPConnection("fat.fatmou.se", 80, timeout=30)
       
        params = urllib.urlencode(report_data)
        httpClient.request("POST", "/api/report", params, headers)
        
        response = httpClient.getresponse()
        print response.status
        print response.reason
        print response.read()
        print response.getheaders()
    except Exception, e:
        print e
    finally:
        if httpClient:
            httpClient.close()
            
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(15,GPIO.OUT)
GPIO.setup(16,GPIO.IN)
GPIO.setup(18,GPIO.IN)

count=0
sensor1=0
sensor2=0
time_stamp1=time.time()
time_stamp2=time.time()
state1_pre=False
state2_pre=False
clk=0;

for i in range(1,4):
    GPIO.output(15,False)
    time.sleep(1)
    GPIO.output(15,True)
    time.sleep(1)

while True:
    if GPIO.input(18)==True:
        time_stamp1=time.time()
    if GPIO.input(16)==True:
        time_stamp2=time.time()
    
    #front
    if GPIO.input(18)==True and state1_pre==False: #if someone appear in front
        print "front detectd"
        if sensor2==0: #come in
           sensor1=1
        else:  #come out   
           dtime=time.time()-time_stamp2 #check if time < 3
           if dtime < 3:
	       print "front valid" 
               sensor2=0
               count=count-1 #count--
           else:
	       print "front invalid"
               sensor2=0
               sensor1=1
    state1_pre=GPIO.input(18)
    
    #behind
    if GPIO.input(16)==True and state2_pre==False:#if someone appear behind
        print "behind detectd"
        if sensor1==0: #come in
           sensor2=1
        else:   #come out
           dtime=time.time()-time_stamp1 #check if time < 3
           if dtime < 3:
	       print "behind valid"
               sensor1=0
               count=count+1 #count++
           else:
	       print "behind invalid"
               sensor1=0
               sensor2=1
    state2_pre=GPIO.input(16)
    
    time.sleep(0.1)
    
    clk=clk+1;
    if clk==100: #send data every 10 seconds
        clk=0
	send_data1(count)
	#send_data2(count)
        print("the number of people:"+str(count))
        if count >= 6:
            print("Don't come in!The bathroom is full now!")
            GPIO.output(15,True)
        else:
            GPIO.output(15,False)
              


        
    
        
