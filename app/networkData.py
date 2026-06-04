import psutil
import platform
import socket
import json
import random
import string
import getpass
import os
import time
import speedtest
import traceback
from easysnmp import Session
from scapy.all import ARP, Ether, srp
from manuf import manuf




def findDeviceEspecifications():
    try:
        with open("/sys/devices/virtual/dmi/id/product_name") as f:
            model = f.read().strip()

        with open("/sys/devices/virtual/dmi/id/sys_vendor") as f:
            manufacturer = f.read().strip()

        return {
                "manufacturer" : manufacturer,
                "model" : model
                }
    except:
        return {
                "manufacturer" : "not found",
                "model" : "not found"
                }

def findIpAddress():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip


def convert_bytes_to_megabytes(num):
    mb = (num / 1024)/1024
    return int(mb)


def getSystemLevelData():
    while(True):


        try:
            os = platform.system()
            release = platform.release()
            machineArchitecture = platform.machine()
            deviceEspecifications = findDeviceEspecifications()
            manufacturer = deviceEspecifications["manufacturer"]
            model = deviceEspecifications["model"]
            processor = platform.processor()
        except Exception as e:
            print(f"ERROR: Failed to find device expecifications !\n Datails: {e}")
        #------------------------------------ IP ----------------------------------#

        try:
            ipAddress = findIpAddress()
        except Exception as e:
            print(f"ERROR: Failed to find the IP address!\nDatails: {e}")

        # --------------------------------------  CPU times -----------------------------------------------#
        # Return system CPU times as a named tuple. Every attribute represents the seconds the CPU has spent in the given mode

        try:
            getCpuTimes = list(psutil.cpu_times())
            cpuTimes = {
                "user": getCpuTimes[0],
                "nice": getCpuTimes[1],
                "system": getCpuTimes[2],
                "idle": getCpuTimes[3],
                "iowait": getCpuTimes[4],
                "irq": getCpuTimes[5],
                "softirq": getCpuTimes[6],
                "steal": getCpuTimes[7],
                "guest": getCpuTimes[8],
            }
        except Exception as e:
            print(f"ERROR: Failed to get cpu times!\nDatails: {e}")


        #scputimes(user=383.63, nice=36.46, system=195.25, idle=10804.76, iowait=45.17, irq=0.0, softirq=9.01, steal=0.0, guest=0.0, guest_nice=0.0)

        #-------------------------------- CPU utilization as a percentage ------------------------------------#
        try:
            cpuUsage = psutil.cpu_percent(interval = 1)
        except Exception as e:
            print(f"ERROR: Failed to get cpu percentage!\nDatails: {e}")

        #---------------------------- The number of CPUs (cores) in the system ------------------------------------#
        try:
            physicalCoreCount = psutil.cpu_count()
            logicalCoreCount = psutil.cpu_count(logical=True)
        except Exception as e:
            print(f"ERROR: Failed to get cpu physical and logical core count!\nDetails: {e}")

        #-------------------------------------------- CPU statistics ------------------------------------------------#

        getCpuStats = list(psutil.cpu_stats())
        cpuStats = {
            "ctx_switches": getCpuStats[0],
            "interrupts": getCpuStats[1],
            "soft_interrupts": getCpuStats[2],
            "syscalls": getCpuStats[3]
        }

        #------------------------ CPU frequency - current, min and max frequencies expressed in Mhz ---------------------------------#

        getCpuFrequency = list(psutil.cpu_freq())
        cpuFrequency = {
            "current": round(getCpuFrequency[0], 2),
            "min": round(getCpuFrequency[1], 2),
            "max": round(getCpuFrequency[2], 2),
        }


        # -------------------------------- Average system load in last 1, 5 and 15 minuts -------------------------------------#

        getAverageSystemLoad = psutil.getloadavg()
        averageSystemLoad = {
            "oneMin": getAverageSystemLoad[0],
            "fiveMin": getAverageSystemLoad[1],
            "fifteenMin": getAverageSystemLoad[2]
        }

        #--------------------------------------------- System memory usage ----------------------------------------------------#

        getMemoryUsage = list(psutil.virtual_memory())
        virtualMemory = {
            "total": convert_bytes_to_megabytes(getMemoryUsage[0]),
            "available": convert_bytes_to_megabytes(getMemoryUsage[1]),
            "percent": convert_bytes_to_megabytes(getMemoryUsage[2]),
            "used": convert_bytes_to_megabytes(getMemoryUsage[3]),
            "free": convert_bytes_to_megabytes(getMemoryUsage[4]),
            "active": convert_bytes_to_megabytes(getMemoryUsage[5]),
            "inactive": convert_bytes_to_megabytes(getMemoryUsage[6]),
            "buffers": convert_bytes_to_megabytes(getMemoryUsage[7]),
            "cached": convert_bytes_to_megabytes(getMemoryUsage[8]),
            "shared": convert_bytes_to_megabytes(getMemoryUsage[9]),
            "slab": convert_bytes_to_megabytes(getMemoryUsage[10]),
        }


        #total=16449527808, available=2891665408, percent=82.4, used=12736483328, free=1182068736, active=4800262144,
        #  inactive=9354018816, buffers=73732096, cached=2457243648, shared=683372544, slab=654286848)

        # --------------------------------------------- Swap memory statistics ---------------------------------------------------#

        getSwapMemoryStats = list(psutil.swap_memory())
        swapMemoryStats = {
            "total": convert_bytes_to_megabytes(getSwapMemoryStats[0]),
            "used": convert_bytes_to_megabytes(getSwapMemoryStats[1]),
            "percent": convert_bytes_to_megabytes(getSwapMemoryStats[2]),     
        }
        #---------------------  Disk usage ------------------------------#


        getDiskUsage = psutil.disk_usage("/")
        diskUsage = {
                "total": convert_bytes_to_megabytes(getDiskUsage[0]),
                "used": convert_bytes_to_megabytes(getDiskUsage[1]),
                "free": convert_bytes_to_megabytes(getDiskUsage[2]),
                "percent": convert_bytes_to_megabytes(getDiskUsage[3]),
                }


    #----------------- Net I/O counters ---------------------#
    # Return system-wide network I/O statistics as a named tuple including the following attributes:


        getNetIOCounters = psutil.net_io_counters(pernic=False, nowrap=True)
        netIOCounters = {
            "bytes_sent": convert_bytes_to_megabytes(getNetIOCounters[0]),
            "bytes_recv": convert_bytes_to_megabytes(getNetIOCounters[1]),
            "packets_sent": convert_bytes_to_megabytes(getNetIOCounters[2]),
            "packets_recv": convert_bytes_to_megabytes(getNetIOCounters[3]),
            "errin": convert_bytes_to_megabytes(getNetIOCounters[4]),
            "errout": convert_bytes_to_megabytes(getNetIOCounters[5]),
            "dropin": convert_bytes_to_megabytes(getNetIOCounters[6]),
            "dropout": convert_bytes_to_megabytes(getNetIOCounters[7])
        }

        #---------------------------------- Battery percentage ----------------------------#
        getBatteryPercentage = psutil.sensors_battery()
        batteryPercentage = getBatteryPercentage[0]
 
        #---------------------- Boot time ---------------------------#
        bootTime = psutil.boot_time()  
        
        # Need to be converted to this format (yyyy/mm/dd - H:M:S)

        #---------------------- User ------------------------#

        user = getpass.getuser()



