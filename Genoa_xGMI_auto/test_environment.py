#!\usr\bin\python3
"""Put one line description for this module.

If we need to document more deeply this module we can document it here.


This module is developed and maintained by Server RAS Validation Team.
Contact information:
        Pysy Server Team
"""
import subprocess as _subprocess
import time as _time
import logging as _logging
import os as _os
from os import path as _path
from sys import version_info as _version_info
import requests as _requests
import sys as _sys
import re as _re
import json as _json
import configparser as _configparser
import coloredlogs as _coloredlogs
import pysy as _pysy
import zipfile as _zipfile
import tarfile as _tarfile
import readline as _readline
from enum import Enum as _Enum
from platform import system as _system
from pysy.utils.library import get_access_modes as _get_access_modes
from pysy.utils.library import get_project_names as _get_project_names
from pysy.utils.library import ACCESS_MODES as _ACCESS_MODES
from pysy.utils.library import PROJECT_NAMES as _PROJECT_NAMES
from pysy.utils.library import ACCESS_ENGINES as _ACCESS_ENGINES
from pysy.utils.errors import ServiceNotFound as _ServiceNotFound

logger = _logging.getLogger("test_environment")
_coloredlogs.install(level=_logging.INFO, logger=logger, fmt="%(message)s")

CONFIG_FILE_NAME = "python_config.ini"

_access_engine = None
_project_name = None
_access_mode = None
_stepping = None
_package = None
_engine_version = None

def get_pysy_path() -> str:
    """Get test_content directory path.

    This method is used to get the repository path.
    Args:
        None

    Returns:
        path (str): path where ras folder is located.
    """
    return _pysy.__path__[0]


def get_prj_cfg_path(project=None) -> str:
    """Get test_content directory path.

    This method is used to get the repository path.
    Args:
        None

    Returns:
        path (str): path where ras folder is located.
    """
    if project is None:
        project = get_project_name()
    return _path.join(get_pysy_path(), "config", project)


def get_cfg_file():
    """Get pysy cfg file"""
    config_file_path = _path.join(get_pysy_path(), CONFIG_FILE_NAME)
    python_config = _configparser.ConfigParser()
    python_config.read(config_file_path)
    return python_config


def get_stub_config():
    """ Get stub_config data from .ini file"""
    return get_cfg_file()["stub_config"]


def get_wombat_config():
    """ Get wombat_config data from .ini file"""
    return get_cfg_file()["wombat_config"]


def get_general_config():
    """ Get wombat_config data from .ini file"""
    return get_cfg_file()["general_config"]


def get_project_name():
    """ Get project name """
    global _project_name
    if get_access_mode() != _ACCESS_MODES.STUB:
        logger.warning(
            f"get_project_name method is deprecated, when running in {get_access_mode()} mode please use kysy_platform.get_project_name()"
        )
    if _project_name is None:
        _project_name = get_cfg_file()["mode"]["project_name"]
        if _project_name not in _get_project_names():
            raise Exception("Project '%s' is still not supported. Projects: %s"%(
                _project_name, _get_project_names()))
        logger.info("Project name '%s' from .ini file", _project_name)
    return _project_name


def get_access_mode():
    """ Get project name """
    global _access_mode
    if _access_mode is None:
        _access_mode = get_cfg_file()["mode"]["access_mode"]
        if _access_mode not in _get_access_modes():
            raise Exception("Access mode '%s' is not valid. Access modes: %s"%(
                _access_mode, _get_access_modes()))
        logger.info("Access mode '%s' from .ini file", _access_mode)
    return _access_mode


def get_stepping():
    """ Get stepping """
    global _stepping
    if get_access_mode() != _ACCESS_MODES.STUB:
        logger.warning(
            "get_stepping method is deprecated, when running in '%s' mode please use kysy_platform.get_stepping()",
            get_access_mode(),
        )
    if _stepping is None:
        _stepping = get_stub_config()["stepping"].lower()
        logger.debug("Stepping '%s' from .ini file", _stepping)
    return _stepping


def get_node_cfg_path(project=None) -> str:
    """Get test_content directory path.
    This method is used to get the repository path.
    Args:
        None
    Returns:
        path (str): path where ras folder is located.
    """
    if project is None:
        project = get_project_name()
    return _path.join(get_prj_cfg_path(project), 'node')

def get_node_json(project=None) -> list:
    """Get test_content directory path.
    This method is used to get the repository path.
    Args:
        None
    Returns:
        path (str): path where ras folder is located.
    """
    if project is None:
        project = get_project_name()
    f = _path.join(get_node_cfg_path(project), 'node.json')

    if not _path.exists(f):
        return []

    with open(f, 'r') as j:
        return _json.load(j)

