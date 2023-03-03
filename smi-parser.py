#!/usr/bin/env python3
"""
This script will parse out the trip data from the SMI file generated
by the Caroolive Dashcam app from Pokevian.
It decodes the base64 encoded data and re-inserts the decoded GPS into a new
SMI file, and generates a KML for the trip details.
"""

import base64
import argparse
import sys
from datetime import datetime as dt
import os
import simplekml

__version__ = '1.0.0'
__date__ = '2023-03-02'
__author__ = 'Corey Forman @digitalsleuth'


def generate_kml(filename, coordinates, all_data):
    """Generates a KML file from the trip data"""
    normal_icon = 'https://www.gstatic.com/mapspro/images/stock/503-wht-blank_maps.png'
    highlight_icon = 'https://www.gstatic.com/mapspro/images/stock/503-wht-blank_maps.png'
    kml = simplekml.Kml()
    trip = kml.newlinestring(name=filename, tessellate=1)
    trip.stylemap.normalstyle.labelstyle.scale = 0
    trip.stylemap.normalstyle.iconstyle.color = 'ff3644db'
    trip.stylemap.normalstyle.iconstyle.scale = 1
    trip.stylemap.normalstyle.iconstyle.icon.href = normal_icon
    trip.stylemap.normalstyle.iconstyle.hotspot.x = 32
    trip.stylemap.normalstyle.iconstyle.hotspot.xunits = "pixels"
    trip.stylemap.normalstyle.iconstyle.hotspot.y = 64
    trip.stylemap.normalstyle.iconstyle.hotspot.yunits = "insetPixels"
    trip.stylemap.normalstyle.linestyle.color = 'ffff6712'
    trip.stylemap.normalstyle.linestyle.width = 5

    trip.stylemap.highlightstyle.labelstyle.scale = 1
    trip.stylemap.highlightstyle.iconstyle.color = 'ff3644db'
    trip.stylemap.highlightstyle.iconstyle.scale = 1
    trip.stylemap.highlightstyle.iconstyle.icon.href = highlight_icon
    trip.stylemap.highlightstyle.iconstyle.hotspot.x = 32
    trip.stylemap.highlightstyle.iconstyle.hotspot.xunits = "pixels"
    trip.stylemap.highlightstyle.iconstyle.hotspot.y = 64
    trip.stylemap.highlightstyle.iconstyle.hotspot.yunits = "insetPixels"
    trip.stylemap.highlightstyle.linestyle.color = simplekml.Color.red
    trip.stylemap.highlightstyle.linestyle.width = 7.5

    start_time = dt.utcfromtimestamp(int(all_data[0][0]) / 1000).strftime('%Y-%m-%d %H:%M:%S UTC')
    end_time = dt.utcfromtimestamp(int(all_data[-1][0]) / 1000).strftime('%Y-%m-%d %H:%M:%S UTC')

    trip_times = f'{filename}\nTrip starts at {start_time}\nTrip ends at {end_time}'
    trip.stylemap.highlightstyle.balloonstyle.text = trip_times
    trip.stylemap.highlightstyle.balloonstyle.bgcolor = simplekml.Color.white
    trip.stylemap.highlightstyle.balloonstyle.textcolor = simplekml.Color.black
    trip.description = ''
    for coord in coordinates:
        trip.description += f'{coord[0]},{coord[1]}\n'
    trip.coords = coordinates
    start_point = kml.newpoint(name=f'Start - {start_time}')
    start_point.coords = [coordinates[0]]
    start_point.style.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/paddle/A.png'
    end_point = kml.newpoint(name=f'End - {end_time}')
    end_point.coords = [coordinates[-1]]
    end_point.style.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/paddle/B.png'
    try:
        kml.save(f'{filename}.kml')
        print(f'KML file generated - {filename}.kml')
    except Exception as err:
        print(f'Error encountered - {err}')

def parse_smi(smi_input):
    """Parses through the SMI file to decode the base64 data"""
    try:
        smi_file = open(smi_input, 'r')
        output = f'{smi_input}2'
        smi_output = open(output, 'w')
        smi_read = smi_file.readlines()
        coords = []
        all_data = []
        for line in smi_read:
            if '<!--' and ' -->' in line:
                extra_data = line.replace('<P Class=ENCC ><!--', '').replace(' -->', '').replace('\t', '')
                decoded_data = ''
                values = []
                for section in extra_data.split(' '):
                    decoded_data += (base64.b64decode(section).decode() + '')
                for value in decoded_data.split(';'):
                    values.append(value)
                coords.append((values[5], values[4]))
                all_data.append(values)
                decoded_line = line.replace(line, (f'\t<P Class=ENCC >{values[4]} {values[5]}\n'))
                smi_output.write(f'\t<P Class=ENCC ><!--{decoded_data} -->\n')
                smi_output.write(decoded_line)
            else:
                smi_output.write(line)
        print(f'Output saved as {output}. Generating KML data...')
        generate_kml(smi_input, coords, all_data)
        smi_output.close()
        os.remove(output)
    except FileNotFoundError:
        print(f'Filename {smi_input} does not exist - check your file/path and try again')

def main():
    """Argument Parsing"""
    arg_parse = argparse.ArgumentParser(description=f'SMI Parser for Caroolive data v{str(__version__)}')
    arg_parse.add_argument('-i', metavar='input_file', help='SMI file')

    if len(sys.argv[1:]) == 0:
        arg_parse.print_help()
        arg_parse.exit()

    args = arg_parse.parse_args()
    parse_smi(args.i)

if __name__ == '__main__':
    main()
