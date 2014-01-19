try:
    from django.conf.urls import *
except ImportError:  # django < 1.4
    from django.conf.urls.defaults import *

from django.views.generic import ListView

from videos_tools.models import Video

urlpatterns = patterns('',
  url(r'^$', ListView.as_view(model=Video,
      template_name='videos_tools/listing.html',
      context_object_name='videos'), name='videos-list'),
)
