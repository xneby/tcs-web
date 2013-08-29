from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout, password_change, password_change_done

urlpatterns = patterns('tcs.views',

	url(r'^$','main', name='main'),
	url(r'^login/$', login, name='login'),
	url(r'^logout/$', logout, name='logout'),

	url(r'^passwd/$', password_change, name='passwd'),
	url(r'^passwd/done/$', password_change_done, name='passwd-done'),

	url(r'competitions/$', 'competitions_list', name = 'competitions-list'),
	url(r'competitions/(?P<slug>[A-Za-z0-9-]+)/$', 'competition_details', name = 'competition-details'),
	url(r'competitions/(?P<slug>[A-Za-z0-9-]+)/news/$', 'competition_news', name = 'competition-news'),
	url(r'competitions/(?P<slug>[A-Za-z0-9-]+)/news/add/$', 'competition_news_add', name = 'competition-news-add'),
	url(r'competitions/(?P<slug>[A-Za-z0-9-]+)/news/(?P<pk>\d+)/modify/$', 'competition_news_modify', name = 'competition-news-modify'),
	url(r'competitions/(?P<slug>[A-Za-z0-9-]+)/news/(?P<pk>\d+)/delete/$', 'competition_news_delete', name = 'competition-news-delete'),

	url(r'comments/create/(?P<pk>\d+)/$', 'comment_add', name = 'comment-add'),
	url(r'comments/modify/(?P<pk>\d+)/$', 'comment_modify', name = 'comment-modify'),
	url(r'comments/delete/(?P<pk>\d+)/$', 'comment_delete', name = 'comment-delete'),

	url(r'alert/(?P<pk>\d+)/$', 'comment_alert', name='alert'),
	url(r'vote/(?P<pk>\d+)/$', 'vote', name='vote'),

	url(r'competitions/(?P<slug>[A-Za-z0-9-]+)/problems/$', 'problem_list', name = 'competition-problems'),
	url(r'competitions/(?P<slug>[A-Za-z0-9-]+)/problems/create/$', 'problem_add', name = 'problem-add'),
	url(r'problems/(?P<slug>[A-Za-z0-9-]+)/$', 'problem_details', name = 'problem-details'),
	url(r'problems/(?P<slug>[A-Za-z0-9-]+)/modify/$', 'problem_modify', name = 'problem-modify'),
	
	url(r'problems/(?P<slug>[A-Za-z0-9-]+)/solutions/$', 'solution_list', name = 'solution-list'),
	url(r'problems/(?P<slug>[A-Za-z0-9-]+)/solutions/create/$', 'solution_add', name = 'solution-add'),
	url(r'problems/(?P<slug>[A-Za-z0-9-]+)/solutions/(?P<pk>\d+)/modify/$', 'solution_modify', name = 'solution-modify'),
	url(r'problems/(?P<slug>[A-Za-z0-9-]+)/solutions/(?P<pk>\d+)/delete/$', 'solution_delete', name = 'solution-delete'),
	url(r'problems/(?P<slug>[A-Za-z0-9-]+)/solutions/(?P<pk>\d+)/accept/(?P<value>[a-z]{3})/$', 'solution_accept', name = 'solution-accept'),
    # Examples:
    # url(r'^$', 'tcsweb.views.home', name='home'),
    # url(r'^tcsweb/', include('tcsweb.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
