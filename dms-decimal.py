# coding: utf-8
#!/usr/bin/env python3
import re
import csv
import json

def parse_dms(dms_string):
    p = "(?P<degrees>[\d]{1,3})° (?P<minutes>[\d]{1,3})’ (?P<seconds>[\d\.]{1,5})”"
    m = re.search(p, dms_string)
    return m.groupdict()

def dms_to_decimal(dms_string):
    parsed = parse_dms(dms_string)
    return int(parsed['degrees']) + float(parsed['minutes'])/60 + float(parsed['seconds'])/3600

assert parse_dms("106° 52’ 57.54”") == {'seconds': '57.54', 'degrees': '106', 'minutes': '52'}
assert dms_to_decimal("106° 52’ 57.54”") == 106.88265

def main():
    locations = {}
    with open('mn-aq-stations.csv') as f:
        f_csv = csv.DictReader(f)
        headers = ['Station', 'Province/City', 'Sub-province', 'Longitude', 'Latitude']
        with open('decimal.csv', 'w') as fw:
            fw_csv = csv.writer(fw)
            fw_csv.writerow(headers)
            for row in f_csv:
                city = row['Аймаг']
                name = row['Хяналтын цэгийн нэр']
                sub_province = row.get('Сум', '')
                longitude_dms = row.get('Уртраг')
                latitude_dms = row.get('Өргөрөг')
                if longitude_dms:
                    longitude = dms_to_decimal(longitude_dms)
                    latitude = dms_to_decimal(latitude_dms)
                    row = [name, city, sub_province, longitude, latitude]
                    fw_csv.writerow(row)

if __name__ == "__main__":
    main()
