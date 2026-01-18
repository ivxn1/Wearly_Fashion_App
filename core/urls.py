from django.urls import path

import core.views

app_name = 'core'

urlpatterns = [
    path('', core.views.home_view, name='home'),
    path('about/', core.views.about_view, name='about')
]