#!/bin/bash
# To start a minikube machine and run kubeflow in it
minikube start --cpus 4 --memory 8096 --disk-size=40g
eval $(minikube docker-env)
KFAPP=KF_APP1
KUBEFLOW_SRC=KF1
export KUBEFLOW_TAG=v0.4.1
mkdir ${KUBEFLOW_SRC}
cd ${KUBEFLOW_SRC}
curl https://raw.githubusercontent.com/kubeflow/kubeflow/${KUBEFLOW_TAG}/scripts/download.sh | bash
KUBEFLOW_REPO=~/${KUBEFLOW_SRC} ~/${KUBEFLOW_SRC}/scripts/kfctl.sh init ${KFAPP} --platform minikube
cd ${KFAPP}
~/${KUBEFLOW_SRC}/scripts/kfctl.sh generate all
~/${KUBEFLOW_SRC}/scripts/kfctl.sh apply all
kubectl config set-context $(kubectl config current-context) --namespace=kubeflow
