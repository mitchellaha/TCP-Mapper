# TCP-Mapper

Extracts JSON String From .tcp Files in Provided Directory and Outputs to **.json** or **.geojson** feature collection.

------
### To-Do

- [ ] Remove Unneeded requirements from requirements.txt
- [ ] PyMongo Connection To Upload .tcp Info to MongoDB Database
- [ ] Add QT GUI
- [ ] Add External Documentation For Each Function/Class
- [ ] Maybe Make a Better Icon?

------

### Python Environment Setup

1. Setup The Environment

    ~~~
    $ python3 -m venv env
    ~~~

2. Set The Environment

    ~~~
    $ source env/bin/activate
    ~~~

3. Install Dependencies 

    ~~~
    $ pip install -r requirements.txt
    ~~~

4. Confirm Python Environment

    ~~~
    $ which python
    ~~~

----

### Build Guide

Single File Standalone Build

```
pyinstaller -F -i src\ico\icon.ico main.py
```

Un-Packed Standalone Build

```
pyinstaller -F -i src\ico\icon.ico main.py
```