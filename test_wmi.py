import wmi # install wmi & pywin32

# c = wmi.WMI()
# for interface in c.Win32_NetworkAdapterConfiguration(IPEnabled=1):
#   print(interface.Description)
#   print(interface.MACAddress)
#   for ip_address in interface.IPAddress:
#     print (ip_address)
# print

def getGateway():
  c = wmi.WMI()
  configList = c.Win32_NetworkAdapterConfiguration(
      Description="Qualcomm Atheros QCA9377 Wireless Network Adapter", 
      IPEnabled=1)
  configList = c.Win32_NetworkAdapterConfiguration(IPEnabled=1)
  print(type(configList)) # list
  print(len(configList))
  if len(configList) > 1:
    print('get more than 1 adapter')
  # return 
  for conf in configList:
    print(conf.Description)
  conf = configList[0]
  # print(c.Index)
  print(conf.InterfaceIndex)
  print(type(conf.DefaultIPGateway)) # tuple
  print(conf.DefaultIPGateway)

  return

def getDefaultGateWayFromRouteTable():
  itm_dict = {'InterfaceIndex': -1, 'NextHop': '192.168.1.1'}
  # dictList = []
  minMetric = 10000
  routeList = wmi.WMI().Win32_IP4RouteTable()
  # print(len(routeList))
  if len(routeList) > 50:
    err = 'route item number exceed !!\n'
    err += 'check your route table by cmd: route print'
    raise Exception(err)
  for item in routeList:
    # if item.Destination
    # print(item)
    # print(type(item.Destination)) # str
    # if item.Destination.equals('0.0.0.0'):
    if item.Destination == '0.0.0.0' and item.Destination == '0.0.0.0':
      print('find 0.0.0.0/0')
      if (item.Metric1 < minMetric):
        itm_dict['InterfaceIndex'] = item.InterfaceIndex
        itm_dict['NextHop'] = item.NextHop
      # itm_dict = {
      #     'InterfaceIndex': item.InterfaceIndex, 
      #     'NextHop': item.NextHop
      #   }
      # dictList.append(itm_dict)
      # print(itm_dict)
  if itm_dict['InterfaceIndex'] == -1:
    err = 'getDefaultGateWayFromRouteTable fail !\n'
    err += 'check your route table by cmd: route print'
    # print(err)
    raise Exception(err)
  return itm_dict

if __name__ == '__main__':
  # main()
  # getGateway()
  getDefaultGateWayFromRouteTable()

# gateway
# <https://blog.csdn.net/unsv29/article/details/82148344>
# <https://my.oschina.net/yushulx/blog/484663>