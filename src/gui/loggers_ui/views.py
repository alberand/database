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

class MainPageView(generic.TemplateView):
    '''
    Main page view.
    '''
    template_name = 'main.html'

    def get(self, request):
        return render(request, self.template_name, 
                        {'sessions': Sessions.objects.all()})

class PackagesList(generic.TemplateView):
    '''
    Page with packages for choosen session.
    '''
    template_name = 'd_pkgs_list.html'

    def generate_pkg_set(self, ses_id):
        '''
        Generate list with lists contain packages data.
        Args:
            ses_id: session id
        Returns:
            List with lists representing pacakges.
        '''
        packages = Packages.objects.filter(ses_id=ses_id)

        names_list = self.generate_fld_names()

        pkgs_list = list()
        for package in packages:
            pkgs_list.append([getattr(package, field) for field in names_list])

        return (names_list, pkgs_list)

    def generate_fld_names(self):
        '''
        Generate list of fields names of Model. So names to display.
        Args:
            package: django.db.models.Model
        Returns:
            List with strings
        '''
        except_fields = ['id', 'ses', 't_ms', 'ses_id', 'course',
                'gps_altitude', 'speed', 'temperature', 'pressure', 'gps_state',
                'sat_num', 'module_id']
        return [item.name for item in Packages._meta.get_fields() if item.name 
                not in except_fields]

    def generate_route_for_map(self, pkg_list):
        '''
        Generate GEOjson structure for displaying on map.
        Args:
            pkg_list: list of packages with coordinates.
        '''
        with open('./loggers_ui/template.json', 'r') as _file:
            data_set = json.loads(_file.read())

            for pkg in pkg_list:
                data_set = add_coords_to_json(data_set, 
                        NMEA_to_ll(float(pkg[2]), 
                                   float(pkg[4])))

        replace_table = {ord('\''): '"', ord('"'): '\''}

        # return str(data_set).translate(replace_table)
        return str(data_set).replace('\'', '"')

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
        names_list, packages = self.generate_pkg_set(ses_id)

        route_json = self.generate_route_for_map(packages)

        ses_info = self.session_info(ses_id)

        return render(request, self.template_name, 
                {
                    'ext_templ': 'main.html',
                    'sessions': Sessions.objects.all(),
                    'names': names_list,
                    'packages': packages,
                    'json_map_data': route_json,
                    'ses_info': ses_info
                }
        )



def downloadfile(request, ses_id):
    path_to_file = os.path.realpath("./loggers_ui/data/{}.txt".format(ses_id))
    f = open(path_to_file, 'r')
    myfile = File(f)
    response = HttpResponse(myfile, content_type='application/force-download') 
    response['Content-Disposition'] = 'attachment; filename={}'.format(smart_str('{}.txt'.format(ses_id)))
    # response['X-Sendfile'] = smart_str('./templates/main.html'.format(ses_id))
    # print(response['X-Sendfile'])

    return response
