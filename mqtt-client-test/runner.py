import paho.mqtt.client as mqtt
import yaml
import socket
import time


cfg = ''
def server_program():
    # get the hostname
    host = socket.gethostname()
   # port = 5000  # initiate port no above 1024

    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, 0))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(2)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))
    while True:
        # receive data stream. it won't accept data packet greater than 1024 bytes
        data = conn.recv(1024).decode()
        if not data:
            # if data is not received break
            break
        print("from connected user: " + str(data))
        data = input(' -> ')
        conn.send(data.encode())  # send data to the client

    conn.close()  # close the connection


with open("../props/config.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("$SYS/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

# The program starts here


# 1 . Initiate a connection to the MQTT Broker
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect_async("localhost", 1883, 60)
client.loop_start()



print("Started connectiion with server - the program waits for 3 minutes")

time.sleep(180)
client.loop_end();
print("Stopping the program")






