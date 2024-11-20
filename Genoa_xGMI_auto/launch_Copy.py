import sys, os, readline, atexit, rlcompleter, subprocess
from importlib import reload

#current_dir = os.getcwd()
#curr_path = current_dir.split("/")
#sys_path = os.sep.join(curr_path[0:len(curr_path)-1])
#yww start
if getattr(sys, 'frozen', False):
    sys_path = sys._MEIPASS
    sys_path = os.sep.join([sys_path,"component"])
else:
    current_dir = os.getcwd()
    curr_path = current_dir.split("/")
    sys_path = os.sep.join(curr_path[0:len(curr_path)-1])
#yww end
    
sys.path.append(sys_path)

#from component import starter_py as _starter_py
#yww start
from component import starter_py_Copy as _starter_py
#yww end

from component.console_logger import start_log, stop_log, end_log
reload(_starter_py)

#pysy_path = os.__file__
#pysy_path = pysy_path.replace("os.py",f"site-packages{os.sep}pysy")
#pysy_config = os.sep.join([pysy_path,"python_config.ini"])
#yww start
if getattr(sys, 'frozen', False):
    pysy_path = sys._MEIPASS
    pysy_path = os.path.normpath(os.sep.join([pysy_path, 'pysy']))
    pysy_config = os.sep.join([pysy_path,"python_config.ini"])
else:
    pysy_path = os.__file__
    pysy_path = pysy_path.replace("os.py",f"site-packages{os.sep}pysy")
    pysy_config = os.sep.join([pysy_path,"python_config.ini"])
#yww end

project_name = _starter_py.project_folder

#console_width = os.get_terminal_size()[0]
#yww start
if getattr(sys, 'frozen', False):
    console_width = 80
else:
    console_width = os.get_terminal_size()[0]
#yww end
print (" Welcome To AMD Go-Pi ".center(console_width-1,"#"))

if sys.version_info[0] !=3 or sys.version_info[1] !=7:
    print ("You are using Python version "+ str(sys.version_info[0]) + "." + str(sys.version_info[1]))
    print ("Python 3.7 is required ")
    exit()

#yww start
if getattr(sys, 'frozen', False):
    sys_path = sys._MEIPASS
    sys_path = os.sep.join([sys_path,"Kysy4"])
    print("Kysy is installed at "+ sys_path)
else:
    if os.environ.get('KYSY_BASE') is None:
        print("Kysy is not in path.")
        exit()
    else:
        print("Kysy is installed at "+ os.environ['KYSY_BASE'])

try:
    _starter_py.existing_config(pysy_config)
    config_choice = _starter_py.readInput()
except:
    config_choice = 'y'
config_choice = config_choice.lower()
while True:
    try:
        if config_choice == "n":
            ipaddress=_starter_py.load_config(pysy_step = pysy_config)
        elif config_choice =='y':
            _starter_py.new_config(pysy_step = pysy_config)
            ipaddress=_starter_py.load_config(pysy_step = pysy_config)
        else:
            ipaddress = input("Please provide wombat ip address : ")
        break
    except Exception as e:
        from colorama import Fore, init
        init(autoreset=True)
        print(f"{Fore.LIGHTRED_EX}{e}{Fore.RESET}")
        continue

if ipaddress == 0:
    ipaddress = None

if (ipaddress is None) or (ipaddress == 'None'):
    print ("NDA not supporting offlie mode, please provide ipaddress !")
    sys.exit(0)
else:
    _starter_py.pysy_config_write(pysy_config,project_name,ipaddress)
    host = ipaddress 

class _gp_core(object):
    def __init__(self):
        import version as _version
        import Kysy as _Kysy
        from importlib_metadata import version as _vr
        from pysy.access_methods.kysy import KysyEnvironment as _KysyEnvironment
        gp_ver = vars(_version.gopi_ver())
        self.gopi_core_version = gp_ver.get("gopi_core_version")
        self.debug_analyzer_version = gp_ver.get("debug_analyzer")
        self.kysy_version = _Kysy.LIBRARY_VERSION
        self.pysy_version = _vr("pysy-nda")
        self.python_version = _KysyEnvironment.platform.python_version()


