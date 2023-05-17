# Internet_down
Simple down detector for Internet
This is a simplified version for someone wanting to know the startus of your Internet connectivity.
It can assist you when communicating with your ISP.
Detection is done by pinging 8.8.8.8 and a timeout is considered as interruption. Internet_down will send you an email when internet is restored after an interruption.
- Time stamp on when interrupted and when restored
- Duration of interruption
- Resolution i 1 minuted (easily modified)

Requirements Hardware:
- Raspberry Zero W (This assumes WiFi connection). Feel free to use any computer running Linux

Preparation
- Prepare your Pi (Raspberry Pi OS), configure WiFi and enable SSH. Easily done with Raspberry imager: https://www.raspberrypi.com/news/raspberry-pi-imager-imaging-utility/
- Power on the Pi and confirm you can connect by ssh
```ssh YOURUSERNAME@zero.local```

- Update the Pi

```sudo apt update```

```sudo apt upgrade```

```sudo apt install python3 python3-pip```

```sudo pip3 install ping3```

- Generate an app password if using 2fa
To generate an app password, go to your Google Account settings, navigate to the "Security" tab, and look for the "App passwords" section. Generate a new app password specifically for your Raspberry Pi application and use that in the sender_password variable.

- edit down_detector.py with ```nano down_detector.py``` . 

Note that you have to customize 3 lines: 
sender_email = "YOURSENDER@gmail.com", 
sender_password = "HERE_GOES_YOUR_GMAIL_PASSWORD_OR_APP_PASSWORD" &
receiver_email = "YOURRECIEVER@gmail.com"

- Run the script (you can chose just to run it och have it automatically run when the Pi boots)


```python3 down_detector.py```

- Setup to run as a service from boot (If you want to have it running automatically from boot)

```sudo nano /etc/systemd/system/down_detector.service```

Note that you have to customize following lines: ExecStart=/usr/bin/python3 /home/YOURUSER/down_detector.py
WorkingDirectory=/home/YOURUSER, 
StandardOutput=inherit, 
StandardError=inherit, 
Restart=always, 
User=YOURUSER

- Enable the service & Reboot

```sudo systemctl enable down_detector.service```

```sudo reboot```

- Testing:
Once Pi has rebooted, confirm that it creates down_log.txt. Disconnect your router, wait for a minute and confirm that you get a mail

