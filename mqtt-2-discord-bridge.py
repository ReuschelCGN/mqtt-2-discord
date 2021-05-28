# Installing dependencies
# pip install requests
# pip install paho-mqtt
# pip install configparser
# pip install discord-webhook

import logging, sys
import requests
import paho.mqtt.client as mqtt
import configparser
from discord_webhook import DiscordWebhook
from datetime import datetime

#LOG_LEVEL = logging.INFO
APPNAME = 'MQTT-2-Discord'
LOG_LEVEL = logging.DEBUG
LOG_FILE = "logs/m2dlogs.log"
LOG_FORMAT ="%(asctime)s %(levelname)s %(message)s"

# INITIALISE CONFIG AND LOGGING
config = configparser.ConfigParser()
logging.basicConfig( filename=LOG_FILE, format=LOG_FORMAT, level=LOG_LEVEL )
logging.info( "STARTING" )
topics = {}

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    logging.debug( "Connected with result code "+str(rc) )
    webhook_url = config['DISCORD']['DISCORD_WEBHOOK']
    payload = str( "MQTT 2 Discord connected with result code "+str(rc) )
    webhook = DiscordWebhook( url=webhook_url, content=payload )
    webhook.execute()

    # Subscribe to topics
    for mqtttopic in topics:
        print("* Subscribing to topic: "+mqtttopic )
        client.subscribe(mqtttopic)

def on_message(client, userdata, msg):
    try:
        payload = str(':warning: Message form Topic: ' + msg.topic + ':\nStatus/Msg: ' + msg.payload.decode('utf-8'))
        topic = msg.topic
        print( "MSGTOPIC: "+topic )
        if topic in topics:
            webhook_url = topics[topic]
            print( "WEBHOOK: "+webhook_url )
            webhook = DiscordWebhook( url=webhook_url, content=payload )
            webhook.execute()
    except Exception as e:
        print(e)
        
def main():
    config.read('config.ini')
    
    # Default MQTT section
    if not 'MQTT' in config:
        config['MQTT']={}
    host = config['MQTT']
    
    # Get Topics
    for key in config.sections():
        section = config[key]
        if 'mqtttopic' in section and 'dwebhook' in section:
            topics[section['mqtttopic']]= section['dwebhook']

    # Abort if there are no topics!
    if len(topics)==0:
        print( "Quitting because no topics are defined" )
        logging.critical( "No topics are defined" )
        sys.exit()
    
    # MQTT
    client = mqtt.Client( APPNAME, clean_session=False )
    hostname = host.get('broker-url')
    hostport = host.getint('broker-port')
    if 'mqtt-username' in host:
        username = host.get('mqtt-username')
        password = host.get('mqtt-password')
        print( "- MQTT: "+username+"@"+hostname+":"+str(hostport) )
        client.username_pw_set( username, password )
    else:
        print( "- MQTT: "+hostname+":"+str(hostport) )
    try:
        client.connect( hostname, hostport , 60 )
    except Exception as e:
        logging.critical( str(e) )
        print( e )
        sys.exit()

    client.on_connect = on_connect
    client.on_message = on_message
    client.loop_forever()
    client.disconnect()

if __name__=="__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("")
        print( "Terminated by user" )
        sys.exit()