import pysy as _pysy
plt = _pysy.get_pysy(pysy_name='plt')
#plt = plt.ppr
from pysy.access_methods.kysy import kysy_platform
platform = kysy_platform.get_platform()
gp_core = _gp_core()
from utils.library import getDieOffSet as _getDieOffset
_includeDieOffset = True


def _checkDieOffsetInclusion():
    global _includeDieOffset
    return _includeDieOffset


def _setDieOffsetInclusion(_):
    global _includeDieOffset
    _includeDieOffset = _
    

def go():
    if host == 'offline':
        pass
    else:
        try:
            kysy_platform.exit_pdm()
        except Exception as e:
            print(e)

def pdm():
    if host == 'offline':
        pass
    else:
        try:
            kysy_platform.enter_pdm()
        except Exception as e:
            print(e)

def pdm_status():
    """
    The pdm_status function prints out the pdm status of all cores in platform.
    """
    from colorama import Fore as _Fore
    from prettytable import PrettyTable as _PrettyTable
    def flatten_list(lst):
        """
        The flatten_list function takes a list of lists and returns a single list containing all the elements from the original
        list. The function does not modify the original list.

        :param lst: Pass in the list that we want to flatten
        :return: A flat list of all the items in a nested list
        """
        flat_list = []
        for sublist in lst:
            for item in sublist:
                if item not in flat_list:
                    flat_list.append(item)
        return flat_list

    # Get all PDM status to a list
    topology_list = list()
    debugEnabled_list = list()
    for ccd in flatten_list(
        [
            kysy_platform.get_activate_ccd(socket)
            for socket in kysy_platform.get_activate_socket()
        ]
    ):
        for ccx in flatten_list(
            [
                kysy_platform.get_activate_ccx(socket, ccd)
                for socket in kysy_platform.get_activate_socket()
            ]
        ):
            for core in flatten_list(
                [
                    kysy_platform.get_activate_core(socket, ccd, ccx)
                    for socket in kysy_platform.get_activate_socket()
                ]
            ):
                topology_list.extend(
                    [
                        Kysy.PPRCoreTopologyPhysicalIDs(socket, ccd+_getDieOffset(_checkDieOffsetInclusion()), ccx, core, 0)
                        for socket in kysy_platform.get_activate_socket()
                    ]
                )
    debugEnabled_list = list(kysy_platform._cpu_debug.debugEnabled(topology_list))

    header = ["CORE TOPOLOGY"] + [
        f"SOCKET {socket} PDM STATUS" for socket in kysy_platform.get_activate_socket()
    ]
    table = _PrettyTable(header)
    table.align["CORE TOPOLOGY"] = "l"

    for ccd in flatten_list(
        [
            kysy_platform.get_activate_ccd(socket)
            for socket in kysy_platform.get_activate_socket()
        ]
    ):
        table.add_row(
            [f"ccd-{ccd}"] + ["" for _ in kysy_platform.get_activate_socket()]
        )
        for ccx in flatten_list(
            [
                kysy_platform.get_activate_ccx(socket, ccd)
                for socket in kysy_platform.get_activate_socket()
            ]
        ):
            table.add_row(
                [f"|--> ccx-{ccx}"] + ["" for _ in kysy_platform.get_activate_socket()]
            )
            for core in flatten_list(
                [
                    kysy_platform.get_activate_core(socket, ccd, ccx)
                    for socket in kysy_platform.get_activate_socket()
                ]
            ):
                table.add_row(
                    [f"     |--> core-{core}"]
                    + [
                        f"{_Fore.LIGHTGREEN_EX}IN PDM{_Fore.RESET}"
                        if debugEnabled_list.pop(0)  # FIFO debugEnabled_list
                        else f"{_Fore.LIGHTYELLOW_EX}NOT IN PDM{_Fore.RESET}"
                        for socket in kysy_platform.get_activate_socket()
                    ]
                )

    print(table)

