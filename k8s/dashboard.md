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
