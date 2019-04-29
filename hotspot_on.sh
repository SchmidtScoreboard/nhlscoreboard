#!/bin/bash
sudo cp /etc/dhcpcd.conf.hotspot /etc/dhcpcd.conf
sudo systemctl enable hostapd
sudo systemctl start hostapd
sudo systemctl enable dnsmasq
sudo systemctl start dnsmasq
sudo systemctl daemon-reload
sudo systemctl restart dhcpcd
sudo reboot

