from . import views
from django.urls import path, include, re_path
from .views import *

urlpatterns = [
    path('', views.WebIndex.as_view()),
    re_path(r'^(?P<language>fr|en)/$', views.WebIndex.as_view(), name='index'),
    re_path(r'^(?P<language>fr|en)/(?P<option>properties|properties-for-sale|properties-for-rent|proprietes|proprietes-a-vendre|proprietes-a-louer)/$', views.WebProperties.as_view(), name='properties'),
    re_path(r'^(?P<language>fr|en)/(?P<option>propertie|propriete)/(?P<propertie_id>[-\w]+)/(?P<flag>detail|pdf)/$', views.WebDetailProperty.as_view(), name='detail-propertie'),
    re_path(r'^(?P<language>fr|en)/(?P<option>propertie|propriete)/$', views.WebPropertyRedirect.as_view(), name='propertie-redirect'),
    re_path(r'^(?P<language>fr|en)/media/$', views.WebVideos.as_view(), name='videos'),
    re_path(r'^(?P<language>fr|en)/(?P<option>contact-realestate-broker|contact-courtier-immobilier)/$', views.WebContact.as_view(), name='contact'),
    re_path(r'^(?P<language>fr|en)/(?P<option>privacy-policy|politique-confidentialite)/$', views.WebPolicy.as_view(), name='privacy-policy'),
    re_path(r'^(?P<language>fr|en)/(?P<option>real-estate-broker|courtier-immobilier)/$', views.WebTeam.as_view(), name='team'),
    re_path(r'^(?P<language>fr|en)/(?P<option>courtier)/(?P<member_id>[0-9a-f-]+)/$', views.WebMemberDetail.as_view(), name='member'),
    re_path(r'^(?P<language>fr|en)/(?P<option>buying|selling|acheter|vendre)/$', views.WebWork.as_view(), name='work'),
    path('calc_monthly_payment/', views.calc_monthly_payment_view, name='calc_monthly_payment'),
    path('searchpropriete/', views.searchpropriete, name='searchpropriete'),
    path('searchMember/', views.searchMember, name='searchMember'),
    path("search-videos/", search_videos, name="search_videos"),
    re_path(r'^(?P<language>fr|en)/search/', views.SearchView.as_view(), name='search'),
    path('contact_messages/', views.contact_messages, name='contact_messages'),
    path('statistics/', views.statistics, name='statistics'),
    re_path(r'^search/(?P<language>fr|en)/(?P<option>[\w-]+)/$', views.SearchProperties.as_view(), name='search_properties'),
    path('calculator/', WebCalculator.as_view(), name='calculator'),
    path('metadata/',login_required(metadata), name='list-metadata'),
    re_path('metadata/update/(?P<pk>[\w-]+)/$', login_required(update_metadata), name='update-metadata'),
]

