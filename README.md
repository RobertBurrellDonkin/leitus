> Enjoy Leitus, a suite of higher level functions for cryptographic drives.
> 
> Leitus is coded in Python for Linux under the GPLv2.
>
> - Robert Burrell Donkin, 2011

Configuration
=============

Supported options (easy to add more)

* With [json](http://www.json.org/)

Shared
------
 
- *name* maps drive to this name, for example `"name": "docs"`
- *target* mounts drive at this point, for example `"name": "docs"`

Drive By UUID 
-------------

Maps the encrypted drive with the given UUID to the given *name* and mounts
at the given *target*.
Distinquished by *UUID* attribute. 

- *UUID* identifies an encrypted drive, for example `"UUID":"35432a72-353f-48e8-8eac-6e5fe1d513a7"`

For example, the configuration json

     {"name": "music", "UUID":"65801645-6174-4269-9884-4b25c2027f7b", "target":"/home/rob/Music"}

maps the drive identified by "65801645-6174-4269-9884-4b25c2027f7b" to "music" 
and mounts at "/home/rob/Music"

Image Drive
----------

Maps the encrypted disc image at *source* and to the given *name* and mounts
at the given *target*.
Distinquished by *source* attribute. 

- *source* identifies an encrypted disc image, for example `"source":"small.img"`

* When *source* is absolute, this will be used directly
* Otherwise *source* is relative. Relative paths are resolved based on the drives.d directory.

For example, the configuration json

     {"source":"small.img","name": "small", "target":"/mnt/small"}

maps the disc image named "small.img" to "small" and mounts to point "/mnt/small".


Session Drive
-------------

Creates an encrypted session drive, available until the computer or the drive is closed. 

- *sizeInMeg* is the size of the session drive in megabytes, for example `"sizeInMeg": "2000"`
- *user* will own the session drives, for example `"user": "rdonkin"`
- *profiles* will initialise the session space, for example `"profiles": ["home", "gnome", "maven", "java6"]`

For example, the configuration json

     {"sizeInMeg": "2000", "user": "rdonkin", "profiles": ["home", "gnome", "maven", "java6"], "name": "neo"}

creates a new 2000M disc image owned by "rdonkin" and 
initialised with profiles "home", "gnome", "maven" and "java6" then maps it to "neo".

A temporary file image will be created and filled with noise, before being mounted and initialised.

Develops
========

* Use nose to run all the tests after making changes: nosetests
