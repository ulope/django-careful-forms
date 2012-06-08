try:
    from django.conf.urls import patterns, url
except ImportError:
    # django 1.3 compatibility
    from django.conf.urls.defaults import patterns, url
from careful_forms.tests.views import normal_form, careful_incorrect_model_form, careful_correct_model_form

urlpatterns = patterns('',
    url(r'^form/normal/$', normal_form),
    url(r'^form/careful_incorrect/$', careful_incorrect_model_form),
    url(r'^form/careful_correct/$', careful_correct_model_form),
)
