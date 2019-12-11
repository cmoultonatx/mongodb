from pymongo import MongoClient, GEOSPHERE
from pprint import pprint
import json
from pymongo.errors import (PyMongoError, BulkWriteError)

pw = "sumner67"
geojson_path = "static/countries.geojson"

client = MongoClient("mongodb+srv://cmoulton:{0}@cmoultonatx-6zok5.mongodb.net/countries?retryWrites=true&w=majority".format(pw))
db = client.countries
server_status = db.command('serverStatus')
assert server_status['ok']
print("Connection OK :)")

'''
Inputs: Coordinates [lon,lat]
Outputs: Polygon/MultiPolygon GeoJSON object of corresponding country
'''
def get_geojson(coords):

    query = {
      'location': {
         "$geoIntersects": {
            "$geometry": {
               "type": "Point" ,
               "coordinates": coords
            }
         }
      }
    }

    cursor = db['countries'].find_one(query)
    pprint(json.dumps(cursor['location']))


#
# ####FROM HERE DOWN IS UPLOADING
# with open(geojson_path,'r') as f:
#     geojson = json.loads(f.read())
#
# if geojson:
#     print("True")
# #
# collection = db['countries']
# collection.delete_many({})
# db['countries'].ensure_index([("location",GEOSPHERE)])
# bulk = db['countries'].initialize_unordered_bulk_op()
# # print(geojson)
# for feature in geojson['features']:
#     print(feature['properties']['Country'])
#     # print(feature)
#     out = {
#             'name':feature['properties']['Country'],
#             "type":'Feature',
#             'location':{
#                 'type':feature['geometry']['type'],
#                 'coordinates':feature['geometry']['coordinates']
#             }
#         }
# #
#
#     result = db['countries'].insert_one(out)
#     # db.ensure_index('GEOSPHERE')
#     print(result.inserted_id)
