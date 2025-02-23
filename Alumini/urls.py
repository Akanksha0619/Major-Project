from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from Alumini.views import *

urlpatterns = [
    path('',login_page,name="login"),
    path('registration-page',Registraion_page,name="registraion"),
    path('alumini-page',alumini_page,name='alumini'),
    path('logout-page',logout_page,name="logout"),
    path('alumini-profile',alumini_profile,name='alumni-profile'),
    path('alumini-profile-show/<int:user_id>/',alumini_profile_show,name="alumini-profile-show"),
    path('edit-profile',edit_alumni_profile,name="edit-profile"),
    path('delete-profile/<int:user_id>/',delete_profile,name="delete=profile"),
    path('alumini-post',post,name="alumini-post"),
    path('like/<int:post_id>/',like_post, name='like_post'),
    path('alumini-list',alumini_list,name="alumini_list"),

    path("connection-requests/", connection_requests_view, name="connection_requests"),
    path("accept-connection/<int:request_id>/", accept_connection, name="accept_connection"),
    path("get-connection-request-count/", get_connection_request_count, name="get_request_count"),

    # for mesage
    path('send_request/<int:receiver_id>/', send_connection_request, name='send_request'),
    path('accept_request/<int:request_id>/', accept_connection, name='accept_request'),

     #comment
    path('get-comments/<int:post_id>/', get_comments, name='get-comments'),
    path('add-comment/', add_comment, name='add-comment'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)