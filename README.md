# TCP-Mapper

1. Scans the provided directory
2. Extracts Windows Metadata & TCP Information
3. Inserts Data to MongoDB

## Guide

1. Setup The Python Environment

    ```$ python3 -m venv env```

    ```$ source env/bin/activate```

    ```$ pip install -r requirements.txt```

2. Add MongoDB SRV URL To Environment Variables

    ```$ export MONGO_SRV_URL="mongodb+srv://<....>"```

3. Updated Directories_To_Run.json

4. Run TCP_Tool.py

    ```$ python3 TCP_Tool.py ```


### Issue: *File Owners Listed as Everyone*

1. Make sure owners are now showing on network drive.
2. Do the Below. 
```python
    TCP_MONGO = FILE_Mongo("tcp")
    everyoneOwnerFiles = TCP_MONGO.get_everyone_owner()
    for file in everyoneOwnerFiles:
        process_single_file(file, Update=True)
```
