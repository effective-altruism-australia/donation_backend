from __future__ import absolute_import

from django.core import serializers
from django.http.response import JsonResponse, HttpResponse
from django.views.generic import View

from donation.models import PartnerCharity


class PartnerCharityView(View):
    def get(self, request):
        charity_names = PartnerCharity.objects.filter(active=True).order_by('order').values('slug_id', 'name')
        return HttpResponse(charity_names)
