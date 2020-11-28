from shapely.geometry import mapping, Polygon
import fiona
import csv

list_coord = []
with open('coordinates.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        coord = (float(row[0]), float(row[1]))
        list_coord.append(coord)

poly = Polygon(list_coord)
schema = {
    'geometry': 'Polygon',
    'properties': {'id': 'int'},
}

with fiona.open('test.shp', 'w', 'ESRI Shapefile', schema) as c:
    c.write({
        'geometry': mapping(poly),
        'properties': {'id': 123},
    })
