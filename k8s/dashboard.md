```bash
kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.7.0/aio/deploy/recommended.yaml

# use nodePort service
kubectl -n kubernetes-dashboard patch svc kubernetes-dashboard --type=json -p '
    [{"op":"replace","path":"/spec/type","value":"NodePort"},
     {"op":"replace","path":"/spec/ports/0/nodePort","value":30443}]'
```

配置 Token

```
kubectl create serviceaccount user-admin -n kube-system
kubectl create clusterrolebinding user-admin --clusterrole=cluster-admin --serviceaccount=kube-system:user-admin
kubectl create token user-admin -n kube-system --duration=999999h
```

## metric server

```
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
```



# kubesphere

可以使用 kubekey 来直接安装，也可以



```bash
V=v3.4.0
kubectl apply -f https://github.com/kubesphere/ks-installer/releases/download/$V/kubesphere-installer.yaml

kubectl apply -f https://github.com/kubesphere/ks-installer/releases/download/$V/cluster-configuration.yaml
```

