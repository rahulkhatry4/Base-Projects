kubectl delete svc frontend
kubectl delete deployments frontend
SLEEP 10
docker rmi test-front
cd C:\Users\RKhatry\Dock\Dash\TestFront1
docker build -t test-front .
cd C:\Users\RKhatry\Dock\YAMLs
kubectl create -f Test2.yaml
cd C:\Users\RKhatry\Dock\BATs
pause