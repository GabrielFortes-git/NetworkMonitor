import dbconfig

class DiviceEspecifications():
    def __init__(self,os,release,architecture,manufacturer,model,processor):
        self.os = os
        self.release = release
        self.architecture = architecture
        self.manufacturer = manufacturer
        self.model = model 
        self.processor = processor

    def insertDataIntoDB(self):
        conn = dbconfig.dbConnection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO device_specifications(`os`,`release_date`,`architecture`,`manufacturer`,`model`,`processor`)VALUES(%s,%s,%s,%s,%s,%s)", (self.os, self.release, self.architecture, self.manufacturer, self.model, self.processor))
        conn.commit()
        cursor.close()

    def updateIP(ip):
        conn = dbconfig.dbConnection()
        cursor = conn.cursor()
        cursor.execute("UPDATE device_specifications SET ip_address = %s WHERE id = 1" , [ip])
        conn.commit()
        cursor.close()

class CPUTimes():
    def __init__(self, user,nice,system,idle,iowait,irq,softirq,steal,guest):
        self.user = user
        self.nice = nice
        self.system = system
        self.idle = idle
        self.iowait = iowait
        self.irq = irq
        self.softirq = softirq
        self.steal = steal
        self.guest = guest

    def insertDataInDB(self):
        conn = dbconfig.dbConnection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO cpu_times(`user`,nice,`system`,idle,iowait,irq,softirq,steal,guest)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)", (self.user,self.nice,self.system,self.idle,self.iowait,self.irq,self.softirq,self.steal,self.guest,))
        conn.commit()
        cursor.close()

class CPUTStats():
    def __init__(self,cpuUsage,physicalCoreCount,logicalCoreCount,ctx_switches,interrupts,soft_interrupts,syscalls):
        self.cpuUsage = cpuUsage
        self.physicalCoreCount = physicalCoreCount
        self.logicalCoreCount = logicalCoreCount
        self.ctx_switches = ctx_switches
        self.interrupts =  interrupts
        self.soft_interrupts = soft_interrupts
        self.syscalls = syscalls

    def insertDataInDB(self):
        conn = dbconfig.dbConnection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO cpu_stats(cpuUsage,physicalCoreCount,logicalCoreCount,ctx_switches,interrupts,soft_interrupts,syscalls)VALUES(%s,%s,%s,%s,%s,%s,%s)", (self.cpuUsage,self.physicalCoreCount,self.logicalCoreCount,self.ctx_switches,self.interrupts,self.soft_interrupts,self.syscalls))
        conn.commit()
        cursor.close()

class CPUFrequency():
    def __init__(self, current , min , max):
        self.current = current
        self.max = max
        self.min = min

    def insertDataInDB(self):
        conn = dbconfig.dbConnection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO cpu_frequency(current, min, max)VALUES(%s,%s,%s)", (self.current,self.min,self.max))
        conn.commit()
        cursor.close()

class AverageSystemLoad():
    def __init__(self, oneMin, fiveMin, fifteenMin):
        self.oneMin = oneMin
        self.fiveMin = fiveMin
        self.fifteenMin = fifteenMin

    def insertDataInDB(self):
        conn = dbconfig.dbConnection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO cpu_avg_sys_load(one_min, five_min, fifteen_min)VALUES(%s,%s,%s)", (self.oneMin,self.fiveMin,self.fifteenMin))
        conn.commit()
        cursor.close()
    
class VirtualMemory():
    def __init__(self,total,available,percent,used,free,active,inactive,buffers,cached,shared,slab):
        self.total = total
        self.available = available
        self.percent = percent
        self.used = used
        self.free = free
        self.active = active
        self.inactive = inactive
        self.buffers = buffers
        self.cached = cached
        self.shared = shared
        self.slab = slab


    def insertDataInDB(self):
        conn = dbconfig.dbConnection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO virtual_memory(total,available,percent,used,free,active,inactive,buffers,cached,shared,slab)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (self.total,self.available,self.percent,self.used,self.free,self.active,self.inactive,self.buffers,self.cached,self.shared,self.slab))
        conn.commit()
        cursor.close()

class SwapMemory():
    def __init__(self,total,used,percent):
        self.total = total
        self.used = used
        self.percent = percent

    def insertDataInDB(self):
        conn = dbconfig.dbConnection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO swap_memory(total,used,percent)VALUES(%s,%s,%s)", (self.total,self.used,self.percent))
        conn.commit()
        cursor.close()

