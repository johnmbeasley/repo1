from django.conf.urls import patterns, include, url
from django.contrib import admin
from flip import views


admin.autodiscover()


urlpatterns = patterns('',

    url(r'^study/new/$', views.StudyMetadataEditView.as_view(),
        name='study_metadata_edit'),

    url(r'^admin/', include(admin.site.urls)),
)