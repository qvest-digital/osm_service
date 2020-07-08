# Fix Cannot import name 'cached_property': https://stackoverflow.com/a/60157748/3593881
import werkzeug
werkzeug.cached_property = werkzeug.utils.cached_property
from flask import Flask
from flask.json import jsonify
from osm_service import OsmService
from flask_restplus import Api, Resource, reqparse

app = Flask(__name__)
app.config.from_envvar('SETTINGS_FILE')

with app.app_context():
    osm = OsmService(app.config["DATABASE_USER"], app.config["DATABASE_PASSWORD"], app.config["DATABASE_HOST"], app.config["DATABASE_PORT"], app.config["DATABASE_NAME"])

api = Api(app, version='1.0', title='OSM Service API',
    description='Documentation for the OSM Service API.')

ns = api.namespace('relative', description='Operations for getting data relative to a given point')

relative_arguments = reqparse.RequestParser()
relative_arguments.add_argument('latitude', type=float, required=True)
relative_arguments.add_argument('longitude', type=float, required=True)
relative_arguments.add_argument('radius', type=int, required=True)


@ns.route('/<float:latitude>,<float:longitude>/<int:radius>')
class FullReport(Resource):
    @api.doc(responses={200: 'OK', 500: 'Internal Server Error'},
             params={'latitude': 'Specify the latitude associated with the point.',
                     'longitude': 'Specify the longitude associated with the point.',
                     'radius': 'Specify the radius (meters) covering the circular region of interest around the point '
                               '(coordinate) described by the latitude and longitude.'})
    @api.expect(relative_arguments, validate=True)
    def get(self, latitude, longitude, radius):
        """Returns the full report: Landuse, Parking, Chemists, Convenience Stores, Supermarkets, Malls, Schools, Kindergartens, Hospitals, Doctors, Railway Stations, Tram Stations, Bus Stations within a radius around a point described by the given latitude and longitude."""

        try:
            return {
                "input": {
                    "center": {
                        "lat": latitude,
                        "lon": longitude
                    },
                    "radius": radius
                },
                "result": {
                    "relative_type_of_area": osm.getLanduse(latitude, longitude, radius),

                    "malls": osm.getMalls(latitude, longitude, radius),
                    "chemists": osm.getChemists(latitude, longitude, radius),
                    "convenience": osm.getConvenience(latitude, longitude, radius),
                    "supermarkets": osm.getSupermarket(latitude, longitude, radius),

                    "parks": osm.getParks(latitude, longitude, radius),
                    "parking": osm.getParking(latitude, longitude, radius),
                    "schools": osm.getSchools(latitude, longitude, radius),
                    "kindergartens": osm.getKindergarten(latitude, longitude, radius),
                    "hospitals": osm.getHospitals(latitude, longitude, radius),
                    "doctors": osm.getDoctors(latitude, longitude, radius),

                    "railway_stations": osm.getRailwayStations(latitude, longitude, radius),
                    "tram_stations": osm.getTramStations(latitude, longitude, radius),
                    "bus_stations": osm.getBusStations(latitude, longitude, radius),
                }
            }, 200
        except:
            return "", 500


@ns.route('/<float:latitude>,<float:longitude>/<int:radius>/malls')
class MallReport(Resource):
    @api.doc(responses={200: 'OK', 500: 'Internal Server Error'},
             params={'latitude': 'Specify the latitude associated with the point.',
                     'longitude': 'Specify the longitude associated with the point.',
                     'radius': 'Specify the radius (meters) covering the circular region of interest around the point '
                               '(coordinate) described by the latitude and longitude.'})
    @api.expect(relative_arguments, validate=True)
    def get(self, latitude, longitude, radius):
        """Returns the Malls within a radius around a point described by the given latitude and longitude."""
        try:
            return osm.getMalls(latitude, longitude, radius), 200
        except Exception as e:
            print(e)
            return "", 500


@ns.route('/<float:latitude>,<float:longitude>/<int:radius>/chemists')
class ChemistReport(Resource):
    @api.doc(responses={200: 'OK', 500: 'Internal Server Error'},
             params={'latitude': 'Specify the latitude associated with the point.',
                     'longitude': 'Specify the longitude associated with the point.',
                     'radius': 'Specify the radius (meters) covering the circular region of interest around the point '
                               '(coordinate) described by the latitude and longitude.'})
    @api.expect(relative_arguments, validate=True)
    def get(self, latitude, longitude, radius):
        """Returns the Chemists within a radius around a point described by the given latitude and longitude."""
        try:
            return osm.getChemists(latitude, longitude, radius), 200
        except Exception as e:
            print(e)
            return "", 500


