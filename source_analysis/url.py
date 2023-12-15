from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("summary", views.summary_fun, name="summary"),
    path("source", views.source, name="source"),
    path("results", views.result, name="results"),
    # path('export-pdf/', views.export, name='export_to_pdf')
]
# urlpatterns=[
#     path('',views.donut,name="graph")
# ]
