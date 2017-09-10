

S2-Tick
===============
Customizable Sentinel-2 products downloader
-------------------------------------------

<img src="https://raw.githubusercontent.com/buele/Sentinel-2-Downloader/master/logo/s2-tick.png" alt="alt text" width="300" height="300">

S2-Tick is an automatic and customizable sentinel-2 products downloader.


[Docker](https://www.docker.com/)  containers are included in the package, facilitating the installation and running.


Source code is released under
the [MIT](https://opensource.org/licenses/MIT) license.





## Overview


*S2-Tick* gets automatically products from
[Sentinel-2 on AWS](http://sentinel-pds.s3-website.eu-central-1.amazonaws.com/) portal. Such a downloader is multithreaded and can be
fully customized in terms of AOI (Area of Interest) and Products Sensing Time.






- Cross-platform support
    - Ichnosat Platform provides the Docker containers

- Downloader
    - Get Sentinel-2 data from  [Sentinel-2 on AWS](http://sentinel-pds.s3-website.eu-central-1.amazonaws.com/)
    - Customizable features:
        - Tiles to download (UTM-MGRS Tile-ID)
        - Files to download for each tile (Image files and/or metadata)
        - Dates interval (Sensing time)
        - Number of parallel downloads at the same time




# Software architecture


## Overview




*Downloader* and *Processor* are the main modules of this platform. The schema with all modules involved follows:

![](https://raw.githubusercontent.com/SardegnaClimaOnlus/ichnosat/master/auto-docs/source/_static/ichnosat-modules.png)

## Downloader


This module is deputed to retrieve the list of available products and download them, on the basis of the configurations set by user.
The possible configurations to filter the list of products are:

- List of tiles
- List of files to download for each tile
- Sensing time interval (start - end )


### Class diagram

![](https://raw.githubusercontent.com/buele/Sentinel-2-Downloader/master/docs/downloader-class-diagram.png)


### Sequence diagram

![](https://raw.githubusercontent.com/SardegnaClimaOnlus/ichnosat/master/auto-docs/source/_static/downloader-sequence-diagram.png)



## Processor

The goal of this component is to process downloaded products.
Every processing algorithm is represented by C++ plugins. This means that *Processor* module is
extendible. Plugins are dynamic shared library (Linux environment)

The processor runs as http server to receive requests via http:

![](https://raw.githubusercontent.com/SardegnaClimaOnlus/ichnosat/master/auto-docs/source/_static/processor-web-interface.png)


When the POST /process http is received the *Processor* starts a processing task, spreading a pool of threads.
The number of threads is configurable via *conf.cfg* file.


If you want to develop a new plugin
for your processing purposes, please follows the tutorial:

[How to create a new plugin](https://sardegnaclimaonlus.github.io//ichnosat/how_to_create_a_new_plugin.html)

### Class diagram


![](https://raw.githubusercontent.com/SardegnaClimaOnlus/ichnosat/master/auto-docs/source/_static/processor-class-diagram.png)


### Sequence diagram

![](https://raw.githubusercontent.com/SardegnaClimaOnlus/ichnosat/master/auto-docs/source/_static/processor-sequence-diagram.png)


## System Manager

System Manager is the high level module to manage other modules.

### Class diagram

![](https://raw.githubusercontent.com/SardegnaClimaOnlus/ichnosat/master/auto-docs/source/_static/system_manager-class-diagram.png)




## Database

Database module contains the classes of ORM.
In this version (0.1) is used *SqlAlchemy* ORM.

### Class diagram

![](https://raw.githubusercontent.com/SardegnaClimaOnlus/ichnosat/master/auto-docs/source/_static/database-class-diagram.png)


### Database schema

![](https://raw.githubusercontent.com/SardegnaClimaOnlus/ichnosat/master/auto-docs/source/_static/database-schema.png)


## Folder Structure


The description of the main folders in the source code follows:

```

   |-- Dockerfile             # Docker file of ichnosat platform
   |-- LICENSE.TXT            # MIT license text
   |-- README.md              # README of the project (for github main page)
   |-- auto-docs              # Documentation sources and images
   |-- data_local
   |   |-- db                 # Postgresql database files (mounted by docker-compose)
   |   |-- inbox              # Temporary downloaded products by the Downloader
   |   |-- log                # Ichnosat logs
   |   |-- outbox             # Processed products folder
   |   |-- supervisord        # Supervisord log folder
   |-- docker-compose.yml     # Docker Compose definition file
   |-- src
   |   |-- core               # Main Modules source code (Downloader, Processor, System Manager)
   |   |-- data               # Database and Logger source code
   |   |-- gui                # Web GUI interface source code
   |   |-- presentation       # External interface (http) source code
   |   `-- tests              # Tests
   `-- vendors                # Third part dependencies

```

## External Inteface APIs
----------------------

[](https://raw.githubusercontent.com/SardegnaClimaOnlus/ichnosat/master/auto-docs/source/_static/external-interface-apis.png)




## Technologies


- **Docker and docker compose**: virtual image container
- **SqlAlchemy**: ORM framework for python
- **Supervisord**: Task manager
- **Valgrind**: Process monitoring
- **Sphinx**: Automatic Documentation for python
- **Flask**: light webserver
- **Nginx**: web server
- **Postgresql**: database
- **GDAL**: C/C++ library for satellite image processing
- **OpenJPG**: library to manage jpeg2000 images
- **Python 3.4**
- **crontab**
- **debian**
- **pip**
- **C++11**



## Download

[Source Code](https://github.com/SardegnaClimaOnlus/ichnosat/archive/master.zip)






docker-compose build
docker-compose up
docker-compose down


## Create database
curl -i -H "Accept: application/json" -H "Content-Type: application/json" -X GET localhost:5000/create-database

curl -X GET localhost:5000/products/pending