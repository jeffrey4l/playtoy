```bash
helm repo add rancher-latest https://releases.rancher.com/server-charts/latest

# 安装 cert-manage
V=v1.13.3
kubectl create namespace cattle-system
kubectl apply -f \
  https://github.com/cert-manager/cert-manager/releases/download/$V/cert-manager.crds.yaml

helm repo add jetstack https://charts.jetstack.io

helm repo update

helm install cert-manager jetstack/cert-manager \
  --namespace cert-manager \
  --create-namespace
```



```bash
# 安装 rancher
helm upgrade -i rancher rancher-latest/rancher --namespace cattle-system \
    --create-namespace \
    --reuse-values \
    --set hostname=10.3.0.91.nio.io \
    --set bootstrapPassword=admin \
    --set ingress.tls.source=secret \
    --set replicas=1

kubectl -n cattle-system patch svc rancher --type=json -p '
    [{"op":"replace","path":"/spec/type","value":"NodePort"},
     {"op":"replace","path":"/spec/ports/0/nodePort","value":30444}]'
```

```bash
# 删除
helm -n cattle-system uninstall rancher
```

Tv5byTH8AGYBX1fj

# add nodes

```bash
# add CA
kubectl -n cattle-system create secret generic \
  tls-ca-additional \
  --from-file=ca-additional.pem=cabundle
```

```diff
--- d.yaml	2024-02-07 15:16:49.251000000 +0800
+++ c.yaml	2024-02-07 15:11:47.222000000 +0800
@@ -173,7 +173,12 @@
       containers:
         - name: cluster-register
           imagePullPolicy: IfNotPresent
+          command:
+             - bash
+             - -c
+             - "update-ca-certificates && run.sh"
           env:
+          - name: SSL_CERT_DIR
           - name: CATTLE_IS_RKE
             value: "false"
           - name: CATTLE_SERVER
@@ -197,11 +202,17 @@
           - name: cattle-credentials
             mountPath: /cattle-credentials
             readOnly: true
+          - name: ca
+            mountPath: /etc/pki/trust/anchors/ca-additional.pem
+            subPath: ca-additional.pem
       volumes:
       - name: cattle-credentials
         secret:
           secretName: cattle-credentials-9d42989
           defaultMode: 320
+      - name: ca
+        secret:
+         secretName: tls-ca-additional
   strategy:
     type: RollingUpdate
     rollingUpdate:
```

