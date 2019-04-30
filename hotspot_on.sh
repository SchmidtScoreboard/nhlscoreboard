#!/bin/bash
sleep 2
sudo cp /home/pi/nhlscoreboard/dhcpcd.conf.hotspot /etc/dhcpcd.conf
sudo cp /home/pi/nhlscoreboard/dnsmasq.conf /etc/dnsmasq.conf
sudo cp /home/pi/nhlscoreboard/hostapd.conf /etc/hostapd/hostapd.conf
sudo cp /home/pi/nhlscoreboard/hostapd /etc/default/hostapd
sudo systemctl enable hostapd
sudo systemctl start hostapd
sudo systemctl enable dnsmasq
sudo systemctl start dnsmasq
sudo systemctl daemon-reload
sudo systemctl restart dhcpcd
sudo reboot

