import requests
from optparse import OptionParser
url = 'http://127.0.0.1:5002/jobs/'
conversion_id = 1

 
data = '{"a":"aa"}'
import time
import threading 
import os

time_value = 0.00

def call_rest(conversion_id):
    print("ID of process running task 1: {}".format(os.getpid())) 
    st = int(time.time())
    params=[('modifiedTime', st)]
    get_url = url  + str(conversion_id) + '/'
    response = requests.get(get_url, params, timeout=60*2)
    et = time.time()
    global time_value
    time_value = time_value + float(et-st)
    print(et-st)
    print(response) 
    print(response.text)

def rest_call(conversion_id):
    threads = []
    for i in range(0, 2):
        threads.append(threading.Thread(target=call_rest, args=(conversion_id,)))

    for th in threads:
        th.start()

    for th in threads:
        th.join()

#global time_value
#import pdb;pdb.set_trace


if __name__ == "__main__":
    print (time.time())
    parser = OptionParser(usage=__doc__, version="Config Server 1.0")
    parser.add_option("-c", "--conversion", default=None, dest="conversion_id",  help="RDS user")
    options, args = parser.parse_args()
    rest_call(options.conversion_id)
    print("TOTAL TIME TAKEN {}".format(time_value))
    
