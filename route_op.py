# -*- coding:utf-8 -*-
import os
import os.path as path
import sys

import json
import time
from pprint import pprint
from urllib import request
import struct

cwd = r'E:\github_repo\WinRoute'
cwd = r'D:\docs\github_repo\WinRoute'
os.chdir(cwd)
print(os.getcwd())
sys.path.append(cwd)

itm_dict_file = r'default_interface_and_gw.json'
# import prepare_ip
import winroute
import test_wmi

# import winroute.WinRoute as WinRoute
# import winroute.winroute as winroute

#输出当前路由表（IPv4）
# route.printroute()

#添加一个路由，给出：目标IP，子网掩码，网关(即下一跳IP，不给出与默认路由的相同)，Metric值（不给出则与默认路由的相同），接口（不给出则与默认路由的相同）
# route.CreateIpForwardEntry("1.0.7.0","255.255.255.0","192.168.1.1", dwForwardIfIndex=15)

# 掩码位数 转 255.255.0.0 形式
def maskBit2strMask(nBit):
  byte2val = {0:0, 1:128, 2:192, 3:224, 4:240, 5:248, 6:252, 7:254, 8:255}

  byteIdx = 0
  nBitByte = 8 if nBit >= 8 else nBit
  strMask = str(byte2val[nBitByte])
  nBit -= nBitByte
  byteIdx += 1

  while byteIdx < 4 and nBit > 0:
    nBitByte = 8 if nBit >= 8 else nBit
    strMask += '.' + str(byte2val[nBitByte])
    nBit -= nBitByte
    byteIdx += 1

  while byteIdx < 4:
    strMask += '.0'
    byteIdx += 1
  # packed = struct.pack('<I', intMask)
  # maskByte = struct.unpack('<4c', packed)
  # strMask = str(int(maskByte[0]))
  # strMask += '.' + str(int(maskByte[1]))
  # strMask += '.' + str(int(maskByte[2]))
  # strMask += '.' + str(int(maskByte[3]))
  return strMask

def getItem(routeItemFile, maxMaskBit):
  with open(routeItemFile, 'rt') as f:
    lineList = f.readlines()
  
  routeList = [] # itm = {'strFwdDst': '', 'strFwdMask': ''}

  # itm = {}
  # itm['strFwdDst'] = '8.8.8.8'
  # itm['strFwdMask'] = maskBit2strMask(32)
  # routeList.append(itm)

  for line in lineList: # 192.168.1.1/24
    if not line[0].isdigit(): # skip not ip blocks
      continue
    itm = {}
    itm['strFwdDst'], strMaskBit = line.split('/')
    if int(strMaskBit) > maxMaskBit:
      continue
    itm['strFwdMask'] = maskBit2strMask(int(strMaskBit))
    routeList.append(itm)
  print('route item count: %d' % len(routeList))
  # pprint(routeList[0:6])
  return routeList

def tst():
  print('tst')
  routeItemFile = r'D:\BrkGFW\ip_route\us_ip-max20.txt'
  routeItemFile = r'D:\BrkGFW\us-cdir.txt'
  routeItemFile = r'D:\BrkGFW\cn-cdir.txt'
  routeItemFile = r'D:\docs\github_repo\WinRoute\cn-cdir.txt'
  start = time.clock()
  routeList = getItem(routeItemFile, 32)
  # us
  # 26 len = 89428
  # 25 len = 82072
  # 24 len = 76504
  # 
  # 20 len = 19474
  # cn
  # 32 len 7029
  # 28 len 6411
  # 24 len 5986
 
  # print(maskBit2strMask(17))
  # print(maskBit2strMask(18))
  # print(maskBit2strMask(19))
  # print(maskBit2strMask(20))
  # print(maskBit2strMask(21))
  # print(maskBit2strMask(22))
  # print(maskBit2strMask(23))
  # print(maskBit2strMask(24))
  elapsed = (time.clock() - start)
  print(elapsed)
  return

def tst2():
  strr0 = '1.22.56.0'
  strr1 = '\n# Free IP2Location Firewall List by Country'
  print(not strr0[0].isdigit()) # false
  print(not strr1[0].isdigit()) # true
  return

def main():
  # vpn = {'gateway': '10.111.2.5', 'fwdIfIndex': 37} # 26
  # vpn = {'gateway': '10.111.2.5', 'fwdIfIndex': 4} # 26

  routeItemFile = r'E:\github_repo\WinRoute\us_ip_max24.txt'
  routeItemFile = r'D:\BrkGFW\us-cdir.txt'
  routeItemFile = r'D:\BrkGFW\cn-cdir.txt'
  routeItemFile = r'D:\docs\github_repo\WinRoute\cn-cdir.txt'
  
  routeList = getItem(routeItemFile, 32)

  #实例
  route=winroute.WinRoute()
  # return

  addRoute = False
  if len(sys.argv) > 1:
    addRoute = True

  defaultAdapter = {
      'gateway': '192.168.1.1',
      'fwdIfIndex': -1
    }
  if addRoute:
    print('add route')
    # 保存默认网关 删除时使用
    itm_dict = test_wmi.getDefaultGateWayFromRouteTable()
    print(itm_dict)
    defaultAdapter['gateway'] = itm_dict['NextHop']
    defaultAdapter['fwdIfIndex'] = itm_dict['InterfaceIndex']
    print(defaultAdapter)
    with open(itm_dict_file, 'w') as f:
      json.dump(itm_dict, f)

    # 加路由 计时
    start = time.process_time()
	# DeprecationWarning: time.clock has been deprecated in Python 3.3 and will be removed from Python 3.8: 
	# use time.perf_counter or time.process_time instead
    for itm in routeList:
      # route.CreateIpForwardEntry(itm['strFwdDst'], itm['strFwdMask'], vpn['gateway'], 
          # dwForwardIfIndex=vpn['fwdIfIndex'])
      # print('CreateIpForwardEntry')
      route.CreateIpForwardEntry(itm['strFwdDst'], itm['strFwdMask'], defaultAdapter['gateway'], 
          dwForwardIfIndex=defaultAdapter['fwdIfIndex'])
    elapsed = (time.process_time() - start)
    print(elapsed)
  # input()
  else :
    print('delete route')
    with open(itm_dict_file, 'r') as f:
      itm_dict = json.load(f)
    print(itm_dict)
    defaultAdapter['gateway'] = itm_dict['NextHop']
    defaultAdapter['fwdIfIndex'] = itm_dict['InterfaceIndex']
    # 删路由 计时
    start = time.process_time()
    for itm in routeList:
      # route.DeleteIpForwardEntry(itm['strFwdDst'], itm['strFwdMask'], vpn['gateway'], 
          # dwForwardIfIndex=vpn['fwdIfIndex'])
      route.DeleteIpForwardEntry(itm['strFwdDst'], itm['strFwdMask'], defaultAdapter['gateway'], 
          dwForwardIfIndex=defaultAdapter['fwdIfIndex'])
    elapsed = (time.process_time() - start)
    print(elapsed)
  return

if __name__ == '__main__':
  main()
  # tst()
  # tst2()
