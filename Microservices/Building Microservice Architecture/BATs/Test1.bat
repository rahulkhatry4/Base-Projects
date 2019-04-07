REM docker rmi test-api

REM cd C:\Users\RKhatry\Dock\Django\TestAPI1

REM docker build -t test-api .

REM docker rmi test-front

REM cd C:\Users\RKhatry\Dock\Dash\TestFront1

REM docker build -t test-front .

cd C:\Users\RKhatry\Dock\YAMLs

kubectl create -f Test3.yaml
kubectl create -f Test2.yaml

cd C:\Users\RKhatry\Dock\BATs

pause