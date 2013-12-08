from django.conf.urls import patterns, url
from django.views.generic import ListView, DetailView

from pleniere.models import Deputy

urlpatterns = patterns('',
  url(r'^$', ListView.as_view(model=Deputy,
      template_name='deputy/index.html',
      context_object_name='deputies'),
      name='deputy-list'),
  url(r'^(?P<pk>\w+)/$', DetailView.as_view(model=Deputy,
      template_name='deputy/deputy.html'),
      name='deputy'),
)