def isSecured():
   """
   The isSecured function will print out the security status of each socket on the platform.
      If it is secured, 'SECURED' will be printed in that row's column;
      otherwise 'UNSECURED' will be printed.
   """
   import Kysy
   from prettytable import PrettyTable
   table = PrettyTable(['SOCKET','SECURED STATUS'])
   security = Kysy.PlatformSecurityInfo(platform)
   for socket in range(kysy_platform.num_sockets()):
           table.add_row([socket, 'SECURED' if security.isSecured(socket, 0) else 'UNSECURED'])
   print(table)

'''
def unlock(url=None) :
    """Execute a secure debug unlock.  Requires an ntid and password to authenticate that the user has secure debug unlock privileges.  These are completely distinct from the wombat name/pw pair."""
    if host == 'offline':
        print (" You are in offline Mode, no unlock required !!")
        pass
    else:
        wombat = kysy_platform._wombat
        Kysy.SecureDebug.initialize()
        # this will fail if terminal has done "su newuser"
        sdu_username = input("Enter your NTID username:")

        # slightly safer than above
        # import commands
        # sdu_username = commands.getoutput("whoami")

    #   sdu_password = os.environ['KYSY_PASSWORD']
        import getpass
        sdu_password = getpass.getpass(prompt = 'Password for user %s: ' % sdu_username)			# hides typed text

        platformSecurity = Kysy.PlatformSecurityInfo.create(platform)
        if platformSecurity.isSecured(0, 0) and not platformSecurity.isUnlocked(0, 0):
            if url is not None:
                secureDbg = Kysy.SecureDebug.create(wombat,url)
            else:
                secureDbg = Kysy.SecureDebug.create(wombat)
            if secureDbg.detailedUnlockStatus() == 2:
                secureDbg.forcePSPMailBoxToDefault()
            ucPtr = Kysy.UserCredentials(sdu_username, sdu_password)
            platform.platformAccess().debugVisitor( Kysy.DISABLE_DEBUGVISITOR )
            wombat.jtag( Kysy.JTAG.CPU_JTAG ).disableLog()
            platform.platformAccess().logger().consoleLogLevel( Kysy.Logger.LOG_NONE )
            secureDbg.unlock(ucPtr, Kysy.SecureDebug.ON_FAILURE)

        # Wipe out the password from memory
        sdu_password = "invalid"
'''        
#yww start
def unlock(sdu_username, sdu_password, url=None) :
    """Execute a secure debug unlock.  Requires an ntid and password to authenticate that the user has secure debug unlock privileges.  These are completely distinct from the wombat name/pw pair."""
    if host == 'offline':
        print (" You are in offline Mode, no unlock required !!")
        pass
    else:
        wombat = kysy_platform._wombat
        Kysy.SecureDebug.initialize()
        # this will fail if terminal has done "su newuser"
        #sdu_username = input("Enter your NTID username:")


        # slightly safer than above
        # import commands
        # sdu_username = commands.getoutput("whoami")

    #   sdu_password = os.environ['KYSY_PASSWORD']
        #import getpass
        #sdu_password = getpass.getpass(prompt = 'Password for user %s: ' % sdu_username)			# hides typed text

        platformSecurity = Kysy.PlatformSecurityInfo.create(platform)
        if platformSecurity.isSecured(0, 0):
            if url is not None:
                secureDbg = Kysy.SecureDebug.create(wombat,url)
            else:
                secureDbg = Kysy.SecureDebug.create(wombat)
            if secureDbg.detailedUnlockStatus() == 2:
                secureDbg.forcePSPMailBoxToDefault()
            ucPtr = Kysy.UserCredentials(sdu_username, sdu_password)
            platform.platformAccess().debugVisitor( Kysy.DISABLE_DEBUGVISITOR )
            wombat.jtag( Kysy.JTAG.CPU_JTAG ).disableLog()
            platform.platformAccess().logger().consoleLogLevel( Kysy.Logger.LOG_NONE )
            secureDbg.unlock(ucPtr, Kysy.SecureDebug.ON_FAILURE)

        # Wipe out the password from memory
        sdu_password = "invalid"
