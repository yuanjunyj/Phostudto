from django.conf.urls import url
from . import views, auth_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
	url(r'^$', views.display, name='display'),
	url(r'^display$', views.display, name='display'),
	#auth
	url(r'^login$', auth_views.login, name='login'),
	url(r'^authenticate$', auth_views.authenticate, name='authenticate'),
	url(r'^signup$', auth_views.signup, name='signup'),
	url(r'^signup/submit$', auth_views.signup_submit, name='signup-submit'),
	url(r'^logout$', auth_views.logout, name='logout'),

	url(r'^uploadPhoto$', views.uploadPhoto, name='uploadPhoto'),
	url(r'^deletePhoto$', views.deletePhoto, name='deletePhoto'),
	url(r'^filterPhoto$', views.filterPhoto, name='filterPhoto'),
	url(r'^searchPhoto$', views.SearchPhoto, name='searchPhoto'),
	url(r'^profile$', views.profile, name='profile'),
	url(r'^makedir$', views.makedir, name='makedir'),

	url(r'^imageProcess$', views.imageProcess),
	url(r'^saveNewPhoto$', views.saveNewPhoto),
	url(r'^deleteTempImg$', views.deleteTempImg),
	url(r'^likeOrWithdrew$', views.likeOrWithdrew),
	url(r'^chooseLabels$', views.chooseLabels),
	url(r'^getPicLabels$',views.getPicLabels),
	#url(r'^searchImage$', views.SearchImage, name='searchImage'),

	url(r'^register$',views.register),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)