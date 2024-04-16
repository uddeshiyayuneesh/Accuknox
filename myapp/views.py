from django.contrib.auth import authenticate, login
from rest_framework import status, views
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Friendship
from .serializers import *
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.throttling import UserRateThrottle
from rest_framework import filters
from myapp.services import FriendRequestService
import logging

logger = logging.getLogger(__name__)


# Define a class for handling sign-up requests
class SignupView(views.APIView):
    """
    Specify that this view does not require authentication (permission class AllowAny)
    """

    permission_classes = [permissions.AllowAny]

    # Define a method to handle POST requests
    def post(self, request):
        # Initialize a serializer object with the data from the request
        serializer = UserCreateSerializer(data=request.data)

        # Check if the data provided is valid according to the serializer's validation rules
        if serializer.is_valid():
            # If the data is valid, save the user and return a success response
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            # If the data is not valid, return an error response with details about the validation errors
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Define a class for handling login requests
class LoginView(views.APIView):
    """
    Specify that this view does not require authentication (permission class AllowAny)
    """

    permission_classes = [permissions.AllowAny]

    # Define a method to handle POST requests
    def post(self, request):
        # Initialize a serializer object with the data from the request
        serializer = UserLoginSerializer(data=request.data)

        # Check if the data provided is valid according to the serializer's validation rules
        if serializer.is_valid():
            # Extract email and password from the validated data
            email = serializer.validated_data["email"].lower()
            password = serializer.validated_data["password"]

            # Authenticate the user using the provided email and password
            user = authenticate(request, username=email, password=password)

            # If authentication is successful, log in the user and return a success response
            if user:
                login(request, user)
                return Response("successfully-login", status=status.HTTP_200_OK)

            # If authentication fails, return an error response indicating invalid credentials
            return Response(
                {"message": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST
            )

        # If the data provided is not valid, return an error response with details about the validation errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Define a class for handling user search requests
class UserSearchAPIView(generics.ListAPIView):
    """
    Specify the queryset to retrieve all User objects
    """

    queryset = User.objects.all()

    # Specify the serializer class to use for serializing/deserializing User objects
    serializer_class = UserCreateSerializer

    # Specify the filter backend to use for filtering the queryset
    filter_backends = [filters.SearchFilter]

    # Define the fields to search for using the specified search filter
    search_fields = ["=email", "name__icontains"]


# Define a custom throttle class for friend requests
class FriendRequestThrottle(UserRateThrottle):
    """
    Specify the scope for the throttle, which is 'friend_request'
    """

    scope = "friend_request"


# Define a class for handling friend request API requests
class FriendRequestAPIView(APIView):
    """
    Specify the throttle classes to be applied to this view, using the custom throttle class defined above
    """

    throttle_classes = [FriendRequestThrottle]

    # Define a method to handle POST requests for sending friend requests
    def post(self, request):
        # Extract the 'to_user' ID from the request data
        to_user_id = request.data.get("to_user")
        if not to_user_id:
            # If 'to_user' ID is not provided, log the error and return a bad request response
            logger.error("Friend request failed: 'to_user' not provided")
            return Response(
                {"error": "to_user is required."}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Try to retrieve the user object with the specified 'to_user' ID
            to_user = User.objects.get(pk=to_user_id)
        except User.DoesNotExist:
            # If the user does not exist, log the error and return a bad request response
            logger.error(f"Friend request failed: Invalid 'to_user' ID {to_user_id}")
            return Response(
                {"error": "Invalid to_user id."}, status=status.HTTP_400_BAD_REQUEST
            )

        # Send the friend request using a service method, passing the requesting user and the target user
        response_data, response_status = FriendRequestService.send_friend_request(
            request.user, to_user
        )

        # Log the success or failure of sending the friend request
        if response_status == status.HTTP_201_CREATED:
            logger.info(
                f"Friend request sent successfully from user {request.user.id} to user {to_user_id}"
            )
        else:
            logger.error(
                f"Failed to send friend request from user {request.user.id} to user {to_user_id}: {response_data.get('error')}"
            )

        # Return the response data and status received from the friend request service
        return Response(response_data, status=response_status)


# Define a class for handling friend list API requests
class FriendListAPIView(generics.ListAPIView):
    """
    Specify the serializer class to use for serializing/deserializing Friendship objects
    """

    serializer_class = FriendshipSerializer

    # Define a method to customize the queryset for retrieving friendships
    def get_queryset(self):
        # Construct a queryset to retrieve friendships where the authenticated user is either the sender or the receiver,
        # and the friendship has been accepted (accepted=True)
        return Friendship.objects.filter(
            Q(
                from_user=self.request.user, accepted=True
            )  # Friendship where the authenticated user is the sender
            | Q(
                to_user=self.request.user, accepted=True
            )  # Friendship where the authenticated user is the receiver
        )


# Define a class for handling pending friend request list API requests
class PendingFriendRequestListAPIView(generics.ListAPIView):
    """
    Specify the serializer class to use for serializing/deserializing Friendship objects
    """

    serializer_class = FriendshipSerializer1

    # Define a method to customize the queryset for retrieving pending friend requests
    def get_queryset(self):
        # Construct a queryset to retrieve pending friend requests where the authenticated user is the receiver
        # and the friendship has not been accepted (accepted=False)
        return Friendship.objects.filter(to_user=self.request.user, accepted=False)


# Define a class for handling friend request rejection API requests
class RejectFriendRequestAPIView(generics.DestroyAPIView):
    """
    Specify the queryset to retrieve all Friendship objects
    """

    queryset = Friendship.objects.all()

    # Specify the serializer class to use for serializing/deserializing Friendship objects
    serializer_class = FriendshipSerializer

    # Define a method to handle DELETE requests for rejecting friend requests
    def delete(self, request, *args, **kwargs):
        # Retrieve the friendship object to be rejected using the from_user and to_user fields
        friendship = get_object_or_404(
            Friendship, from_user=request.user, to_user=self.kwargs["pk"]
        )

        # Delete the friendship object
        friendship.delete()

        # Return a success response indicating that the friend request has been rejected
        return Response(status=status.HTTP_204_NO_CONTENT)


# Define a class for handling friend request acceptance API requests
class AcceptFriendRequestView(APIView):
    """
    Define a method to handle POST requests for accepting friend requests
    """

    def post(self, request, request_id):
        try:
            # Retrieve the friend request object to be accepted
            friend_request = get_object_or_404(
                Friendship, id=request_id, to_user=request.user, accepted=False
            )

            # Initialize a serializer with the friend request object and update the 'accepted' field to True
            serializer = FriendRequestAcceptSerializer(
                friend_request, data={"accepted": True}
            )

            # Check if the serializer data is valid
            if serializer.is_valid():
                # Save the serializer data (update the friend request object with the accepted status)
                serializer.save()

                # Log the successful acceptance of the friend request
                logger.info(f"Friend request {request_id} accepted by {request.user}.")

                # Return a success response with the serialized data of the updated friend request
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                # Log a warning if the serializer data is invalid
                logger.warning(
                    f"Failed to accept friend request {request_id}: Invalid serializer data."
                )

                # Return a response with errors if the serializer data is invalid
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # Log an error if an unexpected exception occurs
            logger.error(
                f"Error accepting friend request {request_id}: {e}", exc_info=True
            )

            # Return a response indicating an internal server error if an exception occurs
            return Response(
                {"detail": "An unexpected error occurred."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
