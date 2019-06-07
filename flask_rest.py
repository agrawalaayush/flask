from flask import Flask, request, Response
from flask_restful import Resource, Api
from flask import jsonify

import sqlite3 as sql
import time
from gevent import pywsgi
from gevent import monkey

# need to patch sockets to make requests async
monkey.patch_all()

app = Flask(__name__)
app.debug = True
api = Api(app)

DRUVA_HEADER_KEY = 'aaabbb'
def create_db():
    conn = sql.connect('rest_database.db')
    print("Opened database successfully")
    conn.execute('CREATE TABLE IF NOT EXISTS status (conversion_id INT, status TEXT, read INT)')
    conn.execute('CREATE TABLE IF NOT EXISTS modification (conversion_id INT, modifytime INT)')
    print("Status Table created successfully")
    conn.commit()
    conn.close()

@app.route("/")
@app.route("/<data>/")
def hello(data=None):
    if data:
        return "Hello " + str(data)
    return "Hello World!"

 
class Jobs(Resource):
    
    def _is_updated(self, conversion_id, lastmodifiedtime):
        con = sql.connect("rest_database.db")
        con.row_factory = sql.Row
        cur = con.cursor()
        query = "select * from modification where conversion_id = " + str(conversion_id) 
        cur.execute(query)
        rows = cur.fetchall()
        for row in rows:
            if lastmodifiedtime < row['modifytime']:
                return True
        return False
    
    def get(self, conversion_id):
        #conn = db_connect.connect() # connect to database
        #query = conn.execute("select * from employees") # This line performs query and returns json result
        #return {'employees': [i[0] for i in query.cursor.fetchall()]}
        #import time
        #time.sleep(2*60)
        args = request.args
        print (args)
        modifiedTIme = int(args['modifiedTime'])
        authorization = str(request.headers.get('X-Druva-Secret'))
        #if authorization != DRUVA_HEADER_KEY:
        #    response = jsonify({'message':'A winner is you'})
        #    return Response('<Why access is denied string goes here...>', 401, {'WWW-Authenticate':'Basic realm="Login Required"'})
        while not self._is_updated(conversion_id, modifiedTIme):
            time.sleep(30)
        con = sql.connect("rest_database.db")
        con.row_factory = sql.Row
        cur = con.cursor()
        query = "select * from status where conversion_id = " + str(conversion_id) 
        cur.execute(query)
        rows = cur.fetchall()
        rows_info = []
        for row in rows:
            a = {}
            a['status'] = row['status']
            a['read'] = row['read']
            rows_info.append(a)
        return "Status Information for " + str(conversion_id)+ " " + str(rows_info)
    
    def post(self, conversion_id):
        #import pdb;pdb.set_trace()
        #print("request data" + str(request))
        try:
            status = str(request.get_json())
            with sql.connect("rest_database.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO status (conversion_id,status,read) VALUES (?,?,?)",(conversion_id,status,0) )
                query = "select * from modification where conversion_id = " + str(conversion_id) 
                cur.execute(query)
                rows = cur.fetchall()
                if rows:
                    cur.execute("Update modification set modifytime = ? where conversion_id = ?",(time.time(), conversion_id))
                else:
                    cur.execute("INSERT INTO modification (conversion_id,modifytime) VALUES (?,?)",(conversion_id,time.time()) )            
                con.commit()
                msg = "Record successfully added"
        except Exception as fault:
            print(fault)
            con.rollback()
            msg = "error in insert operation"
      
        finally:
            return msg
            con.close()
        #print("request dataaa" + str(request.get_json()))
        #print(dir(request))
        #return str(request.get_json()) +" "+ str(conversion_id)

api.add_resource(Jobs, '/jobs/<int:conversion_id>/')

if __name__ == '__main__':
    create_db()
    #app.run(port='5002', threaded=True)
    server = pywsgi.WSGIServer(('0.0.0.0', 5002), app.wsgi_app)
    server.serve_forever()