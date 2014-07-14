from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import  static
from django.conf import settings
from registration.backends.default.views import RegistrationView
from mysite.forms import CustomRegForm, CustomAuthForm
from django.contrib.auth import views as auth_view
from blog import views

# Uncomment the next two lines to enable the admin:
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^mysite/', include('mysite.foo.urls')),
    url(r'^$', views.main_view, name='mainpage'),
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^blog/', include('blog.urls',  namespace="blog")),
    url(r'^auth/login/$',auth_view.login,
                           {'template_name': 'registration/login.html','authentication_form' : CustomAuthForm},
                           name='auth_login'),
    url(r'^auth/',include('registration.auth_urls', namespace="authorisation")),

    url(r'^register/$', RegistrationView.as_view(form_class= CustomRegForm), name = 'register'),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^profile/', include('profile.urls', namespace="profile")),

)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns +=staticfiles_urlpatterns()
