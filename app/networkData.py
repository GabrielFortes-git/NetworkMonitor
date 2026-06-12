import psutil
import platform
import socket
import getpass
import time
import speedtest
import traceback
from easysnmp import Session
from scapy.all import ARP, Ether, srp
from manuf import manuf
import schedule
import classes


ROUTER = '192.168.1.254'    # Next step: Find default gateway;


def findDeviceModelAndManufacturer():
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

def obtainDeviceEspecifications():
    try:
        os = platform.system()
        release = platform.release()
        machineArchitecture = platform.machine()
        deviceEspecifications = findDeviceModelAndManufacturer()
        manufacturer = deviceEspecifications["manufacturer"]
        model = deviceEspecifications["model"]
        processor = platform.processor()
        device_spec = classes.DiviceEspecifications(os,release,machineArchitecture,manufacturer,model,processor)
        device_spec.insertDataIntoDB()
    except Exception as e:
        print(f"ERROR: Failed to find device expecifications !\n Datails: {e}")

def obtainDeviceIPAddress():
    try:
        ipAddress = findIpAddress()
        classes.DiviceEspecifications.updateIP(ipAddress)
    except Exception as e:
        print(f"ERROR: Failed to find the IP address!\nDatails: {e}")

def obtainCPUTimes():
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

        cpu_times = classes.CPUTimes(cpuTimes['user'],cpuTimes['nice'],cpuTimes['system'],cpuTimes['idle'],cpuTimes['iowait'],cpuTimes['irq'],cpuTimes['softirq'],cpuTimes['steal'], cpuTimes['guest'])
        cpu_times.insertDataInDB()

    except Exception as e:
        print(f"ERROR: Failed to get cpu times!\nDatails: {e}")

def obtainCPUStats():
    try:
        cpuUsage = psutil.cpu_percent(interval = 1)
        
        #---------------------------- The number of CPUs (cores) in the system ------------------------------------#

        physicalCoreCount = psutil.cpu_count()
        logicalCoreCount = psutil.cpu_count(logical=True)
        #-------------------------------------------- CPU statistics ------------------------------------------------#

        getCpuStats = list(psutil.cpu_stats())
        cpuStats = {
            "ctx_switches": getCpuStats[0],
            "interrupts": getCpuStats[1],
            "soft_interrupts": getCpuStats[2],
            "syscalls": getCpuStats[3]
        }

        cpu_info = classes.CPUTStats(cpuUsage, physicalCoreCount, logicalCoreCount, cpuStats['ctx_switches'], cpuStats['interrupts'], cpuStats['soft_interrupts'], cpuStats['syscalls'])
        cpu_info.insertDataInDB()
        
    except Exception as e:
        print(f"ERROR: Failed to get cpuUsage, physicalCoreCount, logicalCoreCount and cpuStats.\nDetails: {e}")

def obtainCPUFrequency():
    try:

        getCpuFrequency = list(psutil.cpu_freq())
        cpuFrequency = {
            "current": round(getCpuFrequency[0], 2),
            "min": round(getCpuFrequency[1], 2),
            "max": round(getCpuFrequency[2], 2),
        }

        cpu_frequency = classes.CPUFrequency(cpuFrequency['current'], cpuFrequency['min'] , cpuFrequency['max'])
        cpu_frequency.insertDataInDB()

    except Exception as e:
        print(f"ERROR: Failed to get cpuFrequency.\nDetails: {e}")

def obtainAvgSysLoad():
    try:
        getAverageSystemLoad = psutil.getloadavg()
        averageSystemLoad = {
            "oneMin": getAverageSystemLoad[0],
            "fiveMin": getAverageSystemLoad[1],
            "fifteenMin": getAverageSystemLoad[2]
        }

        avg_sys_load = classes.AverageSystemLoad(averageSystemLoad['oneMin'], averageSystemLoad['fiveMin'], averageSystemLoad['fifteenMin'])
        avg_sys_load.insertDataInDB()

    except Exception as e:
        print(f"ERROR: Failed to get cpuAverageSystemLoad.\nDetails: {e}")

def obtainVirtualMemory():
    try:
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

        memory_usage = classes.VirtualMemory(virtualMemory['total'], virtualMemory['available'], virtualMemory['percent'], virtualMemory['used'], virtualMemory['free'], virtualMemory['active'], virtualMemory['inactive'], virtualMemory['buffers'], virtualMemory['cached'],virtualMemory['shared'], virtualMemory['slab'])
        memory_usage.insertDataInDB()

    except Exception as e:
        print(f"ERROR: Failed to get memoryUsage.\nDetails: {e}")

def obtainSwapMemory():
    try:
        getSwapMemoryStats = list(psutil.swap_memory())
        swapMemoryStats = {
            "total": convert_bytes_to_megabytes(getSwapMemoryStats[0]),
            "used": convert_bytes_to_megabytes(getSwapMemoryStats[1]),
            "percent": convert_bytes_to_megabytes(getSwapMemoryStats[2]),     
        }

        swap_memory = classes.SwapMemory(swapMemoryStats['total'], swapMemoryStats['used'], swapMemoryStats['percent'])
        swap_memory.insertDataInDB()

    except Exception as e:
        print(f"ERROR: Failed to get swap memory.\nDetails: {e}")

