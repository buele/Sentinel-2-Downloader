

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


# How to build

```
cd <project_path>
docker-compose build
```



## Create database


curl -X GET localhost:5000/products/pending
# How to run
 1. Launch the dockers
```
docker-compose up
```

 2. Create database (only first execution)

Calling the api to create the database via http request:
```
curl -i -H "Accept: application/json" -H "Content-Type: application/json" -X GET localhost:5000/create-database
```

 3. Launch the downloader

```
curl -i -H "Accept: appliccurl -i -H "Accept: application/json" -H "Content-Type: application/json" -X GET localhost:5000/start-downloader
```

 4. Get list of downloading products

```
curl -i -H "Accept: appliccurl -i -H "Accept: application/json" -H "Content-Type: application/json" -X GET localhost:5000/products/downloading
```

 5. Get list of pending products

```
curl -i -H "Accept: appliccurl -i -H "Accept: application/json" -H "Content-Type: application/json" -X GET localhost:5000/products/pending
```


# How to stop
```
docker-compose down
```

# Customizations

## Set Tiles to download

1. Edit the *Downloader* configuration file

```

   vim /usr/downloader/src/core/config/config.cfg
```

2. Set the list of tiles using the comma ',' as separator, in the 'tiles' key; e.g.:

```
   tiles=32/T/ML,32/T/NL,32/T/MK,32/T/NK,32/S/MJ,32/S/NJ
```


## Set files to download for each tile

1. Edit the *Downloader* configuration file

```
   vim /usr/downloader/src/core/config/config.cfg
```
2. Set the list of tiles using the comma ',' as separator, in the 'files_to_download' key; e.g.:


```
   files_to_download=B04.jp2,B08.jp2
```

## Set Sensing time interval

You can filter the products to download, setting the sensing time interval.
The interval is composed of *start* date and *end* date.

1. Edit the *Downloader* configuration file

```
   vim /usr/downloader/src/core/config/config.cfg
```

2. Set the sensing time **start**, in the 'start_date' key; e.g.:


```
   start_date=2016/07/13
```

3. Set the sensing time **end**, in the 'end_date' key; e.g.:

```
   end_date=2017/07/13
```


It is possible to set *NOW* as sensing time *end*, this means that the *Downloader* for every download cycle consider as sensing time *end* the current date; e.g.:

```
   end_date=NOW
```

## Set how many parallels download threads

You can define how many parallels download run in the same time:

1. Edit the *Downloader* configuration file

```
   vim /usr/downloader/src/core/config/config.cfg
```
2. Set how many threads the *Downloader* launches, in the 'parallel_downloads' key; e.g.:
```
   parallel_downloads=2
```


# Software architecture


## Overview



This module is deputed to retrieve the list of available products and download them, on the basis of the configurations set by user.
The possible configurations to filter the list of products are:

- List of tiles
- List of files to download for each tile
- Sensing time interval (start - end )


### Class diagram

![](https://raw.githubusercontent.com/buele/Sentinel-2-Downloader/master/docs/downloader-class-diagram.png)


### Sequence diagram

![](https://raw.githubusercontent.com/SardegnaClimaOnlus/ichnosat/master/auto-docs/source/_static/downloader-sequence-diagram.png)




## System Manager

System Manager is the high level module to manage other modules.

### Class diagram

![](https://raw.githubusercontent.com/SardegnaClimaOnlus/ichnosat/master/auto-docs/source/_static/system_manager-class-diagram.png)



## Database

Database module contains the classes of ORM.
In this version (0.1) is used *SqlAlchemy* ORM.

### Class diagram

![](https://raw.githubusercontent.com/buele/Sentinel-2-Downloader/master/docs/database-class-diagram.png)


### Database schema

![](https://raw.githubusercontent.com/buele/Sentinel-2-Downloader/master/docs/database-schema.png)




## Technologies


- **Docker and docker compose**: virtual image container
- **SqlAlchemy**: ORM framework for python
- **Supervisord**: Task manager
- **Flask**: light webserver
- **Postgresql**: database
- **Python 3.4**
- **crontab**
- **debian**
- **pip**










