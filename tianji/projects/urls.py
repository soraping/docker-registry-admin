from django.urls import path
from tianji.projects import views

urlpatterns = [
    path('', views.ProjectView.as_view(), name='project_list'),
    path('list', views.ProjectListView.as_view()),
    path('add', views.ProjectAddView.as_view()),
    path('upd', views.ProjectUpdateView.as_view()),
    path('detail', views.ProjectDetailView.as_view()),

    path('host', views.ProjectHostView.as_view(), name="project_host_list"),
    path('host-list', views.ProjectHostListView.as_view()),
    path('host-add', views.ProjectHostAddView.as_view()),
    path('host-upd', views.ProjectHostUpdView.as_view())
]