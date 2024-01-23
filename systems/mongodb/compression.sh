#!/bin/sh

# THE FOLLOWING SCRIPT WILL PRINT STORAGE SIZE FOR D1, TO SHOW D2 UNCOMMENT THE LINES BELOW 
#!/bin/bash

mongo_database="db"
mongo_collection="d1"

sudo docker exec -it mongo mongosh --quiet d1 --eval 'db.d1.stats().storageSize'

