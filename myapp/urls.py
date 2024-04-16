from django.urls import path
from .views import *

urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path("search/", UserSearchAPIView.as_view(), name="search"),
    path("friend-request/", FriendRequestAPIView.as_view(), name="friend-request"),
    path("friends/", FriendListAPIView.as_view(), name="friends"),
    path(
        "pending-requests/",
        PendingFriendRequestListAPIView.as_view(),
        name="pending-requests",
    ),
    path(
        "reject-request/<int:pk>/",
        RejectFriendRequestAPIView.as_view(),
        name="reject-request",
    ),
    path(
        "accept-friend-request/<int:request_id>/",
        AcceptFriendRequestView.as_view(),
        name="accept-friend-request",
    ),
]
