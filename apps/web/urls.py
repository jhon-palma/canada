
from django.contrib.auth.decorators import login_required
from django.urls import path, include, re_path

from apps.web.views import web, web_messages

urlpatterns = [
    path('', web.WebIndex.as_view()),
    re_path(r'^(?P<language>fr|en)/$', web.WebIndex.as_view(), name='index'),
    re_path(r'^(?P<language>fr|en)/(?P<option>properties|properties-for-sale|properties-for-rent|proprietes|proprietes-a-vendre|proprietes-a-louer)/$', web.WebProperties.as_view(), name='properties'),
    re_path(r'^(?P<language>fr|en)/(?P<option>propertie|propriete)/(?P<propertie_id>[-\w]+)/(?P<flag>detail|pdf)/$', web.WebDetailProperty.as_view(), name='detail-propertie'),
    re_path(r'^(?P<language>fr|en)/(?P<option>propertie|propriete)/$', web.WebPropertyRedirect.as_view(), name='propertie-redirect'),
    re_path(r'^(?P<language>fr|en)/media/$', web.WebVideos.as_view(), name='videos'),
    re_path(r'^(?P<language>fr|en)/(?P<option>contact-realestate-broker|contact-courtier-immobilier)/$', web.WebContact.as_view(), name='contact'),
    re_path(r'^(?P<language>fr|en)/(?P<option>privacy-policy|politique-confidentialite)/$', web.WebPolicy.as_view(), name='privacy-policy'),
    re_path(r'^(?P<language>fr|en)/(?P<option>real-estate-broker|courtier-immobilier)/$', web.WebTeam.as_view(), name='team'),
    re_path(r'^(?P<language>fr|en)/(?P<option>courtier)/(?P<member_id>[0-9a-f-]+)/$', web.WebMemberDetail.as_view(), name='member'),
    re_path(r'^(?P<language>fr|en)/(?P<option>buying|selling|acheter|vendre)/$', web.WebWork.as_view(), name='work'),
    path('calc_monthly_payment/', web.calc_monthly_payment_view, name='calc_monthly_payment'),
    path('searchpropriete/', web.searchpropriete, name='searchpropriete'),
    path('searchMember/', web.searchMember, name='searchMember'),
    path("search-videos/", web.search_videos, name="search_videos"),
    re_path(r'^(?P<language>fr|en)/search/', web.SearchView.as_view(), name='search'),
    path('contact_messages/', web_messages.contact_messages, name='contact_messages'),
    path('statistics/', web.statistics, name='statistics'),
    re_path(r'^search/(?P<language>fr|en)/(?P<option>[\w-]+)/$', web.SearchProperties.as_view(), name='search_properties'),
    path('calculator/', web.WebCalculator.as_view(), name='calculator'),
    path('metadata/',login_required(web.metadata), name='list-metadata'),
    re_path('metadata/update/(?P<pk>[\w-]+)/$', login_required(web.update_metadata), name='update-metadata'),
]

