from django.views import generic
from django.shortcuts import render
from django.http import HttpResponse

from .models import Sessions, Packages

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
        Generate list of fields names of Model.
        Args:
            package: django.db.models.Model
        Returns:
            List with strings
        '''
        except_fields = ['id', 't_ms', 'ses_id', 'latitude', 'lat_pos', 
                'longitude', 'lon_pos']
        return [item.name for item in Packages._meta.get_fields() if item.name 
                not in except_fields]

    def get(self, request, ses_id):
        names_list, packages = self.generate_pkg_set(ses_id)

        return render(request, self.template_name, 
                {
                    'ext_templ': 'main.html',
                    'sessions': Sessions.objects.all(),
                    'names': names_list,
                    'packages': packages
                }
        )

