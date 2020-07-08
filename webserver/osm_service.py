import json
import psycopg2

class OsmService:
    def __init__(self, user, password, host, port, database):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.database = database

        self.__connectToDatabase()

    def __connectToDatabase(self):
        self.connection = psycopg2.connect(user=self.user, password=self.password, host=self.host, port=self.port, database=self.database)

    def __parse_other_tags(self, other_tags):
        if other_tags is None:
            return dict()

        result = dict()
        for key, value in map(lambda tag: tag.split('"=>"'), other_tags[1:-1].split('","')):
            result[key] = value

        return result

    def __response_from_row(self, name, point, other_tags, distance):
        result = {
            "distance": distance,
            "unit": "m"
        }

        geojson = json.loads(point)
        result["location"] = {
            "lat": geojson["coordinates"][1],
            "lon": geojson["coordinates"][0]
        }

        if other_tags != None:
            result["other_tags"] = self.__parse_other_tags(other_tags)

        if name != None:
            result["name"] = name

        return result

    def __getCursor(self):
        if self.connection.closed:
            self.__connectToDatabase()

        return self.connection.cursor()

    def __executeQuery(self, query, parameters):
        cursor = self.__getCursor()

        cursor.execute(query, parameters)
        return list(cursor.fetchall())


    def getLanduse(self, lat, lon, radius):
        rows = self.__executeQuery("""\
            SELECT landuse, count(id), ST_Area(ST_Collect(geom)::geography, false)
            FROM multipolygons
            WHERE (landuse = 'commercial'
            OR landuse = 'industrial'
            OR landuse = 'residential'
            OR landuse = 'retail')
            AND ST_DWithin(geom::geography, ST_MakePoint(%(lon)s, %(lat)s)::geography, %(radius)s, false)
            GROUP BY landuse""", {
                "lat": lat,
                "lon": lon,
                "radius": radius
            })

        result = {}
        for row in rows:
            result[row[0]] = {
                "count": row[1],
                "total_area": row[2],
                "unit": "m^2"
            }

        return result

    def getParking(self, lat, lon, radius):
        rows = self.__executeQuery("""\
            SELECT name, ST_AsGeoJSON(ST_Centroid(geom)), other_tags, ST_Distance(geom::geography, ST_MakePoint(%(lon)s, %(lat)s)::geography) as dist
            FROM points
            WHERE ST_DWithin(geom::geography, ST_MakePoint(%(lon)s, %(lat)s)::geography, %(radius)s, false)
            AND other_tags like '%%"amenity"=>"parking"%%'
            AND NOT other_tags like '%%"access"=>"private"%%'
            AND NOT other_tags like '%%"access"=>"no"%%'
            AND NOT other_tags like '%%"access"=>"discouraged"%%'
            ORDER BY dist
            """, {
                "lat": lat,
                "lon": lon,
                "radius": radius
            })

        result = list()
        for row in rows:
            result.append(self.__response_from_row(*row))

        return result

    def getParks(self, lat, lon, radius):
        rows = self.__executeQuery("""\
            SELECT name, ST_AsGeoJSON(ST_Centroid(geom)), other_tags, ST_Distance(geom::geography, ST_MakePoint(%(lon)s, %(lat)s)::geography) as dist, ST_Area(geom)
            FROM multipolygons
            WHERE ST_DWithin(geom::geography, ST_MakePoint(%(lon)s, %(lat)s)::geography, %(radius)s, false)
            AND leisure like 'park'
            ORDER BY dist
            """, {
                "lat": lat,
                "lon": lon,
                "radius": radius
            })

        result = list()
        for row in rows:
            temp = self.__response_from_row(row[0], row[1], row[2], row[3])
            temp["area"] = row[4]
            temp["area_unit"] = "m^2"

            result.append(temp)

        return result


    def getMalls(self, lat, lon, radius):
        rows = self.__executeQuery("""\
            SELECT name, ST_AsGeoJSON(ST_Centroid(geom)), other_tags, ST_Distance(geom::geography, ST_MakePoint(%(lon)s, %(lat)s)::geography) as dist
            FROM points
            WHERE ST_DWithin(geom::geography, ST_MakePoint(%(lon)s, %(lat)s)::geography, %(radius)s, false)
            AND other_tags like '%%"shop"=>"mall"%%'
            ORDER BY dist
            """, {
                "lat": lat,
                "lon": lon,
                "radius": radius
            })

        result = list()
        for row in rows:
            result.append(self.__response_from_row(*row))

        return result

    def getChemists(self, lat, lon, radius):
        rows = self.__executeQuery("""\
            SELECT name, ST_AsGeoJSON(ST_Centroid(geom)), other_tags, ST_Distance(geom::geography, ST_MakePoint(%(lon)s, %(lat)s)::geography) as dist
            FROM points
            WHERE ST_DWithin(geom::geography, ST_MakePoint(%(lon)s, %(lat)s)::geography, %(radius)s, false)
            AND other_tags like '%%"shop"=>"chemist"%%'
            ORDER BY dist
            """, {
                "lat": lat,
                "lon": lon,
                "radius": radius
            })

        result = list()
        for row in rows:
            result.append(self.__response_from_row(*row))

        return result

    def getConvenience(self, lat, lon, radius):
        rows = self.__executeQuery("""\
            SELECT name, ST_AsGeoJSON(ST_Centroid(geom)), other_tags, ST_Distance(geom::geography, ST_MakePoint(%(lon)s, %(lat)s)::geography) as dist
            FROM points
            WHERE ST_DWithin(geom::geography, ST_MakePoint(%(lon)s, %(lat)s)::geography, %(radius)s, false)
            AND other_tags like '%%"shop"=>"convenience"%%'
            ORDER BY dist
            """, {
                "lat": lat,
                "lon": lon,
                "radius": radius
            })

        result = list()
        for row in rows:
            result.append(self.__response_from_row(*row))

        return result

    def getSupermarket(self, lat, lon, radius):
        rows = self.__executeQuery("""\
            SELECT name, ST_AsGeoJSON(ST_Centroid(geom)), other_tags, ST_Distance(geom::geography, ST_MakePoint(%(lon)s, %(lat)s)::geography) as dist
            FROM points
            WHERE ST_DWithin(geom::geography, ST_MakePoint(%(lon)s, %(lat)s)::geography, %(radius)s, false)
            AND other_tags like '%%"shop"=>"supermarket"%%'
            ORDER BY dist
            """, {
                "lat": lat,
                "lon": lon,
                "radius": radius
            })

        result = list()
        for row in rows:
            result.append(self.__response_from_row(*row))

        return result


    def getSchools(self, lat, lon, radius):
        rows = self.__executeQuery("""\
            SELECT name, ST_AsGeoJSON(ST_Centroid(geom)), other_tags, ST_Distance(geom::geography, ST_MakePoint(%(lon)s, %(lat)s)::geography) as dist
            FROM points
            WHERE ST_DWithin(geom::geography, ST_MakePoint(%(lon)s, %(lat)s)::geography, %(radius)s, false)
            AND other_tags like '%%"amenity"=>"school"%%'
            ORDER BY dist
            """, {
                "lat": lat,
                "lon": lon,
                "radius": radius
            })

        result = list()
        for row in rows:
            result.append(self.__response_from_row(*row))

        rows = self.__executeQuery("""\
            SELECT name, ST_AsGeoJSON(ST_Centroid(geom)), other_tags, ST_Distance(geom::geography, ST_MakePoint(%(lon)s, %(lat)s)::geography) as dist
            FROM other_relations
            WHERE ST_DWithin(geom::geography, ST_MakePoint(%(lon)s, %(lat)s)::geography, %(radius)s, false)
            AND other_tags like '%%"amenity"=>"school"%%'
            ORDER BY dist
            """, {
                "lat": lat,
                "lon": lon,
                "radius": radius
            })

        for row in rows:
            result.append(self.__response_from_row(*row))

        return result

    def getKindergarten(self, lat, lon, radius):
        rows = self.__executeQuery("""\
            SELECT name, ST_AsGeoJSON(ST_Centroid(geom)), other_tags, ST_Distance(geom::geography, ST_MakePoint(%(lon)s, %(lat)s)::geography) as dist
            FROM points
            WHERE ST_DWithin(geom::geography, ST_MakePoint(%(lon)s, %(lat)s)::geography, %(radius)s, false)
            AND other_tags like '%%"amenity"=>"kindergarten"%%'
            ORDER BY dist
            """, {
                "lat": lat,
                "lon": lon,
                "radius": radius
            })

        result = list()
        for row in rows:
            result.append(self.__response_from_row(*row))

        rows = self.__executeQuery("""\
            SELECT name, ST_AsGeoJSON(ST_Centroid(geom)), other_tags, ST_Distance(geom::geography, ST_MakePoint(%(lon)s, %(lat)s)::geography) as dist
            FROM other_relations
            WHERE ST_DWithin(geom::geography, ST_MakePoint(%(lon)s, %(lat)s)::geography, %(radius)s, false)
            AND other_tags like '%%"amenity"=>"kindergarten"%%'
            ORDER BY dist
            """, {
                "lat": lat,
                "lon": lon,
                "radius": radius
            })

        for row in rows:
            result.append(self.__response_from_row(*row))

        return result

    def getHospitals(self, lat, lon, radius):
        rows = self.__executeQuery("""\
            SELECT name, ST_AsGeoJSON(ST_Centroid(geom)), other_tags, ST_Distance(geom::geography, ST_MakePoint(%(lon)s, %(lat)s)::geography) as dist
            FROM points
            WHERE ST_DWithin(geom::geography, ST_MakePoint(%(lon)s, %(lat)s)::geography, %(radius)s, false)
            AND other_tags like '%%"amenity"=>"hospital"%%'
            ORDER BY dist
            """, {
                "lat": lat,
                "lon": lon,
                "radius": radius
            })

        result = list()
        for row in rows:
            result.append(self.__response_from_row(*row))

        return result

    def getDoctors(self, lat, lon, radius):
        rows = self.__executeQuery("""\
            SELECT name, ST_AsGeoJSON(ST_Centroid(geom)), other_tags, ST_Distance(geom::geography, ST_MakePoint(%(lon)s, %(lat)s)::geography) as dist
            FROM points
            WHERE ST_DWithin(geom::geography, ST_MakePoint(%(lon)s, %(lat)s)::geography, %(radius)s, false)
            AND other_tags like '%%"amenity"=>"doctors"%%'
            ORDER BY dist
            """, {
                "lat": lat,
                "lon": lon,
                "radius": radius
            })

        result = list()
        for row in rows:
            result.append(self.__response_from_row(*row))

        return result


    def getRailwayStations(self, lat, lon, radius):
        rows = self.__executeQuery("""\
            SELECT name, ST_AsGeoJSON(ST_Centroid(geom)), other_tags, ST_Distance(geom::geography, ST_MakePoint(%(lon)s, %(lat)s)::geography) as dist
            FROM points
            WHERE ST_DWithin(geom::geography, ST_MakePoint(%(lon)s, %(lat)s)::geography, %(radius)s, false)
            AND other_tags like '%%"railway"=>"station"%%'
            ORDER BY dist
            """, {
                "lat": lat,
                "lon": lon,
                "radius": radius
            })

        result = list()
        for row in rows:
            result.append(self.__response_from_row(*row))

        return result

    def getTramStations(self, lat, lon, radius):
        rows = self.__executeQuery("""\
            SELECT name, ST_AsGeoJSON(ST_Centroid(geom)), other_tags, ST_Distance(geom::geography, ST_MakePoint(%(lon)s, %(lat)s)::geography) as dist
            FROM points
            WHERE ST_DWithin(geom::geography, ST_MakePoint(%(lon)s, %(lat)s)::geography, %(radius)s, false)
            AND other_tags like '%%"railway"=>"tram_stop"%%'
            ORDER BY dist
            """, {
                "lat": lat,
                "lon": lon,
                "radius": radius
            })

        result = list()
        for row in rows:
            result.append(self.__response_from_row(*row))

        return result

    def getBusStations(self, lat, lon, radius):
        rows = self.__executeQuery("""\
            SELECT name, ST_AsGeoJSON(ST_Centroid(geom)), other_tags, ST_Distance(geom::geography, ST_MakePoint(%(lon)s, %(lat)s)::geography) as dist
            FROM points
            WHERE ST_DWithin(geom::geography, ST_MakePoint(%(lon)s, %(lat)s)::geography, %(radius)s, false)
            AND highway = 'bus_stop'
            ORDER BY dist
            """, {
                "lat": lat,
                "lon": lon,
                "radius": radius
            })

        result = list()
        for row in rows:
            result.append(self.__response_from_row(*row))

        return result