@ns.route('/<float:latitude>,<float:longitude>/<int:radius>/convenience')
class ConvenienceReport(Resource):
    @api.doc(responses={200: 'OK', 500: 'Internal Server Error'},
             params={'latitude': 'Specify the latitude associated with the point.',
                     'longitude': 'Specify the longitude associated with the point.',
                     'radius': 'Specify the radius (meters) covering the circular region of interest around the point '
                               '(coordinate) described by the latitude and longitude.'})
    @api.expect(relative_arguments, validate=True)
    def get(self, latitude, longitude, radius):
        """Returns the Convenience Stores within a radius around a point described by the given latitude and longitude."""
        try:
            return osm.getConvenience(latitude, longitude, radius), 200
        except Exception as e:
            print(e)
            return "", 500


@ns.route('/<float:latitude>,<float:longitude>/<int:radius>/supermarkets')
class SupermarketReport(Resource):
    @api.doc(responses={200: 'OK', 500: 'Internal Server Error'},
             params={'latitude': 'Specify the latitude associated with the point.',
                     'longitude': 'Specify the longitude associated with the point.',
                     'radius': 'Specify the radius (meters) covering the circular region of interest around the point '
                               '(coordinate) described by the latitude and longitude.'})
    @api.expect(relative_arguments, validate=True)
    def get(self, latitude, longitude, radius):
        """Returns the Supermarkets within a radius around a point described by the given latitude and longitude."""
        try:
            return osm.getSupermarket(latitude, longitude, radius), 200
        except Exception as e:
            print(e)
            return "", 500


@ns.route('/<float:latitude>,<float:longitude>/<int:radius>/landuse')
class LanduseReport(Resource):
    @api.doc(responses={200: 'OK', 500: 'Internal Server Error'},
             params={'latitude': 'Specify the latitude associated with the point.',
                     'longitude': 'Specify the longitude associated with the point.',
                     'radius': 'Specify the radius (meters) covering the circular region of interest around the point '
                               '(coordinate) described by the latitude and longitude.'})
    @api.expect(relative_arguments, validate=True)
    def get(self, latitude, longitude, radius):
        """Returns the Landuse within a radius around a point described by the given latitude and longitude."""
        try:
            return osm.getLanduse(latitude, longitude, radius), 200
        except Exception as e:
            print(e)
            return "", 500


@ns.route('/<float:latitude>,<float:longitude>/<int:radius>/parking')
class ParkingReport(Resource):
    @api.doc(responses={200: 'OK', 500: 'Internal Server Error'},
             params={'latitude': 'Specify the latitude associated with the point.',
                     'longitude': 'Specify the longitude associated with the point.',
                     'radius': 'Specify the radius (meters) covering the circular region of interest around the point '
                               '(coordinate) described by the latitude and longitude.'})
    @api.expect(relative_arguments, validate=True)
    def get(self, latitude, longitude, radius):
        """Returns car parks within a radius around a point described by the given latitude and longitude."""
        try:
            return osm.getParking(latitude, longitude, radius), 200
        except Exception as e:
            print(e)
            return "", 500


@ns.route('/<float:latitude>,<float:longitude>/<int:radius>/parks')
class ParkReport(Resource):
    @api.doc(responses={200: 'OK', 500: 'Internal Server Error'},
             params={'latitude': 'Specify the latitude associated with the point.',
                     'longitude': 'Specify the longitude associated with the point.',
                     'radius': 'Specify the radius (meters) covering the circular region of interest around the point '
                               '(coordinate) described by the latitude and longitude.'})
    @api.expect(relative_arguments, validate=True)
    def get(self, latitude, longitude, radius):
        """Returns parks within a radius around a point described by the given latitude and longitude."""
        try:
            return osm.getParks(latitude, longitude, radius), 200
        except Exception as e:
            print(e)
            return "", 500


@ns.route('/<float:latitude>,<float:longitude>/<int:radius>/schools')
class SchoolReport(Resource):
    @api.doc(responses={200: 'OK', 500: 'Internal Server Error'},
             params={'latitude': 'Specify the latitude associated with the point.',
                     'longitude': 'Specify the longitude associated with the point.',
                     'radius': 'Specify the radius (meters) covering the circular region of interest around the point '
                               '(coordinate) described by the latitude and longitude.'})
    @api.expect(relative_arguments, validate=True)
    def get(self, latitude, longitude, radius):
        """Returns the Schools within a radius around a point described by the given latitude and longitude."""
        try:
            return osm.getSchools(latitude, longitude, radius), 200
        except Exception as e:
            print(e)
            return "", 500


