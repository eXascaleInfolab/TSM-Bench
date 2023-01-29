foo="paste -d' ' "
for i in `seq 0 99`;
do
foo="${foo} fake_long${i}.csv"
done
foo="${foo} > fake_long_complete.csv"
echo $foo
eval $foo
