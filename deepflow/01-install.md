> https://deepflow.io/docs/zh/ce-install/single-k8s/

# 名词解释

* Flow: DeepFlow Agent 会维护每个 TCP 连接、每个应用协议 Request 的会话状态，称之为 
* vTap: 应该就是和 deepflow-agent 是1:1 对应的



# install

```bash
helm repo add deepflow https://deepflowio.github.io/deepflow
helm repo search deepflow
helm search repo -l  deepflow/deepflow

cat << EOF > values-custom.yaml
global:
  allInOneLocalStorage: true
EOF

helm install deepflow -n deepflow deepflow/deepflow --create-namespace   -f values-custom.yaml
```

```
```



# listen port

server:
* controller: 20417
* grpc_port: 20035
* querier: 20416
  * deepflow-app: 20418
* Roze:
  * listen: 20106
* ingester:
  * listen: 20033

deepflow-app:

* 20418

agent 的连接关系

```
      8 10.224.0.10:20033
      1 10.224.0.10:20035
     10 10.255.0.1:443
```

```
go install github.com/gogo/protobuf/protoc-gen-gogo@latest 


grpcurl -import-path ./message/ -proto trident.proto    -plaintext   10.255.10.19:20035 trident.Synchronizer.Sync
```

* `kubernetes_cluster_id` 来自于 `ca` [文件的 md5 值进行的计算](https://github.com/deepflowio/deepflow/blob/main/server/controller/common/uid.go#L64-L84)
  * 一个值的例子是 `Field(45): kubernetes_cluster_id = d-Oo57bdJbXI (string)`

# agent

agent 的子进程

* synchronizer
* domain_name_listener
* cgroup_controller
  * when not running in container
* guard
* monitor
* platform_synchronizer
  * 拿着 libvirt xml 的启动
  * managed 模式下，启动
* libvirt_xml_extractor
* sidecar_poller
  * when using in `sidecar_mode`
* api_watcher

# server api

* debug apis
  * https://github.com/deepflowio/deepflow/blob/main/server/controller/http/router/debug.go#L39-L57)


```
ip=deepflow-server.deepflow:20417
curl $ip/v1/agent-stats/10.3.0.91/
```

```
task: 算是一个抓取元数据的业务
```



# REF

* https://mp.weixin.qq.com/s/GvUwamT-1VYHZQW34JBdow

```
deepflow-ctl 是个 server 的 client 和上面的
./deepflow-ctl --api-port 20417 agent list
```