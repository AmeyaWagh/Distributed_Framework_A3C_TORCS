#!/bin/bash
clear
echo "--------------------------Installing dependencies for TORCS----------------------------"
echo "Do you want to install python dependencies for this project from requirements.txt?[Y or n]"
read var
if  [ "$var" = "Y" ] || [ "$var" = "y" ]
then
    echo "Installing project dependencies from requirements.txt"
    pip3 install -r requirements.txt
    apt-get install python3-tk
else
    echo "Skipping installion of dependencies"
fi


# #plib installation
# echo "Do you want to install plib?[Y or n]"
# read var
# if  [ "$var" = "Y" ] || [ "$var" = "y" ]
# then
#     echo "Installing plib"
# 	cd plib-1.8.5/
# 	./configure
# 	make
# 	make check
# 	make install
# else
#     echo "Skipping download"
# fi

#Torcs installation
echo "Torcs installation. continue?[Y or n]"
read var
if  [ "$var" = "Y" ] || [ "$var" = "y" ]
then
    echo "Installing torcs from apt-get"
    # cd ../
    # apt-get update
    apt-get install torcs
else
    echo "Skipping installation"
fi


#Gym-Torcs installation
echo "Gym-TORCS installation. continue?[Y or n]"
read var
if  [ "$var" = "Y" ] || [ "$var" = "y" ]
then
    echo "Installing plib"
    # cd ../
    git clone https://github.com/ugo-nama-kun/gym_torcs.git
    cd gym_torcs/vtorcs-RL-color
    sudo apt-get install libglib2.0-dev  libgl1-mesa-dev libglu1-mesa-dev  freeglut3-dev  libplib-dev  libopenal-dev libalut-dev libxi-dev libxmu-dev libxrender-dev  libxrandr-dev libpng12-dev 
	./configure
	make
	make install
	make datainstall

else
    echo "Skipping download"
fi