#yww end
        
def is_locked() :
    if host == 'offline':
        print (" You are in offline Mode, no unlock required !!")
        pass
    else:
        platformSecurity = Kysy.PlatformSecurityInfo.create(platform)
        if platformSecurity.isSecured(0, 0) and not platformSecurity.isUnlocked(0, 0):
            return True
        else:
            return False
# End Custom Environment Variables
#################################################

historyPath = os.path.expanduser("~\\.pyhistory")
readline.parse_and_bind('tab: complete')

readline.write_history_file(historyPath)


if os.path.exists(historyPath):
    readline.read_history_file(historyPath)
#if ipaddress != 'None':
#    atexit.register(print,'Exiting PDM...')
#    atexit.register(go())

def show_history():
    for i in range(readline.get_current_history_length()):
        print (readline.get_history_item(i + 1))

#ori_help = help
#yww start
import pydoc
ori_help = pydoc.help
#yww end

def help(obj=None):
    if obj is not None:
        ori_help(obj)
    else:
        from prettytable import PrettyTable as _PrettyTable
        table = _PrettyTable()
        table.field_names=["No.","IP","Import Command"]
        table.align = "l"
        debug_script = {
            "df" : "from debug.df import df",
            "wafl" : "from debug.dxio import wafl",
            "xgmi" : "from debug.dxio import xgmi",
            "mca" : "from debug.mca import mca",
            "pci" : "from debug.pci import pci",
            "pcie" : "from debug.pcie import pcie_debug",
            "umc" : "from debug.umc import umc",
            "debug analyzer" : "from debug.triage import debug_analyzer",}
        count=1
        for k,v in debug_script.items():
            table.add_row([count,k,v])
            
            count=count+1
        print ("Available Debug Script:")
        print (table)


def msr(address, data=None, pdm_stay=False, socket=0, ccd=0, ccx=0, core=0, thread=0):
    """
    The msr function is used to read and write MSR registers.

    :param address: Specify the msr address
    :param data: Set the value of the msr
    :param pdm_stay: Determine whether to exit pdm mode after the function is executed
    :param socket: Specify which socket to access
    :param ccd: Specify the ccd number
    :param ccx: Specify the ccx id
    :param core: Specify the core number
    :param thread: Select the thread to be read
    """
    from component import wplatform
    print("Try to set system to PDM debug mode")
    try:
        pdm()
        pdm()
    except Exception as e:
        print(e)
    PhysicalHierarchy = platform.platformAccess().x86PhysicalHierarchy()
    KysySocketObj = PhysicalHierarchy.sockets()
    PPRCoreTopologyPhysicalIDs = wplatform.find_threads(KysySocketObj, active_only=True)

    ThreadId = 0
    for _ in PPRCoreTopologyPhysicalIDs:
        ThreadId += 1
        if _.socketID() == socket and _.dieID() == ccd and _.ccxID() == ccx and _.coreID() == core and _.threadID() == thread:
            break
    core_data = Kysy.CoreData.create(ThreadId)
    msr_reg = Kysy.MSRRegister.create(address, platform.platformAccess(), core_data)
    if data is None:
        msr_reg.read()
        return hex(msr_reg.value())
    else:
        msr_reg.read()
        msr_reg.value(data)
        msr_reg.write()
        msr_reg.read()

    if not pdm_stay:
        print("Exiting PDM mode()")
        try:
            go()
            go()
        except Exception as e:
            print(e)
    return hex(msr_reg.value())


