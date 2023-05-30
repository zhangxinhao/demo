# Go

## 环境配置

```shell
# 通过.zshrc配置GOAPATH
# 全局GOPATH
go env -w GOPATH=/Users/zhangxinhao/go
# 项目GOPATH
go env -w GOPATH=/Users/zhangxinhao/code/test/demo/go

# GO111MODULE
go env -w GO111MODULE=on
```

```shell
# go work
cd /Users/zhangxinhao/code/test/demo/go/src
go work init

go work use hello
go work use greet
```