def obtainDiskUsage():
    try:
        getDiskUsage = psutil.disk_usage("/")
        diskUsage = {
                "total": convert_bytes_to_megabytes(getDiskUsage[0]),
                "used": convert_bytes_to_megabytes(getDiskUsage[1]),
                "free": convert_bytes_to_megabytes(getDiskUsage[2]),
                "percent": convert_bytes_to_megabytes(getDiskUsage[3]),
            }
        
        disk_usage = classes.DiskUsage(diskUsage['total'], diskUsage['used'], diskUsage['free'], diskUsage['percent'])
        disk_usage.insertDataInDB()

    except Exception as e:
        print(f"ERROR: Failed to get disk usage.\nDetails: {e}")

def obtainOtherMetrics():
    try:
        #---- Battery percentage -----#
        getBatteryPercentage = psutil.sensors_battery()
        batteryPercentage = getBatteryPercentage[0]
    
        #---- Boot time ----#
        bootTime = psutil.boot_time()  
            
            # Need to be converted to this format (yyyy/mm/dd - H:M:S)

        #---- User ----#
        user = getpass.getuser()

        other_metrics = classes.OtherMetrics(batteryPercentage, bootTime, user)
        other_metrics.insertDataInDB()

    except Exception as e:
        print(f"ERROR: Failed to get other metrics.\nDetails: {e}")

def obtainSpeedTestData():
    try:
        st = speedtest.Speedtest()
        speedTestData = {"download": st.download() / 10**6, "upload": st.upload() / 10**6, "ping": st.results.ping}
        # Download and Upload - Mbps  , ping - ms

        speed_test = classes.SpeedTestData(speedTestData['download'], speedTestData['upload'], speedTestData['ping'])
        speed_test.insertDataInDB()

    except:
        print("ERROR: Failed to execute the speed test!")

def obtainIOCounters():
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
            
        net_counters = classes.IOCounters(netIOCounters['bytes_sent'], netIOCounters['bytes_recv'], netIOCounters['packets_sent'], netIOCounters['packets_recv'], netIOCounters['errin'], netIOCounters['errout'], netIOCounters['dropin'], netIOCounters['dropout'])
        net_counters.insertDataInDB()

    except Exception as e:
            print(f"ERROR: Failed to get net IO counters!\nDetails: {e}")

def obtainNetworkDevices():
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
          
            for send, received in answered_list:
                mac = received.hwsrc
                ip = received.psrc
                getManufacturer = parser.get_manuf(mac)
                manufacturer = getManufacturer or "Unknown"
                    
                classes.Devices.setStateDefaultValue()
                device_ist = classes.Devices(mac,ip,manufacturer)
                device_ist.VerifyDevice()


    except Exception as e:
        print(f"ERROR: Failed to find devices!\nDetails: {e}")

def obtainDefaultGatewayData():
    try:

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


        default_gateway_info = classes.DefaultGateway(datas['description'], datas['objectID'], datas['uptime'], datas['name'], datas['location'], datas['timeSinceLastChange'], datas['numberOfInterfaces'])
        default_gateway_info.insertDataInDB()

    except Exception as e:
        print(f"ERROR: Failed to get default gateway data.\nDetails: {e}")

def obtainDefaultGatewayInterfacesData():
    try:
        # Create an SNMP session to be used for all our requests
        session = Session(hostname= ROUTER, community='public', version=2)

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
     
        classes.DefaultGateway.insertInterfacesData(interfaces)
        print("Data retrived from router sucessefully inserted in correspondent table")

    except Exception as e:
        print(f"ERROR: Failed to retrive data from router!\nDetails: {e}")  

def truncateInterfacesData():
    classes.DefaultGateway.truncateInterfacesDataTable()

schedule.every().day.do(obtainDeviceEspecifications) # day
schedule.every().minute.do(obtainDeviceIPAddress)  # minute
schedule.every(10).seconds.do(obtainCPUTimes)
schedule.every(10).seconds.do(obtainCPUStats)
schedule.every(10).seconds.do(obtainCPUFrequency)
schedule.every(10).seconds.do(obtainAvgSysLoad)
schedule.every(10).seconds.do(obtainVirtualMemory)
schedule.every(10).seconds.do(obtainSwapMemory)
schedule.every(10).seconds.do(obtainDiskUsage)
schedule.every(10).seconds.do(obtainOtherMetrics)
schedule.every(10).seconds.do(obtainSpeedTestData)
schedule.every(10).seconds.do(obtainIOCounters)
schedule.every(10).seconds.do(obtainNetworkDevices)
schedule.every().day.do(obtainDefaultGatewayData)  # day
schedule.every(20).seconds.do(truncateInterfacesData)
#schedule.every(30).seconds.do(obtainDefaultGatewayInterfacesData) # ERROR TO FIX: Because it's done in this periud, it is colecting the data varios times, when the function stores it in the db

   
while(True):
    schedule.run_pending()
    obtainDefaultGatewayInterfacesData()
    time.sleep(1)

       