def msr_read_all(address, pdm_stay=False):
    """
    The msr_read_all function reads MSR registers value from all cores in the system.

    :param address: Specify the msr register address
    :param pdm_stay: Determine whether to exit pdm mode after the function is executed
    """
    from component import wplatform
    from prettytable import PrettyTable
    from alive_progress import alive_bar
    table = PrettyTable(['SOCKET', 'CCD', 'CCX', 'CORE', 'THREAD', 'MSR VALUE'])
    table.align = 'r'
    print("Try to set system to PDM debug mode")
    try:
        pdm()
        pdm()
    except Exception as e:
        print(e)

    physical_hierachy = platform.platformAccess().x86PhysicalHierarchy()
    kysy_socket_obj = physical_hierachy.sockets()
    ppr_core_topology_physical_ids = wplatform.find_threads(kysy_socket_obj, active_only=True)

    ThreadId = 0
    with alive_bar(len(ppr_core_topology_physical_ids), title="Reading all MSR registers value", bar='classic2') as bar:
        for _ in ppr_core_topology_physical_ids:
            core_data = Kysy.CoreData.create(ThreadId)
            msr_reg = Kysy.MSRRegister.create(address, platform.platformAccess(), core_data)
            msr_reg.read()
            value = msr_reg.value()
            table.add_row([_.socketID(), _.dieID(), _.ccxID(), _.coreID(), _.threadID(), f'0x{value:08x}'])
            ThreadId += 1
            bar()
    print(table)
    if not pdm_stay:
        print("Exiting PDM mode()")
        try:
            go()
            go()
        except Exception as e:
            print(e)


def msr_write_all(address, data, pdm_stay=False):
    """
    The msr_write_all function is used to write a value to all MSR registers on the system.

    :param address: Specify the address of the msr register to be written
    :param data: Set the value of the msr register
    :param pdm_stay: Determine whether to exit pdm mode after the function is executed
    """
    from component import wplatform
    from alive_progress import alive_bar
    print("Try to set system to PDM debug mode")
    try:
        pdm()
        pdm()
    except Exception as e:
        print(e)

    physical_hierachy = platform.platformAccess().x86PhysicalHierarchy()
    kysy_socket_obj = physical_hierachy.sockets()
    ppr_core_topology_physical_ids = wplatform.find_threads(kysy_socket_obj, active_only=True)

    ThreadId = 0
    with alive_bar(len(ppr_core_topology_physical_ids), title=f"Writing all MSR registers value to 0x{data:08x}", bar='classic2') as bar:
        for _ in ppr_core_topology_physical_ids:
            core_data = Kysy.CoreData.create(ThreadId)
            msr_reg = Kysy.MSRRegister.create(address, platform.platformAccess(), core_data)
            msr_reg.value(data)
            msr_reg.write()
            ThreadId += 1
            bar()
    if not pdm_stay:
        print("Exiting PDM mode()")
        try:
            go()
            go()
        except Exception as e:
            print(e)


def cfgrd(bus,dev,fun,off):
    reg = Kysy.PCIRegister.create(platform.platformAccess(),bus,dev,fun,off)
    #reg.accessLogic('MMIO')
    reg.read()

    return hex(reg.value())

def cfgwr(bus,dev,fun,off,data):
    reg = Kysy.PCIRegister.create(platform.platformAccess(),bus,dev,fun,off)
    reg.read()
    val = reg.value()
    print(hex(val))
    reg.value(data)
    reg.write()
    reg.read()
    print('%08x' %reg.value())

def io_space(address):
    io_reg = Kysy.IORegister.create(0xCF8,Kysy.IO_DWORD,platform.platformAccess())
    cfc = Kysy.IORegister.create(0xCFC,Kysy.IO_DWORD,platform.platformAccess())
    io_reg.read()
    io_reg.value(address)
    io_reg.write()
    cfc.read()

    return hex(cfc.value())

def io_access(io_register_address,data=None):
    io_reg = Kysy.IORegister.create(io_register_address,Kysy.IO_DWORD,platform.platformAccess())
    
    if data is None:
        io_reg.read()
        print(hex(io_reg.value()))
    else:
        io_reg.read()
        io_reg.value(data)
        io_reg.write()
        io_reg.read()
        print(hex(io_reg.value()))

