from . import views
from django.urls import path, include, re_path

urlpatterns = [
    path('', views.WebIndex.as_view()),
    re_path(r'^(?P<language>fr|en)/$', views.WebIndex.as_view(), name='index'),
    re_path(r'^(?P<language>fr|en)/(?P<option>properties|properties-for-sale|properties-for-rent|proprietes|proprietes-a-vendre|proprietes-a-louer)/$', views.WebProperties.as_view(), name='properties'),
    # re_path(r'^(?P<language>fr|en)/(?P<option>properties|proprietes)/(?P<slug>[-\w]+)/$', views.WebDetailProperty.as_view(), name='detail-propertie'),
    re_path(r'^(?P<language>fr|en)/(?P<option>propertie|propriete)/(?P<propertie_id>[-\w]+)/$', views.WebDetailProperty.as_view(), name='detail-propertie'),
    re_path(r'^(?P<language>fr|en)/media/$', views.WebVideos.as_view(), name='videos'),
    re_path(r'^(?P<language>fr|en)/(?P<option>contact-realestate-broker|contact-courtier-immobilier)/$', views.WebContact.as_view(), name='contact'),
    re_path(r'^(?P<language>fr|en)/(?P<option>privacy-policy|politique-confidentialite)/$', views.WebPolicy.as_view(), name='privacy-policy'),
    re_path(r'^(?P<language>fr|en)/(?P<option>real-estate-broker|courtier-immobilier)/$', views.WebTeam.as_view(), name='team'),
    re_path(r'^(?P<language>fr|en)/(?P<option>courtier)/(?P<member_id>[0-9a-f-]+)/$', views.WebMemberDetail.as_view(), name='member'),
    re_path(r'^(?P<language>fr|en)/(?P<option>work-with-us|travailler-avec-nous)/$', views.WebWork.as_view(), name='work'),
    path('calc_monthly_payment/', views.calc_monthly_payment_view, name='calc_monthly_payment'),
    path('searchpropriete/', views.searchpropriete, name='searchpropriete'),
    path('searchMember/', views.searchMember, name='searchMember'),
    # path('search/', views.SearchView.as_view(), name='search'),
    re_path(r'^(?P<language>fr|en)/search/', views.SearchView.as_view(), name='search'),
    path('contact_messages/', views.contact_messages, name='contact_messages'),
    
]