#!/bin/sh

# THE FOLLOWING SCRIPT WILL SETUP AND LOAD D1, TO LOAD D2 UNCOMMENT THE LINES BELOW 


# curl -G --data-urlencode "query= DROP TABLE IF EXISTS d1temp; \
# 		" http://localhost:9000/exp

# 		" http://localhost:9000/exp


curl -G --data-urlencode "query= DROP TABLE IF EXISTS d1temp; \
                " http://localhost:9000/exec

curl -G --data-urlencode "query= DROP TABLE IF EXISTS d1; \
                " http://localhost:9000/exec


ABSOLUTE_PATH=$(readlink -f "../../datasets")

curl -G --data-urlencode "query= COPY d1temp FROM '$ABSOLUTE_PATH/d1.csv'; \
                " http://localhost:9000/exec

curl -G --data-urlencode "query= CREATE TABLE d1 AS ( SELECT cast(time AS timestamp) ts, cast(id_station AS symbol) id_station, s0, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14, s15, s16, s17, s18, s19, s20, s21, s22, s23, s24, s25, s26, s27, s28, s29, s30, s31, s32, s33, s34, s35, s36, s37, s38, s39, s40, s41, s42, s43, s44, s45, s46, s47, s48, s49, s50, s51, s52, s53, s54, s55, s56, s57, s58, s59, s60, s61, s62, s63, s64, s65, s66, s67, s68, s69, s70, s71, s72, s73, s74, s75, s76, s77, s78, s79, s80, s81, s82, s83, s84, s85, s86, s87, s88, s89, s90, s91, s92, s93, s94, s95, s96, s97, s98, s99 FROM 'd1temp' ), index (id_station) timestamp(ts) PARTITION BY MONTH; \
                " http://localhost:9000/exec

curl -G --data-urlencode "query= DROP TABLE d1temp; \
                " http://localhost:9000/exec



sh compression.sh

## uncoment the following for D2 ##
###################################
# echo "start loading!"

#curl -G --data-urlencode "query= DROP TABLE IF EXISTS d2temp; \
#                " http://localhost:9000/exec

#curl -G --data-urlencode "query= DROP TABLE IF EXISTS d2; \
#                " http://localhost:9000/exec


#ABSOLUTE_PATH=$(readlink -f "../../datasets")

#curl -G --data-urlencode "query= COPY d2temp FROM '$ABSOLUTE_PATH/d2.csv'; \
#                " http://localhost:9000/exec

#curl -G --data-urlencode "query= CREATE TABLE d2 AS ( SELECT cast(time AS timestamp) ts, cast(id_station AS symbol) id_station, s0, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14, s15, s16, s17, s18, s19, s20, s21, s22, s23, s24, s25, s26, s27, s28, s29, s30, s31, s32, s33, s34, s35, s36, s37, s38, s39, s40, s41, s42, s43, s44, s45, s46, s47, s48, s49, s50, s51, s52, s53, s54, s55, s56, s57, s58, s59, s60, s61, s62, s63, s64, s65, s66, s67, s68, s69, s70, s71, s72, s73, s74, s75, s76, s77, s78, s79, s80, s81, s82, s83, s84, s85, s86, s87, s88, s89, s90, s91, s92, s93, s94, s95, s96, s97, s98, s99 FROM 'd1temp' ), index (id_station) timestamp(ts) PARTITION BY MONTH; \
#                " http://localhost:9000/exec

#curl -G --data-urlencode "query= DROP TABLE d2temp; \
#                " http://localhost:9000/exec