def memrd(socket,ccd,address,dword_count=None,enter_pdm = True,pdm_stay=False,binary_dump=False):
    """
    The memrd function is used to read a memory address on the platform.

    :param socket: Specify the socket number
    :param ccd: Specify which ccd to read from
    :param address: Specify the address of the memory to be read
    :param dword_count: Specify the number of dwords to read
    :param enter_pdm: Enter pdm mode before the memory read operation
    :param pdm_stay: Keep the system in pdm mode after running memrd
    :param binary_dump: Dump the data to a binary file
    """
    import Kysy
    from pysy.access_methods.kysy import kysy_platform as _kysy_platform
    platform = _kysy_platform.get_platform()

    if enter_pdm:
        print("Try to set system to PDM debug mode")
        try:
            pdm()
            pdm()
        except Exception as e:
            print(f'ERROR: {e}')
            print('POSSIBLE CAUSE: UNABLE TO ENTERN PDM MODE, MAKE SURE YOUR PLATFORM IS UNLOCKED')

    dump_array = []

    from prettytable import PrettyTable
    table = PrettyTable(['Socket', 'CCD', 'Address', 'Data'])

    # TO AUTO DETECT MEMORY DESTINATION AND MEMORY TYPE
    memoryMap = Kysy.MemoryMap(platform)
    platformAccess = platform.platformAccess()
    dieOffset = platformAccess.x86PhysicalHierarchy().ccdDieNumberOffset()
    idMap = Kysy.PPRCoreTopologyPhysicalIDs(socket, (dieOffset + ccd), 0, 0, 0)
    accessInfo = memoryMap.accessInfo(idMap, address, Kysy.MEMORY_READ)

    memory_destination = accessInfo.destination()
    memory_type = accessInfo.mode()

    if dword_count is None:
        physical_cores = Kysy.PPRCoreTopologyPhysicalIDs(socket, ccd+_getDieOffset(_checkDieOffsetInclusion()), 0, 0, 0)
        mem_mapped = Kysy.PhysicalMemorySpace.mapMemory(platform.platformAccess(), physical_cores, address, Kysy.Bytes(4), memory_destination, memory_type, Kysy.MEMORY_ACCESS_SIZE_DEFAULT)
        mem_mapped.read()
        return hex(mem_mapped.dword(0))

    physical_cores = Kysy.PPRCoreTopologyPhysicalIDs(socket, ccd+_getDieOffset(_checkDieOffsetInclusion()), 0, 0, 0)
    size = Kysy.Bytes(dword_count * 4)
    mem_mapped = Kysy.PhysicalMemorySpace.mapMemory(platform.platformAccess(), physical_cores, address, size, memory_destination, memory_type, Kysy.MEMORY_ACCESS_SIZE_DEFAULT)
    mem_mapped.read()

    for index in range(0, dword_count):
        value = 0
        for byte_offset in range(0, 4):
            value |= mem_mapped.byte(4 * index + byte_offset) << (8 * byte_offset)

        data_array = [socket, ccd, hex(address), hex(value)]

        table.add_row(data_array)
        dump_array.append(hex(value)[2:].zfill(8))

        address += 4

    if binary_dump:
        import binascii

        write_file = open("binary", "w+b")
        dump_array_string_data = str("".join(map(str, dump_array)))
        binary_string = binascii.unhexlify(dump_array_string_data)
        write_file.write(binary_string)
        write_file.close()

    if not pdm_stay:
        print("Exiting PDM mode()")
        try:
            go()
            go()
        except Exception as e:
            print(e)

    return table

