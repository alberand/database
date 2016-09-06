import os
import json

from django.views import generic
from django.shortcuts import render
from django.http import HttpResponse
from django.utils.encoding import smart_str
from django.core.files import File

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

    def get(self, request, ses_id):
        names_list, packages = self.generate_pkg_set(ses_id)

        route_json = self.generate_route_for_map(packages)

        return render(request, self.template_name, 
                {
                    'ext_templ': 'main.html',
                    'sessions': Sessions.objects.all(),
                    'names': names_list,
                    'packages': packages,
                    'json_map_data': route_json
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
