# 为什么不能直接挂载到 /


会报下面的错误

```
  Warning  Failed     11s (x3 over 32s)  kubelet            Error: Error response from daemon: invalid volume specification: '/var/lib/kubelet/pods/a613af35-e393-430f-92bb-70bfbdb57fba/volumes/kubernetes.io~local-volume/pvc-82bc050c-e70a-48b4-87bf-5a35e2bb95e3:/': invalid mount config for type "bind": invalid specification: destination can't be '/'
  Normal   Pulled     11s                kubelet            Successfully pulled image "ealen/echo-server:latest" in 3.894s (3.894s including waiting)
```

* secret mount:  Invalid specification: destination can't be '/' · Issue #44759 · kubernetes/kubernetes
  * https://github.com/kubernetes/kubernetes/issues/44759

这里好像没有解?
