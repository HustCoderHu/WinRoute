#!/usr/bin/python
# -*- coding:utf-8 -*-
import os
import os.path as path
import sys
import socket
import struct

from pprint import pprint
from urllib import request

cwd = r'E:\github_repo\WinRoute'
os.chdir(cwd)
sys.path.append(cwd)

def download_apnic_latest(toFile):
  if path.exists(toFile):
    print(toFile + ' ALREADY EXISTS!!!')
    return
  apnic_url = 'http://ftp.apnic.net/stats/apnic/delegated-apnic-latest'
  # 单线程下载很慢
  request.urlretrieve(apnic_url, toFile)
  return

getip = lambda x: socket.inet_ntoa(struct.pack('!I', x))
getint = lambda x: struct.unpack('!I', socket.inet_aton(x))[0]
def check_range(start, end, MAXBITS):
  routeList=[]
  count = 0
  base = start
  while base <= end:
    step = 0
    while (base | (1 << step)) != base:
      if (base | (0xffffffff >> (31 - step))) > end:
        break
      step += 1
    if step >= (32 - MAXBITS):
      count += (1 << step)
      routeList.append(getip(base) + '/' + str(32 - step))
      # print '%s/%s' % (getip(base), (32 - step))
    base += (1 << step)
  return count, routeList

def parse_record(name, MAXBITS):
  routed = 0
  amount = 0
  start = end = 0

  routeList = []
  for x in open(name):
    # apnic|CN|ipv4|1.0.1.0|256|20110414|allocated
    if 'CN|ipv4' not in x:
      continue
    lists = x.split('|')
    ip = lists[3]
    count = int(lists[4])
    newstart = getint(ip)
    newend = newstart + count
    if end == newstart:
      end = newend
    else:
      if end - start + 1 >= (1 << (32 - MAXBITS)):
        _count, _routeLst = check_range(start, end - 1, MAXBITS)
        # print(len(_routeLst))
        routeList.extend(_routeLst)
        routed += _count
      amount += end - start
      start = newstart
      end = newend
  print('ip range cut down to: %d%%' % (100 * routed / amount))
  print(len(routeList))
  return routeList

def generate_china_ip():
  return

def generate_us_ip(fromFile, toFile, MAXBITS):
  routeList = parse_record(fromFile, MAXBITS)
  with open(toFile, 'wt') as f:
    # f.writelines(routeList)
    for _route in routeList:
      f.write(_route + '\n')
  return

def tst():
  toFile = r'E:\github_repo\WinRoute\delegated-apnic-latest.txt'
  # download_apnic_latest(toFile)

  fromFile = toFile
  toFile = r'E:\github_repo\WinRoute\us_ip_max'
  MAXBITS = 23
  toFile += str(MAXBITS) + '.txt'
  generate_us_ip(fromFile, toFile, MAXBITS)
  return

def main(_):
  return

if __name__ == '__main__':
  # main()
  tst()