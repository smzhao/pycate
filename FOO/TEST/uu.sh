
for k in $( seq 1 10000 )
do
    nosetests  testLogin.py
    sleep 0.01
    echo $k
done
