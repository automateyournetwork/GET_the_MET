import requests
from requests.adapters import HTTPAdapter, Retry
import json
import time
import os
# -------------------------
# Jinja2
# -------------------------
from jinja2 import Environment, FileSystemLoader
template_dir = 'Template/'
env = Environment(loader=FileSystemLoader(template_dir))
newline = '\n'
object_template = env.get_template('object.j2')
s = requests.Session()
retries = Retry(total=5, backoff_factor=1, status_forcelist=[ 502, 503, 504 ])
s.mount('http://', HTTPAdapter(max_retries=retries))
master_list = requests.request("GET","https://collectionapi.metmuseum.org/public/collection/v1/objects")
master_list_json = master_list.json()
for art_object in master_list_json['objectIDs']:
    art_object_details = s.get(f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{ art_object }")
    art_object_details_json = art_object_details.json()
    parsed_output = object_template.render(art_to_template = art_object_details_json)
    if not os.path.exists(f"MindMaps/{ art_object_details_json['department'].replace(',',' ') }"):
        os.makedirs(f"MindMaps/{ art_object_details_json['department'].replace(',',' ') }")
    with open(f"MindMaps/{ art_object_details_json['department'].replace(',',' ') }/{ art_object_details_json['objectID'] } { art_object_details_json['title'][:100].replace(',',' ').replace('/',' ').replace('.',' ').replace(newline,' ') } { art_object_details_json['accessionYear'] }.md", "w") as fh:
        fh.write(parsed_output)                
        fh.close()
    print(f"{ art_object_details_json['department'] } { art_object_details_json['title'].replace(',',' ').replace('/',' ').replace('.',' ').replace(newline,' ') } { art_object_details_json['accessionYear'] } Transformed to a Mind Map!")