# GeoIP-txt2dat-converter

This is a simple comverter from "txt" file with list of network subnets to GeoIP "dat" format. 
GeoIP "dat" file further may be used with NGINX ngx_http_geoip_module module wich creates variables with values depending on the client IP address, using the precompiled GeoIP databases.

## Requirements: 
txt2csv.py works on Python3 <br />
csv2dat.py works on Python2 <br />

**Python2** <br />
pip install ipaddr <br />
pip install pygeoip <br />

**Linux:** <br />
apt-get install ipcalc <br />
apt-get install aggregate <br />

## Usage:
Input txt file example: 
```
31.40.24.0/22
31.135.208.0/21
31.148.144.0/22
31.148.208.0/22
37.110.208.0/21
46.8.35.0/24
46.227.120.0/21
```
Convert TXT file with network subnets to CSV file <br />
python3 ./txt2csv.py -i test.txt  -o test2_output.csv <br />

Convert CSV file to DAT format <br />
python csv2dat.py -w mmcountry.dat mmcountry ./test2_output.csv <br />
