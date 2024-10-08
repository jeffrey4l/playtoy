# down binaries

> 版本信息从 https://github.com/kubesphere/kubekey/releases 获取

```
mkdir -p kk
cd kk
version=v3.1.0-alpha.7
wget https://github.ccommon.openldapom/kubesphere/kubekey/releases/download/$version/kubekey-$version-linux-amd64.tar.gz
tar xvf kubekey-$version-linux-amd64.tar.gz

yum install -y conntrack socat ebtables ipset ipvsadm
```

# config

> * https://github.com/kubesphere/kubekey/blob/master/api/v1beta1/kkcluster_types.go
> * https://github.com/kubesphere/kubekey/blob/release-2.2/docs/config-example.md

```bash
ip1=10.3.0.91
ip2=10.3.0.92
ip3=10.3.0.93

cat <<EOF > cluster.yml
apiVersion: kubekey.kubesphere.io/v1alpha2
kind: Cluster
metadata:
  name: master.com
spec:
  hosts:
      - {name: cloud, address: $ip1, internalAddress: $ip1, privateKeyPath: ~/.ssh/id_rsa}
      - {name: edge2, address: $ip2, internalAddress: $ip2, privateKeyPath: ~/.ssh/id_rsa}
      - {name: edge3, address: $ip3, internalAddress: $ip3, privateKeyPath: ~/.ssh/id_rsa}
  roleGroups:
    etcd:
    - cloud
    master:
    - cloud
    worker:
    - cloud
    - edge2
    - edge3
  controlPlaneEndpoint:
    ## Internal loadbalancer for apiservers
    # internalLoadbalancer: ""
    domain: vip.master.com
    # address: "172.20.163.65"
    port: 6443
  kubernetes:
    version: v1.27.2
    clusterName: master.com
    containerManager: containerd
    DNSDomain: master.com
    imageRepo: kubesphere
    maxPods: 110
    featureGates:
      CSIStorageCapacity: true
      RotateKubeletServerCertificate: true
      ReadWriteOncePod: true
    kubeletArgs:
    - --authentication-token-webhook=true
    - --authorization-mode=Webhook
  network:
    plugin: "flannel"
    KubeServiceCIDR: "10.255.0.0/18"
    KubePodsCIDR: "10.224.0.0/18"
  registry:
    privateRegistry: ""
    registryMirrors: ["https://hub-mirror.c.163.com"]
    insecureRegistries: ["0.0.0.0/0"]
  addons: []
---
apiVersion: installer.kubesphere.io/v1alpha1
kind: ClusterConfiguration
metadata:
  name: ks-installer
  namespace: kubesphere-system
  labels:
    version: v3.4.1
spec:
  metrics_server:
    enabled: true
EOF
```

```
./kk create cluster -f cluster.yml
```

# add nodes

> [office doc](https://kubesphere.io/docs/v3.4/installing-on-linux/cluster-operation/add-new-nodes/)

```
./kk add nodes -f cluster.yaml
```


# openyurt

```bash
version=v1.4.0
wget https://github.com/openyurtio/openyurt/releases/download/$version/yurtadm-$version-linux-amd64.tar.gz
tar xvf yurtadm-$version-linux-amd64.tar.gz
```

# enable metric server
