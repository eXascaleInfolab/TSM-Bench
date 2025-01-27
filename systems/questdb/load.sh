#!/bin/sh

sh launch.sh &
sleep 30

dataset="d1"
if [ $# -ge 1 ]; then
    dataset="$1"
fi
echo "loading $dataset"


# dataset != d2
if [ $dataset != "d2" ]; then
    echo "start loading!"

    curl -G --data-urlencode "query= DROP TABLE IF EXISTS ${dataset}temp; \
                    " http://localhost:9000/exec

    curl -G --data-urlencode "query= DROP TABLE IF EXISTS $dataset; \
                    " http://localhost:9000/exec

curl -G --data-urlencode "query= DROP TABLE IF EXISTS ${dataset}temp; \
                " http://localhost:9000/exec

curl -G --data-urlencode "query= DROP TABLE IF EXISTS $dataset; \
                " http://localhost:9000/exec

start_time=$(date +%s.%N)

ABSOLUTE_PATH=$(readlink -f "../../datasets")
#ABSOLUTE_PATH=$(echo $ABSOLUTE_PATH | sed 's/\//\\\//g')

curl -G --data-urlencode "query= COPY ${dataset}temp FROM '$ABSOLUTE_PATH/$dataset.csv'; \
                " http://localhost:9000/exec

curl -G --data-urlencode "query= CREATE TABLE $dataset AS ( SELECT cast(time AS timestamp) ts, cast(id_station AS symbol) id_station, s0, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14, s15, s16, s17, s18, s19, s20, s21, s22, s23, s24, s25, s26, s27, s28, s29, s30, s31, s32, s33, s34, s35, s36, s37, s38, s39, s40, s41, s42, s43, s44, s45, s46, s47, s48, s49, s50, s51, s52, s53, s54, s55, s56, s57, s58, s59, s60, s61, s62, s63, s64, s65, s66, s67, s68, s69, s70, s71, s72, s73, s74, s75, s76, s77, s78, s79, s80, s81, s82, s83, s84, s85, s86, s87, s88, s89, s90, s91, s92, s93, s94, s95, s96, s97, s98, s99 FROM 'd1temp' ), index (id_station) timestamp(ts) PARTITION BY MONTH; \
                " http://localhost:9000/exec

curl -G --data-urlencode "query= DROP TABLE ${dataset}temp; \
                " http://localhost:9000/exec



else
    echo "start loading!"

    curl -G --data-urlencode "query= DROP TABLE IF EXISTS d2temp; \
                    " http://localhost:9000/exec

    curl -G --data-urlencode "query= DROP TABLE IF EXISTS d2; \
                    " http://localhost:9000/exec


    ## insert it in bacthes with d2_1_4, d2_2_4 , d2_3_4, d2_4_4
    ## d2_1_4
    ABSOLUTE_PATH=$(readlink -f "../../datasets")
    #ABSOLUTE_PATH=$(echo $ABSOLUTE_PATH | sed 's/\//\\\//g')

    curl -G --data-urlencode "query= COPY d2temp FROM '$ABSOLUTE_PATH/d2_1_4.csv'; \
                    " http://localhost:9000/exec
    curl -G --data-urlencode "query= COPY d2temp FROM '$ABSOLUTE_PATH/d2_2_4.csv'; \
                    " http://localhost:9000/exec
    curl -G --data-urlencode "query= COPY d2temp FROM '$ABSOLUTE_PATH/d2_3_4.csv'; \
                    " http://localhost:9000/exec
    curl -G --data-urlencode "query= COPY d2temp FROM '$ABSOLUTE_PATH/d2_4_4.csv'; \
                    " http://localhost:9000/exec

    #curl -G --data-urlencode "query= CREATE TABLE d2 AS ( SELECT cast(time AS timestamp) ts, cast(id_station AS symbol) id_station, s0, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11 FROM 'd2temp' ), index (id_station) timestamp(ts) PARTITION BY MONTH; \
     #               " http://localhost:9000/exec

	curl -G --data-urlencode "query= CREATE TABLE d2 AS ( SELECT cast(f0 AS timestamp) ts, cast(f1 AS symbol) id_station, f3, f4, f5, f6, f7, f8, f9, f10, f11, f12, f13, f14, f15, f16, f17, f18, f19, f20, f21, f22, f23, f24, f25, f26, f27, f28, f29, f30, f31, f32, f33, f34, f35, f36, f37, f38, f39, f40, f41, f42, f43, f44, f45, f46, f47, f48, f49, f50, f51, f52, f53, f54, f55, f56, f57, f58, f59, f60, f61, f62, f63, f64, f65, f66, f67, f68, f69, f70, f71, f72, f73, f74, f75, f76, f77, f78, f79, f80, f81, f82, f83, f84, f85, f86, f87, f88, f89, f90, f91, f92, f93, f94, f95, f96, f97, f98, f99, f100, f101 FROM 'd2temp' ), index (id_station) timestamp(ts) PARTITION BY DAY; \
                    " http://localhost:9000/exec


	curl -G --data-urlencode "query= DROP TABLE d2temp; \
                " http://localhost:9000/exec


fi # end if dataset != d2

end_time=$(date +%s.%N)
elapsed_time=$(echo "$end_time - $start_time" | bc)
elapsed_time=$(printf "%.2f" "$elapsed_time")


compression="$(sh compression.sh $dataset | tail -n 1)"
compression=$(echo "$compression" | grep -o '[0-9]*') # Extract the numeric part
compression=$(printf "%.2f" "$(echo "$compression / 1024 / 1024" | bc -l)") # Convert to GB

echo "$dataset ${elapsed_time}s ${compression}GB" >> time_and_compression.txt

echo $elapsed_time
echo "database compression"



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


