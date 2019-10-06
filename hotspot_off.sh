#!/bin/bash
echo "Running hotspot off"
sleep 2
sudo cp /home/pi/nhlscoreboard/dhcpcd.conf.connect /etc/dhcpcd.conf
sudo cp /home/pi/nhlscoreboard/wpa_supplicant.conf /etc/wpa_supplicant/wpa_supplicant.conf
sudo systemctl stop hostapd
sudo systemctl disable hostapd
sudo systemctl stop dnsmasq
sudo systemctl disable dnsmasq
sudo systemctl daemon-reload
sudo systemctl restart dhcpcd

