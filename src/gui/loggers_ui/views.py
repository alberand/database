import os
import json

from django.views import generic
from django.shortcuts import render
from django.http import HttpResponse
from django.utils.encoding import smart_str
from django.core.files import File
from django.db.models import Max, Min

from .models import Sessions, Packages

from .utils import add_coords_to_json, NMEA_to_ll, NMEA_to_dd, lvl_to_degree
from .utils import route_template, json_route, find_coords_center, find_bounds

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

        names = self._disp_fields_names()

        values = list()
        for package in packages:
            values.append({field: getattr(package, field) for field in names})

        return values

    def _disp_fields_names(self):
        '''
        Generate list of fields names of Model. So names to display.
        Args:
            package: django.db.models.Model
        Returns:
            List with strings
        '''
        # Add to this list names which you want to display
        fields = ['date', 'time', 'latitude', 'longitude', 'gsm_sig_str',
                'net_provider', 'network_type']

        return [item.name for item in Packages._meta.get_fields() if item.name 
                in fields]

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
        # ses_info['avr_speed'] = 322
        # ses_info['avr_sat_num'] = 7

        return ses_info

    def get(self, request, ses_id):
        # Get packages
        packages = self.get_packages(ses_id)

        return render(request, self.template_name, 
                {
                    'ext_templ':        'main.html',
                    'sessions':         Sessions.objects.all(),
                    'names':            self._disp_fields_names,
                    'packages':         packages[1:100],
                    'ses_info':         self.session_info(ses_id),
                    'json_map_data':    json_route(packages[::3]),
                    'json_map_center':  find_coords_center(packages),
                    'json_map_bounds': find_bounds(packages)
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

        names = ['latitude', 'lat_pos', 'longitude', 'lon_pos']

        values = list()
        for package in packages:
            values.append({field: getattr(package, field) for field in names})

        return values

    def get(self, request, ses_id):
        # Get packages
        packages = self.get_packages(ses_id)

        response =  render(request, self.template_name, 
                {
                    'ses_id':           ses_id,
                    'json_map_data':    json_route(packages),
                    'json_map_center':  find_coords_center(packages),
                    'json_map_bounds':  find_bounds(packages)
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

        names = ['latitude', 'lat_pos', 'longitude', 'lon_pos']

        values = list()
        for package in packages:
            values.append({field: getattr(package, field) for field in names})

        return values

    def _find_zoom_level(self, bounds):
        diff_lat, diff_lon = [
                bounds[0][1] - bounds[0][0], 
                bounds[1][1] - bounds[1][0]
        ]

        zoom_level = 20
        prev_degree_range = lvl_to_degree[-1]

        for degree_range in lvl_to_degree[::-1]:
            if diff_lat > degree_range:
                continue
            else:
                print('New degree range: {}'.format(degree_range))
                prev_degree_range = degree_range

                new_zoom_level = lvl_to_degree.index(prev_degree_range)
                print('New zoom level: {}'.format(new_zoom_level))
                if new_zoom_level < zoom_level:
                    zoom_level = new_zoom_level
                break

        for degree_range in lvl_to_degree[::-1]:
            if diff_lon > degree_range:
                continue
            else:
                print('New degree range: {}'.format(degree_range))
                prev_degree_range = degree_range

                new_zoom_level = lvl_to_degree.index(prev_degree_range)
                print('New zoom level: {}'.format(new_zoom_level))
                if new_zoom_level < zoom_level:
                    zoom_level = new_zoom_level
                break

        return zoom_level


    def get(self, request):
        # Get packages
        routes = list()
        all_pkgs = list()

        for session in Sessions.objects.all():
            packages = self.get_packages(getattr(session, 'ses_id'))[::3]
            all_pkgs.extend(packages)
            routes.append(json_route(packages))

        routes = zip(routes, [getattr(session, 'ses_id') 
                for session in Sessions.objects.all()])

        print(list(routes))

        response =  render(request, self.template_name, 
                {
                    'ext_templ':        'main.html',
                    'sessions':         Sessions.objects.all(),
                    'n_routes':         len(list(routes)),
                    'routes':           list(map(list, routes)),
                    'json_map_center':  find_coords_center(all_pkgs),
                    'json_map_bounds':  find_bounds(all_pkgs)
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
    path_to_file = os.path.realpath("./loggers_ui/data/server_01/{}.txt".format(ses_id))
    _file = open(path_to_file, 'r')

    file_to_down = File(_file)
    response = HttpResponse(
            file_to_down, 
            content_type='text/plain') 
    response['Content-Disposition'] = 'inline; filename={}'.format(
            smart_str('{}.txt'.format(ses_id)))

    return response
