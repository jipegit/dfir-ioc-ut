# DFIR IOC Unit testing

DFIR-IOC-ut provides an easy way to customize a (virtual) machine with common *system* artifacts to test Indicators Of Compromise.

It may help your team with different use cases:
 * IOC validation
 * Threat Hunting simulation
 * Security product (AV/EDR) testing

|   | Windows | Linux  | macOS |
|---|---------|--------|-------|
| File  | X | X | X |
| Directory | X | X | X |
| Registry Key  | X |   |   |
| Service  | X |   |   |
| Scheduled task  | X |   |   |
| Mutex  | X |   |   |
| Semaphore  | X |   |   |

# Output

![Screenshot](https://github.com/jipegit/dfir-ioc-ut/blob/master/resources/dfir_ioc_ut_run.png)

# Supported types

You can create the following artifacts depending on the platform of your target (virtual) machine:

* unix_directory
``` 
- type: unix_directory
  directory: /tmp/malwaredir
```
* win_directory
```
- type: win_directory
  directory: c:\malicious\path
```
* unix_filepath
```
- type: unix_filepath
  file_path: /tmp/malpath/malware
```
* win_filepath
```
- type: win_filepath
  file_path: C:\Windows\toto\malware.exe
```
* type: win_mutex
```
- type: win_mutex
  mutex_name: malware_mutex
```
* type: win_semaphore
```
- type: win_semaphore
  semaphore_name: malware_semaphore
```
* type: win_task
```
- type: win_task
  task_name: evil_task_name
  task_exe_path: C:\Windows\toto\malware.exe
  task_schedule: ONSTART
```
* win_service
```
- type: win_service
  service_name: evil_service_name
  service_display_name: evil_service_display_name
  service_description: evil_service_description
  service_exe_path: C:\Windows\toto\malware.exe
```
* win_regkey
```
- type: win_regkey
  key: HKEY_LOCAL_MACHINE
  subkey: Software\Microsoft\Windows\CurrentVersion\Run
  data_name: malware
  data_value: C:\Windows\toto\malware.exe
  data_type: REG_SZ
```

See. sample.yaml for examples.

# Requirements
* PyYAML
* pywin32

# Author

Jean-Philippe Teissier - @Jipe_

# License
Apache License Version 2.0