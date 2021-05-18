from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from SCM.views import landing_page, LandingPageView


admin.autodiscover()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LandingPageView.as_view(), name='landing-page'),
    path('SCM/', include('SCM.urls', namespace="SCM")),   
    
]
static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# if settings.DEBUG:
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