def get_package():
    """Get package"""
    global _package
    project_mapping = {
        _PROJECT_NAMES.ROME: "SP3",
        _PROJECT_NAMES.MILAN: "SP3",
        _PROJECT_NAMES.GENOA: "SP5",
        _PROJECT_NAMES.BERGAMO: "SP5",
        _PROJECT_NAMES.SIENA: "SP6",
        _PROJECT_NAMES.SIENA_DENSE: "SP6",
        _PROJECT_NAMES.MI300A: "SP5",
        _PROJECT_NAMES.MI300X: "SP5",
        _PROJECT_NAMES.MI300C: "SP5"
    }
    if get_access_mode() != _ACCESS_MODES.STUB:
        logger.warning(
            "get_package method is deprecated, when running in '%s' mode please use kysy_platform.get_package()",
            get_access_mode(),
        )
    if _package is None:
        _package = get_stub_config()["package"].lower()
        if _package == 'default':
            _package = project_mapping.get(get_project_name(), None)
            logger.info(f"Package {_package} from default")
            return _package
        logger.info("Package '%s' from .ini file", _package)
    return _package


def write_cfg_file(config_file):
    config_file_path = _path.join(get_pysy_path(), CONFIG_FILE_NAME)
    with open(config_file_path, "w") as python_config:
        config_file.write(python_config)


def format_text(text):
    """ format text to snake"""
    def is_int(char):
        try:
            int(char)
            return True
        except ValueError:
            return False

    new_text = ""
    last_char = text[0]
    if is_int(last_char):
        raise Exception("Name cannot start with int")
    new_text += last_char
    for i in text[1:]:
        if not is_int(i):
            if is_int(last_char):
                new_text += "_%s"%i
                last_char = i
                continue
            is_lower = i.islower()
            if not is_lower and last_char.islower():
                new_text += "_"
        new_text += i
        last_char = i
    new_text = new_text.replace("__", "_")
    return new_text.lower()


def format_name(text):
    """ Format text to snake """
    def individual_name_format(name):
        regex = _re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return _re.sub('([a-z0-9])([A-Z])', r'\1_\2', regex).lower().replace("__", "_")
    return ".".join(individual_name_format(split_path) for split_path in text.split("."))


def get_regex_output(line, regex):
    """Check if text match with entered regex.

    Verify if entered line match with regex and return
    a dictionary with the matched groups.

    Args:
        line (str): text that needs to inspected.
        regex (str): regular expression.

    Returns:
        match, groups
        match  (bool): True if line match with regex else False
        groups (dict): Groups defined in regex
    """

    regex = _re.compile(regex)
    match = True
    groups = {}
    regex_match = regex.match(line)
    if regex_match:
        groups = regex_match.groupdict()
    else:
        match = False
    return match, groups


def get_index_from_path(path):
    """
    Obtain socket, ccd, ccx, core index
    Args:
        path (str): Node path

    Returns:
        Dict of index (dict)
    """
    indexes = {
        'socket': None,
        'ccd': None,
        'ccx': None,
        'core': None,
        'aid': None,
        'xcd': None
    }

    indexes_pattern = {
        'socket': 'socket(?P<index>\d+)',
        'ccd': 'ccd(?P<index>\d+)',
        'ccx': '(lthree|ccx)(?P<index>\d+)',
        'core': 'core(?P<index>\d+)',
        'aid': 'aid(?P<index>\d+)',
        'xcd': 'xcd(?P<index>\d+)'
    }

    for k, pattern in indexes_pattern.items():
        m = _re.search(pattern, path)
        if m:
            indexes[k] = int(m.group('index'))

    return indexes


def is_aHDS_services_enabled(host='localhost'):
    """
    Check aHDS Services is enabled
    Returns:
        Status (bool)
    """
    try:
        r = _requests.get(r'http://localhost:8085/swagger/index.html')
        if not r.ok:
            raise _ServiceNotFound(f'aHDS Service: localhost not found')
        return True
    except _requests.exceptions.ConnectionError:
        return False
    except _ServiceNotFound:
        return False
    except Exception as e:
        logger.error(f'Unexpected Error occurs: {e}')


def enable_aHDS_services():
    """
    Enable aHDS Services
    """
    if _sys.platform != 'win32':
        raise RuntimeError('Unable to start aHDS in Linux os')
    ahds_exe_path = (r"C:\Program Files\aHDS\publish\AHDSForWindows.exe")
    for _exe in ahds_exe_path:
        try:
            p = _subprocess.run(_exe, shell=True, timeout=10)
            _time.sleep(10)  # Buffer time for aHDS enable
            if not p.returncode:
                return
        except _subprocess.TimeoutExpired:
            # Handling on Window aHDS service, there is no exit code return
            if is_aHDS_services_enabled():
                return
    raise RuntimeError('start aHDS not found !!!')


