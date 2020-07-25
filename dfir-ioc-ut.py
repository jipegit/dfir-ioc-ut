#!/usr/bin/env python
#
# DFIR IOC Unit Testing -- Jean-Philippe Teissier
#

import argparse
import yaml
import os
import platform
import time
import logging
import subprocess

try:
    import winreg
    WINREG_IMPORTED=True
except ImportError:
    logging.error('winreg module importation failed')

try:
    import win32event
    WIN32EVENT_IMPORTED=True
except ImportError:
    logging.error('win32event module importation failed')

try:
    import win32api
    WIN32API_IMPORTED=True
except ImportError:
    logging.error('win32api module importation failed')

try:
    import win32serviceutil
    WIN32SERVICEUTIL_IMPORTED=True
except ImportError:
    logging.error('win32serviceutil module importation failed')

import ctypes
from ctypes import wintypes

def create_unix_filepath(file_path):

    ''' Creates a file on a specific path (UNIX) '''
    logging.info('Creating file (UNIX): %s' % (file_path))
    try:
        logging.info('Creating needed (sub)directory')
        os.makedirs('/'.join(file_path.split('/')[:-1]), exist_ok=True)
    except OSError as e:
        logging.error(e.args[1])
        pass
    try:
        with open(file_path, 'w') as f:
            f.write('automatically generated artifact')
    except Exception as e:
        logging.error(e.args[1])
        pass

def create_win_filepath(file_path):

    ''' Creates a file on a specific path (WINDOWS) '''
    logging.info('Creating file (WINDOWS): %s' % (file_path))
    try:
        subdir = '\\'.join(file_path.split('\\')[:-1])
        logging.info('Creating needed (sub)directory: %s' % subdir)
        os.makedirs(subdir, exist_ok=True)
    except OSError as e:
        logging.error(e.args[1])
        pass
    try:
        with open(file_path, 'w') as f:
            f.write('automatically generated artifact')
    except Exception as e:
        logging.error(e.args[1])
        pass

def create_directory(directory):

    ''' Creates a specific directory '''
    logging.info('Creating directory: %s' % (directory))
    try:
        os.makedirs(directory, exist_ok=True)
    except OSError as e:
        logging.error(e.args[1])
        pass

def create_win_regkey(key, subkey, data_name, data_value, data_type):

    ''' Creates a Windows registry subkey and data '''
    _key = None
    logging.info('Creating Windows registry key')
    
    winreg_keytype = {'HKEY_LOCAL_MACHINE':winreg.HKEY_LOCAL_MACHINE}
    winreg_datatype = {'REG_SZ':winreg.REG_SZ}

    try:
        _key = winreg.CreateKeyEx(winreg_keytype[key], subkey, 0, winreg.KEY_SET_VALUE)
    except OSError as e:
        logging.error(e.args[1])
        pass
    if data_name:
        try:
            logging.info('Setting Windows registry key data value')
            winreg.SetValueEx(_key, data_name, 0, winreg_datatype[data_type], data_value)
        except OSError as e:
            logging.error(e.args[1])
            pass

def create_win_mutex(mutex_name):

    ''' Creates a Windows mutex '''
    # win32api_error = None
    # try:
    #     logging.info('Creating Mutex %s' % mutex_name)
    #     win32event.CreateMutex(None, False, mutex_name) #FIXME
    #     if WIN32API_IMPORTED:
    #         win32api_error = win32api.GetLastError()
    #         if win32api_error:
    #             logging.error(win32api_error) 
    # except Exception as e:
    #     logging.error(e.args[1])
    #     pass

    try:
        logging.info('Creating Mutex %s' % mutex_name)
        _CreateMutex = ctypes.windll.kernel32.CreateMutexA
        _CreateMutex.argtypes = [wintypes.LPCVOID, wintypes.BOOL, wintypes.LPCSTR]
        _CreateMutex.restype = wintypes.HANDLE
        _CreateMutex(None, False, mutex_name.encode('ascii', 'strict'))
    except Exception as e:
        logging.error(e.args[0])
        pass

