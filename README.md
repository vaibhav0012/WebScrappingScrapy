# WebScrappingScrapy

1. Setting Up Scrapy
    ```bash
    conda create -n scrapy_env
    conda activate scrapy_env
    conda install -c conda-forge scrapy
    conda install -c conda-forge protego

2. Starting your first project
    ```bash
    scrapy startproject dir_name
    cd dir_name/
    scrapy genspider spider_name website #exclude https and the final backslash as scrapy mamnages this in the backend
    scrapy shell  # Used for testing purpose only

3. Edit the spider_name.py file to fetch relevant data

4. Switch to the folder which stores scrapy.cfg file and use the below command to execute the spider
    ```bash
    spider crawl spider_name

5. To save a file as a json run the below command in the terminal:
    ```bash
    spider crawl spider_name -o file_name.json