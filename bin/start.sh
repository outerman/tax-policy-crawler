basepath=$(cd `dirname $0`; pwd)
echo current path: $basepath
cd $basepath

echo starting...
cd ../
count=1
while true; do
    echo 'start for the ' + $count + ' round'
    /Library/Frameworks/Python.framework/Versions/3.6/bin/python3.6 entrypointEx.py
    count=$((count + 1))
done
echo "finished"