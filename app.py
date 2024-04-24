from flask import Flask, jsonify, render_template
import sqlite3
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    # Retrieve data from the database
    getDbData = getdataFromDB()

    # Pass the data as a variable to the template
    return render_template("index.html", data=getDbData)
 
#@app.route('/index')
#def indexs():
    #return 'index data:'


def getdataFromDB() -> dict:
    try:
        ## SQL to fetch one/latest data from db
        conn = sqlite3.connect('data.db') 
        cursor = conn.cursor() 
        cursor.execute('''SELECT * FROM data 
                        ORDER BY timestamp DESC 
                        LIMIT 1;''')

        row = cursor.fetchone()
        print(row)

        conn.commit()
        conn.close()

        LIVE_DATA = {
            #insert data to be displayed
        }

        return LIVE_DATA

    except Exception as e:
        print(f"DB error : {e}")
        return False

## route to return simple REST (json) data.
@app.route("/rest/data/v2", methods=['GET'])
def rest():

    getDbData = getdataFromDB()

    if getDbData is not False:

        return jsonify(success = 'y', data = getDbData)
    
    return jsonify(success = 'n')
    

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9999)
