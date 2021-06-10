#!/bin/bash
#turn json files into geojson and create the summary
# TODO: in this version is assumed that json files have the0 word Camera in his name. 
PARENT_FOLDER=${1:-.}
echo PARENT_FOLDER
jq -s '[.[] | {"name":.name, "thumbnail":.thumbnail, "point":[.longitude, .latitude], "species_colonies":.species_colonies}]' "$PARENT_FOLDER"/*Camera*.json>summary.json
for f in "$PARENT_FOLDER"/*Camera*.json
do
jq '{"type":"Feature", "id":(.name|gsub("\\s+|\\.jpg"; "")), "geometry":{"type":"Point", "coordinates":[.longitude, .latitude]}, "properties":.}' "$f" > "${f%json}geojson"
done

