> https://deepflow.io/docs/zh/ce-install/single-k8s/

# 名词解释

* Flow: DeepFlow Agent 会维护每个 TCP 连接、每个应用协议 Request 的会话状态，称之为 
* vTap: 应该就是和 deepflow-agent 是1:1 对应的

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

* [debug info](https://github.com/deepflowio/deepflow/blob/main/server/controller/http/router/debug.go#L39-L57)

```
ip=10.224.0.26:20417
curl $ip/v1/agent-stats/10.3.0.91/
```

