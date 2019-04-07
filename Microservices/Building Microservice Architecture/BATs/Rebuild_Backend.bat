kubectl delete svc backend-service
kubectl delete deployments backend-deployment
SLEEP 20
docker rmi test-api
cd C:\Users\RKhatry\Dock\Django\TestAPI1
docker build -t test-api .
cd C:\Users\RKhatry\Dock\YAMLs
kubectl create -f Test3.yaml
cd C:\Users\RKhatry\Dock\BATs
pause