class DiskUsage():
    def __init__(self, total, used, free, percent):
        self.total = total
        self.used = used
        self.free = free
        self.percent = percent

    def insertDataInDB(self):
        conn = dbconfig.dbConnection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO disk_usage(total,used,free,percent)VALUES(%s,%s,%s,%s)", (self.total, self.used, self.free, self.percent))
        conn.commit()
        cursor.close()

class IOCounters():
    def __init__(self, bytes_sent, bytes_recv, packets_sent, packets_recv, errin, errout, dropin, dropout):
        self.bytes_sent = bytes_sent
        self.bytes_recv = bytes_recv 
        self.packets_sent = packets_sent
        self.packets_recv = packets_recv
        self.errin = errin
        self.errout = errout
        self.dropin = dropin
        self.dropout = dropout

    def insertDataInDB(self):
        conn = dbconfig.dbConnection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO IO_counter(bytes_sent, bytes_recv, packets_sent, packets_recv, errin, errout, dropin, dropout)VALUES(%s,%s,%s,%s,%s,%s,%s,%s)", (self.bytes_sent, self.bytes_recv, self.packets_sent, self.packets_recv, self.errin, self.errout, self.dropin, self.dropout))
        conn.commit()
        cursor.close()

class OtherMetrics():
    def __init__(self, batteryPercentage, bootTime, user):
        self.batteryPercentage = batteryPercentage
        self.bootTime = bootTime
        self.user = user
    
    def insertDataInDB(self):
        conn = dbconfig.dbConnection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO other_metrics(batteryPercentage,bootTime, user)VALUES(%s,%s,%s)", (self.batteryPercentage, self.bootTime, self.user))
        conn.commit()
        cursor.close()

class SpeedTestData():
    def __init__(self,download,upload,ping):
        self.download = download
        self.upload = upload
        self.ping = ping

       
    def insertDataInDB(self):
        conn = dbconfig.dbConnection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO speed_test_data(download,upload,ping)VALUES(%s,%s,%s)", (self.download, self.upload, self.ping))
        conn.commit()
        cursor.close()

class Devices():
    def __init__(self, macAddress, ipAddress, model):
        self.macAddress = macAddress
        self.ipAddress = ipAddress
        self.model = model

    def VerifyDevice(self):
        conn = dbconfig.dbConnection()
        cursor = conn.cursor()
        cursor.execute(f"SELECT mac_address FROM devices WHERE mac_address = '{self.macAddress}'")
        verifyDevice = cursor.fetchone()
        if(verifyDevice == None):
            self.__storeDevice()
        else:
            self.__updateState()

        cursor.close()

        
    def __storeDevice(self):
        conn = dbconfig.dbConnection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO devices(mac_address,ip_address,model,state)VALUES(%s,%s,%s,%s)", (self.macAddress, self.ipAddress, self.model, 1))
        conn.commit()
        cursor.close()

    def setStateDefaultValue():
        conn = dbconfig.dbConnection()
        cursor = conn.cursor()
        cursor.execute(f"UPDATE devices SET state = 0")
        cursor.close()

    def __updateState(self):
        conn = dbconfig.dbConnection()
        cursor = conn.cursor()
        cursor.execute(f"UPDATE devices SET state = 1 WHERE mac_address = '{self.macAddress}'")
        cursor.close()
            
class DefaultGateway():
    def __init__(self,description,objectID,uptime,name,location,timeSinceLastChange,numberOfInterfaces):
        self.description = description
        self.objectID = objectID
        self.uptime = uptime
        self.name = name
        self.location = location
        self.timeSinceLastChange = timeSinceLastChange
        self.numberOfInterfaces = numberOfInterfaces

    def insertDataInDB(self):
        conn = dbconfig.dbConnection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO default_gateway(description,objectID,uptime,name,location,timeSinceLastChange,numberOfInterfaces)VALUES(%s,%s,%s,%s,%s,%s,%s)", (self.description,self.objectID,self.uptime,self.name,self.location,self.timeSinceLastChange,self.numberOfInterfaces))
        conn.commit()
        cursor.close()

    def insertInterfacesData(datas):
        conn = dbconfig.dbConnection()
        cursor = conn.cursor()

        for data in datas:
            cursor.execute("INSERT INTO default_gateway_interfaces(id_default_gateway,name,type,maxPacketSize,speed,status,lastChange,octetsReceived,packetsDelivered,errors,discartedPackets)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (1,data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8], data[9]))
            conn.commit()

        cursor.close()

    def truncateInterfacesDataTable():
        conn = dbconfig.dbConnection()
        cursor = conn.cursor()
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
        cursor.execute("TRUNCATE TABLE default_gateway_interfaces")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
        cursor.close()