def get_access_engine():
    """ Return Kysy Engine according to python version and installed Kysy Engine """
    global _access_engine
    if _access_engine is not None:
        return _access_engine
    if "access_engine" in get_cfg_file()["mode"]:
        access_engine = get_cfg_file()["mode"]["access_engine"]
        if access_engine != "auto":
            _access_engine = access_engine
            return access_engine
    if _version_info > (3,8):
        try:
            # return hKysy If python is greater than 3.8 and we have hKYSY
            import hKYSY22  # pylint: disable=import-outside-toplevel,unused-import
            check_hkysy_python_run_version()
            if is_aHDS_services_enabled():
                return _ACCESS_ENGINES.hKYSY
            _access_engine = _ACCESS_ENGINES.hKYSY
            return _ACCESS_ENGINES.hKYSY
        except ModuleNotFoundError:
            logger.debug("Python is > 3.8 and hKysy not found :(")
    try:
        import KysyEnvironment  # noqa: F401# pylint: disable=import-outside-toplevel,unused-import
        _access_engine = _ACCESS_ENGINES.KYSY4
        return _ACCESS_ENGINES.KYSY4
    except ModuleNotFoundError:
        try:
            # return hKysy If python is greater than 3.8 and we have hKYSY
            import hKYSY22  # pylint: disable=import-outside-toplevel,unused-import
            if is_aHDS_services_enabled():
                return _ACCESS_ENGINES.hKYSY
            _access_engine = _ACCESS_ENGINES.hKYSY
            return _ACCESS_ENGINES.hKYSY
        except ModuleNotFoundError as not_found:
            logger.debug("Adding kysy to python path")
            #yww start
            if getattr(_sys, 'frozen', False):
                kysy_python = _os.path.join((_os.path.join(_sys._MEIPASS, "Kysy4")), "Python")
            else:
                if _os.environ.get("KYSY_BASE") is None:
                    raise Exception(
                        "'KYSY_BASE' environment variable was not found, it was not possible to determine KYSY installation path") from not_found
                kysy_python = _os.path.join(_os.environ.get("KYSY_BASE"), "Python")
            #yww end
            _sys.path.append(kysy_python)
            import KysyEnvironment  # noqa: F401# pylint: disable=import-outside-toplevel,unused-import
            _access_engine = _ACCESS_ENGINES.KYSY4
            return _ACCESS_ENGINES.KYSY4  # pylint: disable=invalid-name
    raise RuntimeError("No valid Kysy Engine Found!!!")


def check_hkysy_python_run_version():
    if _version_info < (3,10):
        logger.warning(f'hKYSY should be installed in python 3.10 and above. Current installed at python version: {_version_info.major}.{_version_info.minor}')


def get_value_from_Enum(cls: _Enum, key:str):
    """
    Get Enum Value from key
    Args:
        cls (Enum): Enum class
        key(str): Key from Enum clas

    Returns:
        index (int): return index of key
    """
    for des in cls:
        if des.name.lower() == key.lower():
            return des.value
    raise RuntimeError(f'{key} not found in {cls}')


def get_description_from_Enum(cls: _Enum, value):
    for des in cls:
        if des.value == value:
            return des.name

    return 'Description Not found'


def get_config_path():
    if get_general_config()['lmdb_path'].lower() not in ('none', 'default'):
        return get_general_config()['lmdb_path']
    return _path.join(get_pysy_path(), 'config')


def get_engine_version():
    """ Get Kysy version for defined engine """
    global _engine_version
    if _engine_version is not None:
        return _engine_version
    if get_access_engine() == _ACCESS_ENGINES.KYSY4:
        import Kysy  # pylint: disable=import-error
        _engine_version = Kysy.LIBRARY_VERSION
        return _engine_version
    else:
        from hKYSY22.version import hKYSY as _hKYSY  # hkysy only available in python3.10 # pylint: disable=import-error
        if hasattr(_hKYSY, "Version"):
            return _hKYSY.Version
        return _hKYSY.LIBRARY_VERSION

def unzip(file_path, new_file_path):
    if file_path.endswith('.zip'):
        with _zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(new_file_path)

    elif file_path.endswith(('.tar', '.tar.gz', '.tar.bz2')):
        with _tarfile.open('.tar*', 'r') as tar_ref:
            tar_ref.extractall(new_file_path)

    else:
        raise ValueError('Unsupported file type')


def process_and_unzip(file_path):
    if not file_path.endswith(('.zip', '.tar', '.tar.gz', '.tar.bz2')) and not _path.exists(file_path):
        raise ValueError("The file given is not a zipped file or the file path does not exists")

    config_file_path = _os.path.dirname(get_prj_cfg_path())

    if config_file_path:
        print(f"Directory found at: {config_file_path}")
    else:
        print("Directory not found.")

    project_name = _path.basename(file_path).split('_')[0]
    new_folder_path = _os.path.join(config_file_path, project_name)

    if not _os.path.exists(new_folder_path):
        _os.makedirs(new_folder_path)
        print(f'New folder created at {new_folder_path}')

    unzip(file_path, new_folder_path)

    print(f"Extracted successfully to {new_folder_path}")

def str2bool(s):
    """
    Convert String to Bool
    Args:
        s (str): String to covert to bool

    Returns:
        bool
    """
    return s.lower() in ('yes', 'y', 'true', '1', 't')
