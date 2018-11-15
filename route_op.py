import os
import os.path as path
import sys

cwd = r'E:\github_repo\WinRoute'
os.chdir(cwd)
print(os.getcwd())
sys.path.append(cwd)
import prepare_ip
import winroute

#!/usr/bin/python
# -*- coding:utf-8 -*-
import time
from pprint import pprint
from urllib import request
import struct

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

def getItem(routeItemFile):
  with open(routeItemFile, 'rt') as f:
    lineList = f.readlines()

  routeList = [] # itm = {'strFwdDst': '', 'strFwdMask': ''}
  for line in lineList: # 192.168.1.1/24
    itm = {}
    itm['strFwdDst'], strMaskBit = line.split('/')
    itm['strFwdMask'] = maskBit2strMask(int(strMaskBit))
    routeList.append(itm)
  print('route item count: %d' % len(routeList))
  # pprint(routeList[0:6])
  return routeList

def tst():
  print('tst')
  start = time.clock()
  routeItemFile = r'D:\BrkGFW\ip_route\us_ip-max20.txt'
  routeList = getItem(routeItemFile)
  
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
  vpn = {'gateway': '192.168.1.1', 'fwdIfIndex': 15} # 26
  defaultAdapter = {'gateway': '115.156.159.254', 'fwdIfIndex': 15}

  routeItemFile = r'E:\github_repo\WinRoute\us_ip_max24.txt'
  routeList = getItem(routeItemFile)

  # routeList = routeList[0 : 200]

  #实例
  route=winroute.WinRoute()
  return

  # 加路由 计时
  start = time.clock()
  for itm in routeList:
    route.CreateIpForwardEntry(itm['strFwdDst'], itm['strFwdMask'], vpn['gateway'], 
        dwForwardIfIndex=vpn['fwdIfIndex'])
  elapsed = (time.clock() - start)
  print(elapsed)

  input()

  # 删路由 计时
  start = time.clock()
  for itm in routeList:
    route.DeleteIpForwardEntry(itm['strFwdDst'], itm['strFwdMask'], vpn['gateway'], 
        dwForwardIfIndex=vpn['fwdIfIndex'])
  elapsed = (time.clock() - start)
  print(elapsed)

  return

def main(_):
  return

if __name__ == '__main__':
  # main()
  # tst()
  tst2()