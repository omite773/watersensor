########## Function which copies the data_log file onto a USB ##########
#echo '1-1' | sudo tee /sys/bus/usb/drivers/usb/bind #power on USB

#Let start and mount for atleast 5 sec
sleep 8
#Copy contents

sudo cp /home/pi/watersensor/data_logs/* /media/pi/KINGSTON/
sleep 4

sudo umount /media/pi/KINGSTON/
sleep 2

#echo '1-1' | sudo tee /sys/bus/usb/drivers/usb/unbind  #power off usb
