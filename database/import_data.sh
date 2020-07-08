#!/bin/bash

HOST="localhost"
PORT="5432"
USER="postgres"
PASSWORD="password"
ACTIVE_SCHEMA="public"

FILE="nordrhein-westfalen-latest.osm.pbf"
if [ -f "$FILE" ]; then
    echo "$FILE exists."
else
    echo "$FILE does not exist. downloading..."
    wget "http://download.geofabrik.de/europe/germany/nordrhein-westfalen-latest.osm.pbf"
fi

# ogr2ogr is part of the GDAL library see:
# https://gdal.org/index.html

ogr2ogr -progress --config PG_USE_COPY YES -f PostgreSQL "PG:host=$HOST port=$PORT user=$USER password=$PASSWORD active_schema=$ACTIVE_SCHEMA" -lco DIM=2 $FILE points -overwrite -lco GEOMETRY_NAME=geom -lco FID=id -nln public.points -nlt PROMOTE_TO_MULTI
ogr2ogr -progress --config PG_USE_COPY YES -f PostgreSQL "PG:host=$HOST port=$PORT user=$USER password=$PASSWORD active_schema=$ACTIVE_SCHEMA" -lco DIM=2 $FILE multipolygons -overwrite -lco GEOMETRY_NAME=geom -lco FID=id -nln public.multipolygons -nlt PROMOTE_TO_MULTI
ogr2ogr -progress --config PG_USE_COPY YES -f PostgreSQL "PG:host=$HOST port=$PORT user=$USER password=$PASSWORD active_schema=$ACTIVE_SCHEMA" -lco DIM=2 $FILE other_relations -overwrite -lco GEOMETRY_NAME=geom -lco FID=id -nln public.other_relations -nlt PROMOTE_TO_MULTI
