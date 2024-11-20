import keyboard, time, os, configparser
from tabulate import tabulate

parser = configparser.ConfigParser()
import re

#current_path = os.getcwd()
#current_path = re.split("\\\|/", current_path)
#project_folder = current_path[-1]
#current_path = current_path[0:len(current_path) - 1]
#yww start
import sys
if getattr(sys, 'frozen', False):   
    project_folder = 'Genoa'
    current_path = sys._MEIPASS
    current_path = re.split("\\\|/", current_path)
else:
    current_path = os.getcwd()
    current_path = re.split("\\\|/", current_path)
    project_folder = current_path[-1]
    current_path = current_path[0:len(current_path) - 1]
#yww end
current_path = current_path + ["gopi.cfg"]

def existing_config(pysystep):
    if os.path.exists(os.sep.join(current_path)):
        parser.read(os.sep.join(current_path))
        project_name = parser.get(project_folder, "project")
        targetname = parser.get(project_folder, "target")
        parser.clear()
        parser.read(pysystep)
        stepping = parser.get('stub_config', 'stepping')
        if targetname == "None": targetname = "Stub"
        print("Previuos config :\n")
        print("Project : {}\nTarget : {}".format(project_name, targetname))
        parser.clear()


def print_pysy_config(config):
    parser.read(config)
    enabled_ccd = parser.get("ccd_config", "enabled_ccds")
    cores_per_ccd = parser.get("ccd_config", "cores_per_ccd")
    threads_per_core = parser.get('ccd_config', 'threads_per_core')
    socket_number = parser.get("stub_config", "sockets")
    stepping = parser.get("stub_config", "stepping")
    print("Current Stub config set up : ")
    table = [['Stepping', stepping], ["Enabled CCDs", enabled_ccd], ['Cores per ccd', cores_per_ccd], ['Threads per core', threads_per_core], ['Number of socket', socket_number]]
    print(tabulate(table, tablefmt="plain"))
    parser.clear()


def readStubInput():
    # sys.stdout.write('%s(%s)%s:'%(caption, default,timeout))
    # sys.stdout.flush()
    while True:
        reconfig = input("Reconfiure stub config ? (y/n) \n")
        if reconfig.lower() == 'n':
            print("\nUsing default config")
            return reconfig
            break
        elif reconfig.lower() == 'y':
            print("\nReconfigure stub config. ")
            return reconfig
            break
        else:
            print("Please provide (y) for yes and (n) for no ")


def load_config(pysy_step):
    import KysyEnvironment
    import Kysy
    from colorama import Fore
    if os.path.exists(os.sep.join(current_path)):
        config = load_existing_config(project_folder, os.sep.join(current_path))
    else:
        print("No Previous config found !\n")
        config = new_config(project_folder, os.sep.join(current_path), pysy_step)

    connection_success = False
    connection_attempt = 1

    #yww start
    if getattr(sys, 'frozen', False):
        print(f"请稍等，正在尝试连接{config}")
    #yww end

    while not connection_success:
        try:
            wombat = Kysy.Wombat.create(config, "kysy", "kysy")
            platform = wombat.platform()
            connection_success = True
            print(f'{Fore.LIGHTGREEN_EX}CONNECTION SUCCESS{Fore.RESET}')
        except RuntimeError as runtime:
            if connection_attempt < 0:
                raise Exception(f'{Fore.LIGHTRED_EX}Failed to initialize wombat even after toggling TRST{Fore.RESET}') from runtime
            wombat = Kysy.Wombat.create(config, "kysy", "kysy")
            jtag = wombat.cpuJtag()
            print(f'{Fore.LIGHTYELLOW_EX}Failed to connect to device. Toggling TRST{Fore.RESET}')
            jtag.toggleTRST()
            connection_attempt -= 1

    return config


def load_existing_config(project, currentpath):
    parser.read(currentpath)
    if project in parser.sections():
        ipaddress = parser.get(project, "target")
    else:
        ipaddress = new_config(project, currentpath)
    parser.clear()
    return ipaddress


import sys, time


def readInput():
    while True:
        reconfig = input("Reconfigure previous config ? (y/n) \n")
        if reconfig.lower() == 'n':
            print("\nUsing default config")
            return reconfig
            break
        elif reconfig.lower() == 'y':
            print("\nReconfigure stub config. ")
            return reconfig
            break
        else:
            print("Please provide (y) for yes and (n) for no ")


