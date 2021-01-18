from django.conf.urls import url
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

from .views.ProteinView import ProteinView
from .views.ProteinListView import ProteinListView
from .views.ResultView import ResultView
from .views.SessionView import SessionView
from .views.SessionsView import SessionsView
from .views.ProfileListView import ProfileListView
from .views.ProfileView import ProfileView

urlpatterns = [
    path('proteins/', ProteinListView.as_view()),
    path('proteins/<int:pk>/', ProteinView.as_view()),
    path('result/<int:pk1>/<int:pk2>/', ResultView.as_view()),
    path('sessions/', SessionsView.as_view()),
    path('sessions/<slug:username>/', SessionView.as_view()),
    path('users/', ProfileListView.as_view()),
    path('users/<slug:username>/', ProfileView.as_view()),
]
