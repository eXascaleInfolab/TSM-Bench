#!/bin/sh

# THE FOLLOWING SCRIPT WILL PRINT STORAGE SIZE FOR D1, TO SHOW D2 UNCOMMENT THE LINES BELOW 

current="$(pwd)"
sudo du -sh ./master_db/mydb
#sudo du -sh ./d2