def read_kysy_version():
    if os.path.exists(os.sep.join(current_path)):
        parser.read(os.sep.join(current_path))
        if parser.has_option(project_folder, 'kysy_version'):
            existing_version = parser.get(project_folder, 'kysy_version')
            parser.clear()
        else:
            parser.set(project_folder, 'kysy_version', '0')
            with open(os.sep.join(current_path), 'w') as kysy_version:
                parser.write(kysy_version)
            kysy_version.close()
            existing_version = "0"
    else:
        parser.read(os.sep.join(current_path))
        if project_folder not in parser.sections():
            parser.add_section(project_folder)
        parser.set(project_folder, 'kysy_version', '0')
        parser.set(project_folder, "project", project_folder)
        parser.set(project_folder, "target", "None")
        with open(os.sep.join(current_path), 'w') as kysy_version:
            parser.write(kysy_version)
        kysy_version.close()
        existing_version = "0"
    return existing_version


def write_kysy_version(version):
    parser.read(os.sep.join(current_path))
    parser.set(project_folder, 'kysy_version', version)
    with open(os.sep.join(current_path), 'w') as f:
        parser.write(f)
    f.close()
    parser.clear()


def pysy_config_write(config, project, ipaddress):
    # stepping = get_stepping(ipaddress)
    from pysy.utils import __main__

    __main__.main("--update_project {}".format(project.lower()))
    __main__.main("--update_mode {}".format("wombat"))
    # __main__.main("--update_stepping {}".format(stepping))
    __main__.main("--update_hostnam {}".format(ipaddress))


def kysy_config_write(config, project, var, val):
    parser.read(config)
    parser.set(project, var, val)
    with open(config, 'w') as lala:
        parser.write(lala)
    lala.close()
    parser.clear()


def stub_config(config, stepping, enabled_ccd, cores_per_ccd, thread_per_core, socket_number):
    parser.read(config)
    parser.set('stub_config', 'stepping', stepping.upper())
    parser.set('stub_config', 'sockets', socket_number)
    parser.set('ccd_config', 'enabled_ccds', enabled_ccd)
    parser.set('ccd_config', 'cores_per_ccd', cores_per_ccd)
    parser.set('ccd_config', 'threads_per_core', thread_per_core)
    with open(config, 'w') as fff:
        parser.write(fff)
    fff.close()
    parser.clear()


def new_config(project_folder=project_folder, config_path=os.sep.join(current_path), pysy_step=None):
    parser.read(config_path)
    if project_folder not in parser.sections():
        parser.add_section(project_folder)
    ip = input("Please provide wombat ip address/name : ")
    stepping = get_stepping(ip)
    parser.set(project_folder, "project", project_folder)
    parser.set(project_folder, "target", "{}".format(ip))
    with open(config_path, 'w') as xf:
        parser.write(xf)
    xf.close()
    parser.clear()
    if not os.path.exists(pysy_step):
        pysy_config_write(pysy_step, project_folder, ip)
    parser.read(pysy_step)
    #parser.set('stub_config', 'stepping', stepping)
    #with open(pysy_step, 'w') as pf:
    #    parser.write(pf)
    #pf.close()
    return ip


def get_stepping(ipaddress):
    import KysyEnvironment
    import Kysy
    import RegisterDef
    from colorama import Fore

    connection_success = False
    connection_attempt = 1
    while not connection_success:
        try:
            wombat = Kysy.Wombat.create(ipaddress, "kysy", "kysy")
            platform = wombat.platform()
            stepping = platform.platformAccess().chipInfo(RegisterDef.ChipInfo.CPU).revision().lower()
            connection_success = True
        except RuntimeError as runtime:
            if connection_attempt < 0:
                raise Exception(f'{Fore.LIGHTRED_EX}Failed to initialize wombat even after toggling TRST{Fore.RESET}') from runtime
            wombat = Kysy.Wombat.create(ipaddress, "kysy", "kysy")
            jtag = wombat.cpuJtag()
            print(f'{Fore.LIGHTYELLOW_EX}Failed to connect to device. Toggling TRST{Fore.RESET}')
            jtag.toggleTRST()
            connection_attempt -= 1
        except Exception as e:
            print("{}{}{}".format("\033[93m", e, "\033[0m"))
            exit(1)
    return stepping
