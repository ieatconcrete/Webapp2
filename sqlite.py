#sqlite

import sqlite3
from pymavlink import mavutil
from time import sleep
import threading

conn = sqlite3.connect('data.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS data (
                  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  ##insert data to be displayed##
                )''')

conn.commit()
conn.close()

LIVE_DATA = {
    #insert data to be displayed
}

master = mavutil.mavlink_connection("COM22", baud=57600)

master.wait_heartbeat()
print(f"Got HeartBeat")

def fcDataExtract():
    global LIVE_DATA
    global master

    while True:
        try:
            data = master.recv_match()

            if data:
                data_dict = data.to_dict()
                #convert the mavpackettypes from the original packet names to the given table key names, eg:
                #if data_dict['mavpackettype'] == 'GLOBAL_POSITION_INT':
                    #LIVE_DATA['relAlt'] = data_dict['relative_alt'] / 1000  # in meters

                #elif data_dict['mavpackettype'] == 'GPS_RAW_INT':
                    #UAV_DATA['lat'] = data_dict['lat'] / (10 ** 7)
                    #UAV_DATA['lng'] = data_dict['lon'] / (10 ** 7)

               

        except Exception as e:
            print(f"Error: {e}")

        

        # print(f"-----------")
        # print(f"relAlt: {UAV_DATA['relAlt']}\nLat: {UAV_DATA['lat']}\nLng: {UAV_DATA['lng']}\nGroundSpeed: {UAV_DATA['groundSpeed']}\nHeading: {UAV_DATA['heading']}\nRoll: {UAV_DATA['roll']} | Pitch: {UAV_DATA['pitch']} | Yaw: {UAV_DATA['yaw']}\n")
        #snippet for printing the data in the terminal

    



def dataUpdateInDB():
    global LIVE_DATA
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    while True:
        try:
            cursor.execute('''INSERT INTO data 
                            (##table key names### A, B, C, D, E, F, G, H) 
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', 
                        (LIVE_DATA['A'], LIVE_DATA['B'], LIVE_DATA['C'], 
                            LIVE_DATA['D'], LIVE_DATA['E'], 
                            LIVE_DATA['F'], LIVE_DATA['G'], LIVE_DATA['H']))

            conn.commit()

            print("updated db")

        except Exception as e:
            print(f"Error in db thread : {e}")
            conn.close()

        sleep(0.25)

thread1 = threading.Thread(target=fcDataExtract)
thread2 = threading.Thread(target=dataUpdateInDB)

thread1.start()
thread2.start()

thread1.join()
thread2.join()




master.close()
