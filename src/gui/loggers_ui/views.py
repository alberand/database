import os
import json

from django.views import generic
from django.shortcuts import render
from django.http import HttpResponse
from django.utils.encoding import smart_str
from django.core.files import File
from django.db.models import Max, Min

from .models import Sessions, Packages

from .utils import add_coords_to_json, NMEA_to_ll

class MainPage(generic.TemplateView):
    '''
    Main page view.
    '''
    template_name = 'main.html'

    def get(self, request):
        response =  render(request, self.template_name, 
                {
                    'sessions': Sessions.objects.all()
                }
        )

        return response

class SessionPage(generic.TemplateView):
    '''
    Page with packages for choosen session.
    '''
    template_name = 'session.html'

    def get_packages(self, ses_id):
        '''
        Generate list with lists contain packages data.
        Args:
            ses_id: session id
        Returns:
            List with lists representing pacakges.
        '''
        packages = Packages.objects.filter(ses_id=ses_id)

        names_list = self._disp_fields_names()

        pkgs_list = list()
        for package in packages:
            pkgs_list.append([getattr(package, field) for field in names_list])

        return (names_list, pkgs_list)

    def _disp_fields_names(self):
        '''
        Generate list of fields names of Model. So names to display.
        Args:
            package: django.db.models.Model
        Returns:
            List with strings
        '''
        # Add to this list names which you don't want to display
        except_fields = [
                'id', 'ses', 't_ms', 'ses_id', 'course',
                'gps_altitude', 'speed', 'temperature', 'pressure', 'gps_state',
                'sat_num', 'module_id'
        ]
        return [item.name for item in Packages._meta.get_fields() if item.name 
                not in except_fields]

    def json_route(self, pkg_list):
        '''
        Generate GEOjson structure for displaying on map.
        Args:
            pkg_list: list of packages with coordinates.
        Returns:
            String which represents json structure.
        '''
        with open('./loggers_ui/template.json', 'r') as _file:
            data_set = json.loads(_file.read())

            for pkg in pkg_list:
                data_set = add_coords_to_json(data_set, 
                        NMEA_to_ll(float(pkg[2]), 
                                   float(pkg[4])))

        replace_table = {ord('\''): '"', ord('"'): '\''}

        return str(data_set).replace('\'', '"')

    def _find_coords_center(self, pkg_list):
        # Latitude id in the list.
        i = 2
        max_lat = max([pkg[i] for pkg in pkg_list])
        min_lat = min([pkg[i] for pkg in pkg_list])
        # Longitude id in the list.
        i = 4
        max_lon = max([pkg[i] for pkg in pkg_list])
        min_lon = min([pkg[i] for pkg in pkg_list])

        return json.dumps(NMEA_to_ll(min_lat + (max_lat - min_lat)/2,
                                     min_lon + (max_lon - min_lon)/2))


    def session_info(self, ses_id):
        '''
        Generate sessions information displayed on the page.
        Args:
            ses_id: integer, session id
        Returns:
            Dictionary.
        '''
        ses_info = dict()

        # Calculate date range
        earliest_d = Packages.objects.all().aggregate(Min('date'))['date__min']
        latest_d = Packages.objects.all().aggregate(Max('date'))['date__max']

        # Calculate time range
        earliest_t = Packages.objects.all().aggregate(Min('time'))['time__min']
        latest_t = Packages.objects.all().aggregate(Max('time'))['time__max']

        ses_info['ses_id'] = ses_id
        ses_info['date_range'] = ('{} - {}'.format(earliest_d, latest_d) if
                latest_d != earliest_d else '{}'.format(latest_d))
        ses_info['time_range'] = ('{} - {}'.format(earliest_t, latest_t) if
                latest_t != earliest_t else '{}'.format(latest_t))
        # TODO: empty for now
        ses_info['avr_speed'] = 322
        ses_info['avr_sat_num'] = 7

        return ses_info

    def get(self, request, ses_id):
        # Get packages
        names_list, packages = self.get_packages(ses_id)

        return render(request, self.template_name, 
                {
                    'ext_templ':        'main.html',
                    'sessions':         Sessions.objects.all(),
                    'names':            names_list,
                    'packages':         packages,
                    'ses_info':         self.session_info(ses_id),
                    'json_map_data':    self.json_route(packages),
                    'json_map_center':  self._find_coords_center(packages)
                }
        )


