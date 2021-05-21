from django.urls import path
from .views import (
      SCM_update, 
      SCMListView, SCMDetailView, SCMCreateView,
      SCMUpdateView, SCMDeleteView, AssignAgentView, CategoryListView,CategoryDetailView, SCMCategoryUpdateView
      )

app_name = "SCM"

urlpatterns = [
     path('', SCMListView.as_view(), name='SCM-list'),
     path('<int:pk>/', SCMDetailView.as_view(), name='SCM-detail'),
     path('<int:pk>/update/',SCM_update, name='SCM-update'),
     path('<int:pk>/delete/',SCMDeleteView.as_view(), name='SCM-delete'),
     path('<int:pk>/assign-agent/',AssignAgentView.as_view(), name='assign-agent'),
     path('<int:pk>/category/',SCMCategoryUpdateView.as_view(), name='SCM_category_update'),
     path('create/',SCMCreateView.as_view(), name='SCM-create'),
     path('categories/',CategoryListView.as_view(), name='category-list'),
     path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
]
