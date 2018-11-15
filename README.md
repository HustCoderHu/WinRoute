# WinRoute
Use Python to Manage Windows Route Table with IP Helper Functions（iphlpapi.dll）
通过系统 cmd 增删路由，速度无法忍受，期间cpu占用也非常高

python 版本 3.x

# 文件说明
## prepare_ip
- 下载 anpic 的 ip 文件
- 分析 ip 文件，通过限制掩码长度，限制路由的条数 (使用了 chinaip 的代码)

## winroute
封装了增加、删除路由的 winapi

# route_op
读取 prepare 生成的文件(里的路由)，调用 Winroute 的方法增减系统路由(管理员权限)

需要设置
- 默认网关, 及对应接口序号
- vpn 网关, 及对应接口序号

接口序号通过 CMD 执行 `route print` 查看接口列表的第一列

# 耗时测试

路由条数 | 增加/s | 删除/s
-|-|-
5086 | 0.1369 | 0.0928

# reference
<https://github.com/liudongmiao/chinaip>  
<https://github.com/HustCoderHu/myNotes/blob/master/vpn/winroute.md>  

Python调用IP Helper Functions（iphlpapi.dll），实现对Windows路由表的操作（参考了MSDN及部分网络代码）
- 使用printroute，打印输出当前win路由表(IPv4)
- 使用getroute，得到当前win路由表(IPv4)
- 使用CreateIpForwardEntry，添加新的路由，使用参数dwForwardDest,dwForwardMask,dwForwardNextHop=None,dwForwardMetric=0,ForwardIfIndex=None，对应目标IP，掩码，网关（不提供与默认路由相同），跃点数（不提供与默认路由相同），接口（不提供与默认路由相同）