class MapPage(generic.TemplateView):
    '''
    Page with map only.
    '''
    template_name = 'map.html'

    def get_packages(self, ses_id):
        '''
        Generate list with lists contain packages data.
        Args:
            ses_id: session id
        Returns:
            List with lists representing pacakges.
        '''
        packages = Packages.objects.filter(ses_id=ses_id)

        names_list = ['latitude', 'lat_pos', 'longitude', 'lon_pos']

        pkgs_list = list()
        for package in packages:
            pkgs_list.append([getattr(package, field) for field in names_list])

        return (names_list, pkgs_list)

    def json_route(self, pkg_list):
        '''
        Generate GEOjson structure for displaying on map.
        Args:
            pkg_list: list of packages with coordinates.
        Returns:
            String which represents json structure.
        '''
        with open('./loggers_ui/template.json', 'r') as _file:
            data_set = json.loads(_file.read())

            for pkg in pkg_list:
                data_set = add_coords_to_json(data_set, 
                        NMEA_to_ll(float(pkg[0]), 
                                   float(pkg[2])))

        replace_table = {ord('\''): '"', ord('"'): '\''}

        return str(data_set).replace('\'', '"')

    def _find_coords_center(self, pkg_list):
        # Latitude id in the list.
        i = 0
        max_lat = max([pkg[i] for pkg in pkg_list])
        min_lat = min([pkg[i] for pkg in pkg_list])
        # Longitude id in the list.
        i = 2
        max_lon = max([pkg[i] for pkg in pkg_list])
        min_lon = min([pkg[i] for pkg in pkg_list])

        return json.dumps(NMEA_to_ll(min_lat + (max_lat - min_lat)/2,
                                     min_lon + (max_lon - min_lon)/2))

    def get(self, request, ses_id):
        # Get packages
        names_list, packages = self.get_packages(ses_id)

        response =  render(request, self.template_name, 
                {
                    'ses_id':           ses_id,
                    'json_map_data':    self.json_route(packages),
                    'json_map_center':  self._find_coords_center(packages)
                }
        )

        return response

class GlobalMap(generic.TemplateView):
    '''
    '''
    template_name = 'maps.html'

    def get_packages(self, ses_id):
        '''
        Generate list with lists contain packages data.
        Args:
            ses_id: session id
        Returns:
            List with lists representing pacakges.
        '''
        packages = Packages.objects.filter(ses_id=ses_id)

        names_list = ['latitude', 'lat_pos', 'longitude', 'lon_pos']

        pkgs_list = list()
        for package in packages:
            pkgs_list.append([getattr(package, field) for field in names_list])

        return (names_list, pkgs_list)

    def json_route(self, pkg_list):
        '''
        Generate GEOjson structure for displaying on map.
        Args:
            pkg_list: list of packages with coordinates.
        Returns:
            String which represents json structure.
        '''
        with open('./loggers_ui/template.json', 'r') as _file:
            data_set = json.loads(_file.read())

            for pkg in pkg_list:
                data_set = add_coords_to_json(data_set, 
                        NMEA_to_ll(float(pkg[0]), 
                                   float(pkg[2])))

        replace_table = {ord('\''): '"', ord('"'): '\''}

        return str(data_set).replace('\'', '"')

    def _find_coords_center(self, pkg_list):
        # Latitude id in the list.
        i = 0
        max_lat = max([pkg[i] for pkg in pkg_list])
        min_lat = min([pkg[i] for pkg in pkg_list])
        # Longitude id in the list.
        i = 2
        max_lon = max([pkg[i] for pkg in pkg_list])
        min_lon = min([pkg[i] for pkg in pkg_list])

        return json.dumps(NMEA_to_ll(min_lat + (max_lat - min_lat)/2,
                                     min_lon + (max_lon - min_lon)/2))

    def get(self, request):
        # Get packages
        routes = list()
        all_pkgs = list()
        for session in Sessions.objects.all():
            names_list, packages = self.get_packages(getattr(session, 'ses_id'))
            all_pkgs.extend(packages)
            routes.append(self.json_route(packages))
            print(all_pkgs)

        response =  render(request, self.template_name, 
                {
                    'ext_templ':        'main.html',
                    'sessions':         Sessions.objects.all(),
                    'routes':           routes,
                    'json_map_center': self._find_coords_center(all_pkgs)
                }
        )

        return response

def download_file(request, ses_id):
    '''
    Function which called when you want to download session file.
    Args:
        request:
        ses_id: integer, session id.
    Returns:
        HttpResponse response objects for browser.
    '''
    path_to_file = os.path.realpath("./loggers_ui/data/{}.txt".format(ses_id))
    _file = open(path_to_file, 'r')

    file_to_down = File(_file)
    response = HttpResponse(
            file_to_down, 
            content_type='application/force-download') 
    response['Content-Disposition'] = 'attachment; filename={}'.format(
            smart_str('{}.txt'.format(ses_id)))

    return response