def create_win_semaphore(semaphore_name):

    ''' Creates a Windows semaphore '''
    # win32api_error = None
    # try:
    #     logging.info('Creating Semaphore %s' % semaphore_name)
    #     win32event.CreateSemaphore(None, 0, 1, semaphore_name) #FIXME
    #     if WIN32API_IMPORTED:
    #         win32api_error = win32api.GetLastError()
    #         if win32api_error:
    #             logging.error(win32api_error)
    # except Exception as e:
    #     logging.error(e.args[1])
    #     pass

    try:
        logging.info('Creating Semaphore %s' % semaphore_name)
        CreateSemaphore = ctypes.windll.kernel32.CreateSemaphoreW
        CreateSemaphore.argtypes = [wintypes.LPCVOID, wintypes.LONG, wintypes.LONG, wintypes.LPCWSTR]
        CreateSemaphore.restype = wintypes.HANDLE
        CreateSemaphore(None, 0, 1, semaphore_name)
    except Exception as e:
        logging.error(e.args[0])
        pass


def create_win_service(service_name, service_display_name, service_description, service_exe_path):

    ''' Creates a Windows service '''
    
    try:
        logging.info('Creating Windows service %s (%s) for %s' % (service_name, service_display_name, service_exe_path))
        subprocess.run(['sc', 'create', service_name, 'binPath=', service_exe_path, 'DisplayName=', service_display_name])
        subprocess.run(['sc', 'description', service_name, service_description])
    except Exception as e:
        logging.error(e.args[1])
        pass

def create_win_task(task_name, task_exe_path, task_schedule):

    ''' Creates a Windows task '''
    
    try:
        logging.info('Creating Windows task %s (%s) for %s' % (task_name, task_schedule, task_exe_path))
        subprocess.run(['schtasks', '/Create', '/F', '/TN', task_name, '/TR', task_exe_path, '/SC', task_schedule])
    except Exception as e:
        logging.error(e.args[1])
        pass

def parse_artifacts_config(yaml_artifacts_config):

    ''' Parses a YAML artifacts configuration file '''

    _platform = platform.system()

    for artifact in yaml_artifacts_config['artifacts']:
        if artifact['type'] == 'unix_filepath' and _platform in ['Linux', 'Darwin']:
            create_unix_filepath(artifact['file_path'])
        if artifact['type'] == 'win_filepath' and _platform == 'Windows':
            create_win_filepath(artifact['file_path'])
        elif artifact['type'] == 'unix_directory' and _platform in ['Linux', 'Darwin']:
            create_directory(artifact['directory'])
        elif artifact['type'] == 'win_directory' and _platform == 'Windows':
            create_directory(artifact['directory'])    
        elif artifact['type'] == 'win_regkey' and _platform == 'Windows' and WINREG_IMPORTED:
            create_win_regkey(artifact['key'], 
                              artifact['subkey'], 
                              artifact['data_name'], 
                              artifact['data_value'], 
                              artifact['data_type'])
        elif artifact['type'] == 'win_mutex' and _platform == 'Windows' and WIN32EVENT_IMPORTED:
            create_win_mutex(artifact['mutex_name'])
        elif artifact['type'] == 'win_semaphore' and _platform == 'Windows' and WIN32EVENT_IMPORTED:
            create_win_semaphore(artifact['semaphore_name'])
        elif artifact['type'] == 'win_service' and _platform == 'Windows':
            create_win_service(artifact['service_name'], 
                               artifact['service_display_name'],
                               artifact['service_description'],
                               artifact['service_exe_path'])
        elif artifact['type'] == 'win_task' and _platform == 'Windows':
            create_win_task(artifact['task_name'],
                            artifact['task_exe_path'],
                            artifact['task_schedule'])
        else:
            logging.warning('Unsupported type %s' % artifact['type'])
    logging.info('Going to sleep now')
    while True:
        time.sleep(1)

def main():
    
    ''' Main function '''
    logging.basicConfig(level=logging.DEBUG)
    logging.info('Parsing artifacts configuration')
    yaml_artifacts_config = None

    parser = argparse.ArgumentParser(description='Create a set of system artifacts')
    parser.add_argument('-c', '--config', action='store', default=False, help='Yaml artifacts config file', required=True)

    args = parser.parse_args()

    if args.config:
        with open(args.config, 'r', encoding='utf-8') as stream:
            try:
                yaml_artifacts_config = yaml.safe_load(stream)
                logging.info('Artifacts configuration loaded')
            except yaml.YAMLError as e:
                logging.error(e.args[1])
  
    if yaml_artifacts_config:
        parse_artifacts_config(yaml_artifacts_config)

if __name__ == '__main__':
    main()