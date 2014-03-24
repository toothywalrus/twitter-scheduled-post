import sys

from django.views.generic import TemplateView

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response


import utils


class MainHomePage(TemplateView):

    """
    Home page for our app.
    """
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(MainHomePage, self).get_context_data(**kwargs)

        forms_list = utils.get_info_forms()
        forms = list((".".join([utils.get_form_id(form), "html"]), form())
                     for form in forms_list)
        partials = utils.get_partials()
        context.update({'forms': forms, 'partials': partials})
        return context


for name in utils.get_info_names():
    gen_class = type(utils.get_viewset_name(name), (
        viewsets.ModelViewSet, ), {'model': utils.get_model_class(name)})
    setattr(sys.modules[__name__], gen_class.__name__, gen_class)


class InfoView(APIView):

    """
    View for getting a bulk of models information at once.
    """

    def get(self, request, format=None):

        info = {utils.get_resource_name(name):
                utils.get_serializer_class(name)
                (utils.get_model_class(name).objects.all(),
                    many=True).data
                for name in utils.get_info_names()}

        return Response(info)