#====================================================== NETWORK DATA =========================================================================#


        dataCollected = []

        #--------------------- Bandwidth & Lantência -----------------------#

        try:
            st = speedtest.Speedtest()
            speedTestData = {"download": st.download() / 10**6, "upload": st.upload() / 10**6, "ping": st.results.ping}
            # Download and Upload - Mbps  , ping - ms
            dataCollected.append(speedTestData)
        except:
            speedTestData = None
            print("ERROR: Failed to execute the speed test!")




        #------------------------- net_io_counters information ---------------------------#

        try:
            net = psutil.net_io_counters()

            netIOCounters = {
                "bytes_sent": net.bytes_sent,
                "bytes_recv": net.bytes_recv,
                "packets_sent": net.packets_sent,
                "packets_recv": net.packets_recv,
                "errin": net.errin,
                "errout": net.errout,
                "dropin": net.dropin,
                "dropout": net.dropout
            }
            dataCollected.append(netIOCounters)
        except:
            netIOCounters = None
            print("ERROR: Failed to get net IO counters!")




        #------------------------ Network Devices -------------------------#


        try:
            # Force updating the OUI database to prevent IOError
            parser = manuf.MacParser(update=False)

            arp_request = ARP(pdst="192.168.1.0/24")
            broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
            arp_request_broadcast = broadcast / arp_request

            # Safely unpack responses without crashing if the list is empty
            sr_result = srp(arp_request_broadcast, timeout=10, verbose=False)
            
            if sr_result and len(sr_result) > 0:
                answered_list = sr_result[0]
            else:
                answered_list = []

            devices = []

            for sent, received in answered_list:
                mac = received.hwsrc
                manufacturer = parser.get_manuf(mac)
                device = [received.psrc, mac, manufacturer or "Unknown"]
                devices.append(device)

            if devices:
                dataCollected.append(devices)
                print(f"Success! Found {len(devices)} devices.")
            else:
                print("Scan finished, but zero devices responded. Check your subnet or run as sudo.")

        except Exception as e:
            devices = None
            print("ERROR: Failed to find devices!")
            # This prints the actual error message and line number to tell you exactly what failed
            traceback.print_exc() 


        #------------------------- Router Data ---------------------------------#

        try:


            ROUTER = '192.168.1.254'    # Next step: Find default gateway;

            # Create an SNMP session to be used for all our requests
            session = Session(hostname= ROUTER, community='public', version=2)

            OIDS = [
                ['description','1.3.6.1.2.1.1.1.0'],
                ['objectID','1.3.6.1.2.1.1.2.0'],
                ['uptime','1.3.6.1.2.1.1.3.0'], # Centésimos de segundo
                ['name','1.3.6.1.2.1.1.5.0'],
                ['location','1.3.6.1.2.1.1.6.0'],
                ['timeSinceLastChange','1.3.6.1.2.1.1.8.0'],
                ['numberOfInterfaces','1.3.6.1.2.1.2.1.0'],
                ]

            datas = {}

            for i in OIDS:
                retrive_data = session.get(i[1])
                datas[i[0]] = retrive_data.value


            # for key, value in datas.items():
            #     print(f"{key} : {value}\n")


            interfaceIDs = []
            getInterfaceIDs = session.walk("1.3.6.1.2.1.2.2.1.1")

            for i in getInterfaceIDs:
                interfaceIDs.append(i.value)

            interfaceCorrespondentNumber = ['2','3','4','5','7','9','10','11','14','15']
            # 1.3.6.1.2.1.2.2.1.5.x   Reference: https://www.net-snmp.org/docs/mibs/interfaces.html#IANAifType
                # ["name",2], 
                # ["type",3], 
                # ["maxPacketSize",4], 
                # ["speed",5] ,    
                # ["status",7] ,   
                # ["lastChange",9] , 
                # ["octetsReceived",10] , 
                # ["packetsDelivered",11] , 
                # ["errors",14] ,    
                # ["discartedPackets",15] , 

            interfaces = []

            #oid = "1.3.6.1.2.1.2.2.1.2." + i 

            for i in interfaceIDs:
                interface = []
                interface.append(i)
                for j in interfaceCorrespondentNumber:
                    data = session.get(f"1.3.6.1.2.1.2.2.1."+j+"."+i)
                    interface.append(data.value)
                    
                interfaces.append(interface)

            routerData = [datas,interfaces]        
            
            dataCollected.append(routerData)
        except:
            routerData = None
            print("ERROR: Failed to retrive data from router!")


        # ----------------------- Sending the data collected -------------#


        dataCollected = [speedTestData,netIOCounters,devices,routerData]
       




    #=============================================================================================================================================#


            

            # --------------------------------------- Organize the collected data ------------------------------------------#


        systemlevelData = {
            "os":os,
            "release":release,
            "architecture":machineArchitecture,
            "manufacturer":manufacturer,
            "model":model,
            "ipAddress": ipAddress,
            "cpuTimes": cpuTimes,
            "cpuUsage": cpuUsage,
            "physicalCoreCount": physicalCoreCount,
            "logicalCoreCount": logicalCoreCount,
            "cpuStats": cpuStats,
            "cpuFrequency": cpuFrequency,
            "averageSystemLoad": averageSystemLoad,
            "virtualMemory": virtualMemory,
            "swapMemoryStats": swapMemoryStats,
            "diskUsage": diskUsage,
            "netIOCounters": netIOCounters,
            "batteryPercentage": batteryPercentage,
            "bootTime": bootTime,
            "user" : user
        }
            
        print(systemlevelData)
        print(f"\n\n{dataCollected}")

        break
        
getSystemLevelData()

       