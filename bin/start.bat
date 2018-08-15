echo starting...
cd ../
set count=1

:start
    echo 'start for the ' + %count% + ' round'
    D:\Users\niu\AppData\Local\Programs\Python\Python37\python.exe entrypointLaw.py
    set count+=1
goto start
echo "finished"