@ns.route('/<float:latitude>,<float:longitude>/<int:radius>/kindergarten')
class KindergartenReport(Resource):
    @api.doc(responses={200: 'OK', 500: 'Internal Server Error'},
             params={'latitude': 'Specify the latitude associated with the point.',
                     'longitude': 'Specify the longitude associated with the point.',
                     'radius': 'Specify the radius (meters) covering the circular region of interest around the point '
                               '(coordinate) described by the latitude and longitude.'})
    @api.expect(relative_arguments, validate=True)
    def get(self, latitude, longitude, radius):
        """Returns the Kindergartens within a radius around a point described by the given latitude and longitude."""
        try:
            return osm.getKindergarten(latitude, longitude, radius), 200
        except Exception as e:
            print(e)
            return "", 500


@ns.route('/<float:latitude>,<float:longitude>/<int:radius>/hospitals')
class HospitalReport(Resource):
    @api.doc(responses={200: 'OK', 500: 'Internal Server Error'},
             params={'latitude': 'Specify the latitude associated with the point.',
                     'longitude': 'Specify the longitude associated with the point.',
                     'radius': 'Specify the radius (meters) covering the circular region of interest around the point '
                               '(coordinate) described by the latitude and longitude.'})
    @api.expect(relative_arguments, validate=True)
    def get(self, latitude, longitude, radius):
        """Returns the Hospitals within a radius around a point described by the given latitude and longitude."""
        try:
            return osm.getHospitals(latitude, longitude, radius), 200
        except Exception as e:
            print(e)
            return "", 500


@ns.route('/<float:latitude>,<float:longitude>/<int:radius>/doctors')
class DoctorReport(Resource):
    @api.doc(responses={200: 'OK', 500: 'Internal Server Error'},
             params={'latitude': 'Specify the latitude associated with the point.',
                     'longitude': 'Specify the longitude associated with the point.',
                     'radius': 'Specify the radius (meters) covering the circular region of interest around the point '
                               '(coordinate) described by the latitude and longitude.'})
    @api.expect(relative_arguments, validate=True)
    def get(self, latitude, longitude, radius):
        """Returns the Doctors within a radius around a point described by the given latitude and longitude."""
        try:
            return osm.getDoctors(latitude, longitude, radius), 200
        except Exception as e:
            print(e)
            return "", 500


@ns.route('/<float:latitude>,<float:longitude>/<int:radius>/railway')
class RailwayStationReport(Resource):
    @api.doc(responses={200: 'OK', 500: 'Internal Server Error'},
             params={'latitude': 'Specify the latitude associated with the point.',
                     'longitude': 'Specify the longitude associated with the point.',
                     'radius': 'Specify the radius (meters) covering the circular region of interest around the point '
                               '(coordinate) described by the latitude and longitude.'})
    @api.doc(responses={200: 'OK', 500: 'Internal Server Error'},
             params={'latitude': 'Specify the latitude associated with the point.',
                     'longitude': 'Specify the longitude associated with the point.',
                     'radius': 'Specify the radius (meters) covering the circular region of interest around the point '
                               '(coordinate) described by the latitude and longitude.'})
    @api.expect(relative_arguments, validate=True)
    def get(self, latitude, longitude, radius):
        """Returns the Railway Stations within a radius around a point described by the given latitude and longitude."""
        try:
            return osm.getRailwayStations(latitude, longitude, radius), 200
        except Exception as e:
            print(e)
            return "", 500


@ns.route('/<float:latitude>,<float:longitude>/<int:radius>/tram')
class TramStationReport(Resource):
    @api.doc(responses={200: 'OK', 500: 'Internal Server Error'},
             params={'latitude': 'Specify the latitude associated with the point.',
                     'longitude': 'Specify the longitude associated with the point.',
                     'radius': 'Specify the radius (meters) covering the circular region of interest around the point '
                               '(coordinate) described by the latitude and longitude.'})
    @api.expect(relative_arguments, validate=True)
    def get(self, latitude, longitude, radius):
        """Returns the Tram Stations within a radius around a point described by the given latitude and longitude."""
        try:
            return osm.getTramStations(latitude, longitude, radius), 200
        except Exception as e:
            print(e)
            return "", 500


@ns.route('/<float:latitude>,<float:longitude>/<int:radius>/bus')
class BusStationReport(Resource):
    @api.doc(responses={200: 'OK', 500: 'Internal Server Error'},
             params={'latitude': 'Specify the latitude associated with the point.',
                     'longitude': 'Specify the longitude associated with the point.',
                     'radius': 'Specify the radius (meters) covering the circular region of interest around the point '
                               '(coordinate) described by the latitude and longitude.'})
    @api.expect(relative_arguments, validate=True)
    def get(self, latitude, longitude, radius):
        """Returns the Bus Stations within a radius around a point described by the given latitude and longitude."""
        try:
            return osm.getBusStations(latitude, longitude, radius), 200
        except Exception as e:
            print(e)
            return "", 500
