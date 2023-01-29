import datetime

data_src = open('./d1.csv')
data_target= open('d1-influxdb.csv','a')
head_line="# DDL\n CREATE DATABASE d1\n"
head_line2="# DML\n# CONTEXT-DATABASE: d1\n"
data_target.write(head_line)
data_target.write(head_line2)
index=1
line = data_src.readline()
while True:
    line = data_src.readline()
    if not line:
        break
    if (line.strip() != ''):
        columns = line.split(',')
        date_str=columns[0]
        date_str = str(int(datetime.datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S").timestamp()) * 1000)
        id_station = columns[1]
        influx_line = "sensor,id_station="+id_station + " "
        for i in range(100):
            influx_line += "s"+str(i)+"=" + str(columns[i+2]) 
            if i < 99: 
                influx_line += ','
            # print(influx_line)
        influx_line = influx_line[:-1] + " " + date_str + '\n'
        #print(influx_line)
        data_target.write(influx_line)
        if(index%1000==0):
            print(index)
            #print(influx_line)
        index=index+1
data_target.close()
data_src.close()
