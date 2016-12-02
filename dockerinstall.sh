#!/bin/bash

sudo apt install apt-transport-https ca-certificates

sudo apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D

echo "deb https://apt.dockerproject.org/repo ubuntu-xenial main" | sudo tee /etc/apt/sources.list.d/docker.list

sudo apt update
sudo apt -y install docker-engine
sudo usermod $USER -aG docker

echo ""
echo "############################################"
echo "# Note: relogin to run docker without sudo #"
echo "############################################"
