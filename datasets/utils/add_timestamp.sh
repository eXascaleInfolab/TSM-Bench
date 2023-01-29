# awk -v date="$( date -d '2010/01/01' '+%s' )" '{print strftime("%Y-%m-%dT%H:%M",date)" "$0; date+=60}' alabama_weather.txt
# alabama_weather.txt

# wl -l Datasets/alabama_weather.csv
# wc -l Datasets/alabama_weather.csv
# python3 run_eval.py --dataset weather --rows 3000 --algorithm simple-queries --database extremedb
# less Datasets/alabama_weather_ori.txt
# man cut
# cd Datasets/
# cat alabama_weather_ori.txt | cut -d, -f1 > time.csv
# ls
# rm time.csv
# cat alabama_weather_ori.txt | cut -d, -f1 > time.csv &
# less time.csv
# cat alabama_weather_ori.txt | cut -d' ' -f1 > time.csv &
# wc -l alabama_weather.csv
# sed 's/,/ /g' alabama_weather.csv >resultfile &
# parse time.csv resultfile -d " " > finalfiles &
# less resultfile
# man parse
# paste time.csv resultfile -d " " > finalfiles &
# less finalfiles
# htop
# sudo apt install htop
# top
# jobs
# wc -l finalfiles
# head -n 1000000 finalfiles > alabama_weather.csv
# wc -l alabama_weather.csv
# less alabama_weather.csv
