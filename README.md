# mqtt-2-discord
Daemon to send messages to Discord from MQTT.

This is particularly useful when integrated into your applications and scripts.

PROJECT STATUS: BETA-RELEASE

KNOWN BUGS:
- Service file is misconfigured
- Minimal error correction

THINGS TO DO:
* Add multiple mqtt server support
* Export requirements.txt
* Central log for all modules

PRE-REQUISITES

    You need Python 3, plus the following packages
    
    sudo apt-get install python3-pip
    sudo apt-get install python3-setuptools
    sudo apt-get install python3-wheel

INSTALLATION

    sudo adduser --system --home /opt/modules --group mqtt2dis
    sudo -u mqtt2dis bash
    cd /opt/modules
    git clone https://github.com/ReuschelCGN/mqtt-2-discord.git .
    python3 -m venv venv
    . venv/bin/activate
    pip install wheel
    pip install paho-mqtt
    pip install discord-webhook

Copy example config and adjust settings:

    cp config.ini.example config.ini
    nano config.ini

Try if everything works, deactivate venv, leave bash:

    python mqtt-2-discord.py
    deactivate
    exit
    
CONFIGURATION

    First obtain your webhook from discord:
    - Open the desired server and select or create a channel
    - Click settings "cog"
    - Navigate to "Webhooks"
    - Create a webhook
        - Give it a name and an icon/image
        - Copy the Webhook URL
        - Press Save

    Now edit/create a config.ini file:
    sudo nano /opt/modules/mqtt-2-discord/config.ini
    
    Add an optional section [MQTT] (case sensitive) if your MQTT server is located on a different server, you have changed the port number or have configured authentication:
    
        [MQTT]
        host=127.0.0.1
        port=1883
        username=MY-USERNAME
        password=MY-PASSWORD
        
    To create an alert topic in MQTT: Add a section (The name does not matter) with two keys "topic" and "webhook"
    
        [Alerts]
        topic=messages/alerts
        webhook=https://discord.com/api/webhooks/AAAAAAAAAAAAAAAAAA/AAAAAAAAAAAAAAAAAA

TESTING

    cd /opt/modules
    venv/bin/python mqtt-2-discord/mqtt-2-discord.py

    Send a message on your configured topic and it should be displayed in your Discord channel.

RUN AS A DEAMON

    cp /opt/modules/mqtt2discord.service /etc/systemd/system/
    sudo chmod u+rwx /etc/systemd/system/mqtt2discord.service
    sudo systemctl enable mqtt2discord
    sudo systemctl start mqtt2discord
