
# Link Google Drive

https://drive.google.com/drive/folders/1zweh24PkZ2N1fCCuBH56TsUuEs7bz0P_?usp=sharing

# Web Scraping

### Crawler: Scrapy
### Code: package pedocs

Use scrapy to generate a .csv file with meta-data and to download each article. 

### Requirements

`>> pip install scrapy`

The web scraping logic is implemented in `pedocs.spiders.pedocs_spyder.py`. 
To reproduce the result, specify the following setting

- in `pedocs.spiders.pedocs_spyder.py` specify the path to the .csv :
```
custom_settings["FEEDS"] = { '/path/to/dir/data.csv': { 'format': 'csv',}}
```

- in `pedocs.settings.py` specify the target folder for .pdf docs:
```
FILES_STORE = '/path/to/target_dir'
```

To start the spider run

```
scrapy crawl pedocs
```

# Convert to master data

### Requirements

`>> pip install pandas`

Convertion to `master.csv` has been executed in Konvertierung_in_normalisierte_Darstlg.ipynb.







