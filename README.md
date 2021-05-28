# mqtt-2-discord-bridge
Modul to send messages from MQTT to Discord.

This is particularly useful when integrated into your applications and scripts.

INSTALLATION

1. Clone repository git clone `https://github.com/ReuschelCGN/mqtt-2-discord`
2. Copy content of docker-compose-yml into your running docker-compose.yml
3. Copy config `cp config.ini-example config.ini`
4. Fill out config.ini
5. `sudo docker-compose build mqtt2discord`
6. `sudo docker-compose up -d mqtt2discord`

get logs:
`sudo docker-compose logs -f -t mqtt2discord`

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
    
   To create an alert topic in config.ini, add a section (The name does not matter) with two keys "mqtttopic" and "dwebhook"
    
        [STATUS1]
        mqtttopic = messages/status
        dwebhook = https://discord.com/api/webhooks/AAAAAAAAAAAAAAAAAA/AAAAAAAAAAAAAAAAAA

    Send a message on your configured topic and it should be displayed in your Discord channel.