def memwr(socket,ccd,address,dram_array,enter_pdm = True,pdm_stay=False):
    """
    The memwr function is used to write a list of dwords into the memory space.

    :param socket: Specify which socket to write the data to
    :param ccd: Specify which ccd to write to
    :param address: Specify the starting address of the memory location to be written
    :param dram_array: Pass the data to be written into memory
    :param enter_pdm: Enter pdm mode before writing to memory
    :param pdm_stay: Keep the system in pdm mode after the memwr function is executed
    """
    if enter_pdm:
        try:
            print("Try to set system to PDM debug mode")
            pdm()
            pdm()
        except Exception as e:
            print(f'ERROR: {e}')
            print('POSSIBLE CAUSE: UNABLE TO ENTERN PDM MODE, MAKE SURE YOUR PLATFORM IS UNLOCKED')

    dword_count = len(dram_array)

    from prettytable import PrettyTable
    table = PrettyTable(['Socket', 'CCD', 'Address', 'Data'])

    # TO AUTO DETECT MEMORY DESTINATION AND MEMORY TYPE
    memoryMap = Kysy.MemoryMap(platform)
    platformAccess = platform.platformAccess()
    dieOffset = platformAccess.x86PhysicalHierarchy().ccdDieNumberOffset()
    idMap = Kysy.PPRCoreTopologyPhysicalIDs(socket, (dieOffset + ccd), 0, 0, 0)
    accessInfo = memoryMap.accessInfo(idMap, address, Kysy.MEMORY_WRITE)

    memory_destination = accessInfo.destination()
    memory_type = accessInfo.mode()

    physical_cores = Kysy.PPRCoreTopologyPhysicalIDs(socket, ccd+_getDieOffset(_checkDieOffsetInclusion()), 0, 0, 0)
    size = Kysy.Bytes(dword_count * 4)
    mem_mapped = Kysy.PhysicalMemorySpace.mapMemory(platform.platformAccess(), physical_cores, address, size, memory_destination, memory_type, Kysy.MEMORY_ACCESS_SIZE_DEFAULT)
    mem_mapped.read()

    for index in range(0, dword_count):
        value = dram_array[index]
        for byte_offset in range(0, 4):
            mem_mapped.byte(4 * index + byte_offset, (value >> (8 * byte_offset)) & 0xFF)
        table.add_row([socket, ccd, hex(address), hex(value)])
        address += 4
    mem_mapped.write()

    if not pdm_stay:
        print("Exiting PDM mode()")
        try:
            go()
            go()
        except Exception as e:
            print(e)

    return table

def smn(address, data=None, socket=0, die=0):
    '''
    read/write a dword into register use smn method
    usage: 
        read -> smn(0x50100)
        write -> smn(0x50100, 0x201)
    
    address : register's smn address
    data : (optional) data to write into register
    socket : which socket to trigger smn address
    die : which die to trigger smn address
    '''
    reg = Kysy.SMNBufferAccess(platform.platformAccess(), socket, die+_getDieOffset(_checkDieOffsetInclusion()), address, 4, 1)
    if not data:
        reg.read()
        return reg.dword(0)
    else:
        reg.read()
        reg.dword(0,data)
        reg.write()
        reg.read()
        return reg.dword(0)
        
## NDA info ##
def gopi_info():
    gp_ver = vars(gp_core)
    
    from prettytable import PrettyTable as _PrettyTable
    table = _PrettyTable()
    table.field_names=["Info","Value"]
    for i in gp_ver.keys():
        table.add_row([i,gp_ver.get(i)])
    
    table.add_row(["hostname",kysy_platform.hostname])
    print (table)


# Initialize redfish with ipaddress
if host is not None:
    try:
        from component.bmc import _bmc
        _bmc.bmc_ip = host
        from component import bmc
    except ImportError:
        print("** Redfish plugin is only supported on BMC IP address.")

# Function to allow users to easily change BMC username and password
def change_bmc_username():
    bmc_user = input("Enter BMC username: ")
    if bmc_user is not None:
        bmc.bmc_user = bmc_user

def change_bmc_password():
    bmc_pwd = input("Enter BMC password: ")
    if bmc_pwd is not None:
        bmc.bmc_pw = bmc_pwd

