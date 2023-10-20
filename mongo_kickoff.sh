#!/bin/bash

sudo yum update -y
sudo amazon-linux-extras install docker -y
sudo service docker start
sudo usermod -a -G docker ec2-user
#docker version #you may need to restart ec2 for ec2-user to be able to run docker command
echo "docker engine install done!"

#pull mongoDB image
sudo docker pull mongo

#Run MongoDB Container
sudo docker run --name mongodb -d -e MONGO_INITDB_ROOT_USERNAME=myuser -e MONGO_INITDB_ROOT_PASSWORD=mypassword -p 5000:27017 mongo

#install python 3.8
#sudo amazon-linux-extras install python3.8 -y

#install pip
#python3 -m pip install --upgrade pip

#create python virtual env
#python3.8 -m venv vvenv
#source vvenv/bin/activate

#install the required python libraries
#pip install -r requirements.txt