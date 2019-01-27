# WinRoute
Use Python to Manage Windows Route Table with IP Helper Functions（iphlpapi.dll）  
通过系统 cmd 增删路由，速度无法忍受，期间cpu占用也非常高

python 版本 3.x

# 思路
大陆白名单模式，即国内流量导向原始默认网关，剩下的全部走 vpn 网关，所以关键就是拿到国内的 ip 段

# 文件说明
## prepare_ip.py
- 下载 ip 文件
- 分析 ip 文件，通过限制掩码长度，限制路由的条数 (使用了 chinaip 的代码)

指定国家获取 格式 CDIR  
<https://www.ip2location.com/blockvisitorsbycountry.aspx>  

## test_wmi.py
获取默认路由即 0.0.0.0/0 (且跃点值最小的) 那一条  
即使有多张网卡跃点数相同，也只取最靠前的一条  

wmi 依赖 包 `wmi` 和 `pywin32`

## winroute.py
封装了增加、删除路由的 winapi

## route_op.py
读取 prepare 生成的文件(里的路由)，调用 Winroute 的方法增减系统路由(管理员权限)

默认网关通过上面的 test_wmi 文件里的函数获取，然后存入到文件，后续恢复时用。  
写到文件的原因是，路由条目数量增大时，恢复时 wmi 的函数获取路由的时间开销较大，找原始默认网关很费时。

# 设置
本地设置 首选 dns: opendns  
备用 114
颠倒好像不影响

国内 ip 全部走默认路由
剩下的导到 vpn

成功登录steam美区

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