from django.conf.urls import url
from . import views, auth_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^index$', views.index, name='index'),

	#auth
	url(r'^login$', auth_views.login, name='login'),
	url(r'^authenticate$', auth_views.authenticate, name='authenticate'),
	url(r'^signup$', auth_views.signup, name='signup'),
	url(r'^signup/submit$', auth_views.signup_submit, name='signup-submit'),
	url(r'^logout$', auth_views.logout, name='logout'),

	url(r'^uploadPhoto$', views.uploadPhoto, name='uploadPhoto'),
	url(r'^deletePhoto$', views.deletePhoto, name='deletePhoto'),
	url(r'^searchPhotoQuery$', views.searchPhotoQuery, name='searchPhotoQuery'),
	url(r'^searchPhoto$', views.searchPhoto, name='searchPhoto'),
	url(r'^profile$', views.profile, name='profile'),
	url(r'^operatedir$', views.operatedir, name='operatedir'),
	url(r'^enterdir$', views.enterdir, name='enterdir'),

	url(r'^imageProcess$', views.imageProcess),
	url(r'^saveNewPhoto$', views.saveNewPhoto),
	url(r'^deleteTempImg$', views.deleteTempImg),
	url(r'^likeOrWithdrew$', views.likeOrWithdrew),
	url(r'^favor$', views.favor, name='favor'),
	url(r'^addFavor$', views.addFavor, name='addFavor'),
	url(r'^chooseLabels$', views.chooseLabels),
	url(r'^getPicLabels$',views.getPicLabels),

	url(r'^searchPhoto$', views.searchPhoto, name='searchPhoto'),
	url(r'^searchAlbum$', views.searchAlbum, name='searchAlbum'),
	url(r'^labelsmanage$', views.labelsmanage, name='labelsmanage'),

	url(r'^help$', views.help, name='help')
	
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)