import datetime 

data_src = open('./d1.csv')
data_target= open('d1-influxdb-narrow.csv','a')
head_line="# DDL\n CREATE DATABASE d1-narrow\n"
head_line2="# DML\n# CONTEXT-DATABASE: d1-narrow\n"
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
        c_index=2;
        while(c_index<102):
            value = columns[c_index]
            influx_line = "sensor,id_station="+id_station+",s=s"+str(c_index-2)+" value="+str(value.strip())+" "+date_str+"\n"
            # print(influx_line)
            data_target.write(influx_line)
            c_index=c_index+1
        if(index%1000==0):
            print(index)
        index=index+1
data_target.close()
data_src.close()
