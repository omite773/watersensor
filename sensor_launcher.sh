#Start sequence which will start the sensor scripts after a reboot

#Detaching the USB stick
#Sudo umount /media/pi/KINGSTON/ &

#sleep 2

#Turning off USB hubs
sudo sh /home/pi/watersensor/hub-off.sh &

#sleep 7

#Starting measurements and logging script
#sudo python /home/pi/watersensor/data_logger.py &

#sleep 2
