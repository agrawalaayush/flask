import requests
from optparse import OptionParser
url = 'http://127.0.0.1:5002/jobs/'
conversion_id = 1

def rest_call(conversion_id):
    post_url = url  + str(conversion_id) + '/' 
    data = '{"a":"aa"}'
    response = requests.post(post_url, data=data,headers={"Content-Type": "application/json"})
    print(response)
    print(response.text)
#print(sid)

if __name__ == "__main__":
    parser = OptionParser(usage=__doc__, version="Config Server 1.0")
    parser.add_option("-c", "--conversion", default=None, dest="conversion_id",  help="RDS user")
    options, args = parser.parse_args()
    rest_call(options.conversion_id)