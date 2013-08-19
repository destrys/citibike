import xml.etree.ElementTree as ET
import csv
import sys

def loadStationPositions(inputfile):
    tree = ET.parse(inputfile)
    root = tree.getroot()
    
    station_locations = {}
    
    for child in root:
        for subchild in child:
            if subchild.tag == 'terminalName':
                termName = subchild.text
            if subchild.tag == 'lat':
                termLat = subchild.text
            if subchild.tag == 'long':
                termLong = subchild.text
            if subchild.tag == 'name':
                termString = subchild.text
        station_locations[termName] = {'lat':termLat,
                                       'long':termLong,
                                       'termString':termString}

    return station_locations

def printStationCSV(station_data,output_filename):
    with open(output_filename,'w') as outfile:
        filewriter = csv.writer(outfile,delimiter=',')
        for key in station_data.keys():
            filewriter.writerow([key]+[station_data[key]['lat']]+[station_data[key]['long']]+[station_data[key]['termString']])
    return None


if __name__ == '__main__':
    station_data = loadStationPositions(sys.argv[1])
    printStationCSV(station_data,sys.argv[2])
