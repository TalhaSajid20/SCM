from django.urls import path
from .views import (
      SCM_list, SCM_detail, SCM_create, SCM_update, SCM_delete, SCMListView, SCMDetailView, SCMCreateView,
      SCMUpdateView, SCMDeleteView
      )

app_name = "SCM"

urlpatterns = [
     path('', SCMListView.as_view(), name='SCM-list'),
     path('<int:pk>/',SCMDetailView.as_view(), name='SCM-detail' ),
     path('<int:pk>/update/',SCM_update, name='SCM-update'),
     path('<int:pk>/delete/',SCMDeleteView.as_view(), name='SCM-delete'),
     path('create/',SCMCreateView.as_view(), name='SCM-create')
]