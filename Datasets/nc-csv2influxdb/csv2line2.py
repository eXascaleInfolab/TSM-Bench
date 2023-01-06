#!/usr/bin/python
import sys, getopt
import progressbar
import time
import pandas as pd
import datetime

def main(argv):
   dbname = 'import'
   inputfile = 'data.csv'
   outputfile = 'import.txt'

   usage = 'csv2line.py -d <dbname> -i <inputfile> -o <outputfile>'
   try:
      opts, args = getopt.getopt(argv,"hd:i:o:",["db=","ifile=","ofile="])
   except getopt.GetoptError:
      print (usage)
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print (usage)
         sys.exit()
      elif opt in ("-d", "--db"):
         dbname = arg.replace(" ", "_")
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg

   convert(dbname, inputfile, outputfile)


def convert(dbname, inputfile, outputfile):
  # Convert csv's to line protocol
  '''
  https://docs.influxdata.com/influxdb/v1.6/write_protocols/line_protocol_tutorial/
  weather,location=us-midwest temperature=82 1465839830100400200
    |    -------------------- --------------  |
    |             |             |             |
    |             |             |             |
  +-----------+--------+-+---------+-+---------+
  |measurement|,tag_set| |field_set| |timestamp|
  +-----------+--------+-+---------+-+---------+
  '''
  start_time = time.time()
  
  # Read csv
  bar = progressbar.ProgressBar(maxval=100, widgets=[progressbar.Bar('=', '[', ']'), 'Read csv file ', progressbar.Percentage()])
  bar.start()
  df_full = pd.read_csv(inputfile, sep=' ')
  bar.finish()

  # Export to file
  theImportFile = open(outputfile, 'w')
  # Write header file
  theImportFile.write('''
# DDL
CREATE DATABASE %s
# DML
# CONTEXT-DATABASE: %s
''' % (dbname, dbname))

  # Measurement
  bar = progressbar.ProgressBar(maxval=len(df_full), widgets=[progressbar.Bar('=', '[', ']'), 'Processing ', progressbar.Percentage()])
  bar.start()

  seen = {}
  print(df_full.head())
  for d in range(len(df_full)):
    bar.update(d+1)
    print(int(datetime.datetime.strptime(df_full["time"][d], "%Y-%m-%dT%H:%M:%S").timestamp()))
    item = "datapoints" \
           + ",id_station=%s" % int(str(df_full["id_station"][d]).replace(" ", "_")) \
           + " " \
           + "temperature=%s" % float(str(df_full["temperature"][d]).replace(" ", "_")) \=
           + ",oxygen=%s" % float(str(df_full["oxygen"][d])) \
           + ",oxygen_saturation=%s" % float(df_full["oxygen_saturation"][d]) \
           + " " \
           + str(int(datetime.datetime.strptime(df_full["time"][d], "%Y-%m-%dT%H:%M:%S").timestamp())*1000000000)
           # + str(df_full["time"][d])

    if item in seen: continue
    theImportFile.write("%s\n" % item)
    seen[item] = 1

  bar.finish()

  # Print log
  print ('---Converting finished !!! (%s seconds)---' % (time.time() - start_time))
  print ('\t-Dabase name is: %s' % dbname)
  print ('\t-Input file is: %s' % inputfile)
  print ('\t-Output file is: %s' % outputfile)

if __name__ == "__main__":
   main(sys.argv[1:])
