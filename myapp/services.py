# services.py

from .models import Friendship
from .serializers import FriendshipSerializer
from django.core.exceptions import ValidationError
from rest_framework import status
import logging
from django.db import IntegrityError


logger = logging.getLogger(__name__)


# Define a service class for handling friend requests
class FriendRequestService:
    """
    Static method for sending friend requests
    """

    @staticmethod
    def send_friend_request(from_user, to_user):
        try:
            # Check if the sender and receiver are the same user
            if from_user == to_user:
                logger.error("Attempt to send a friend request to oneself")
                raise ValidationError("You cannot send a friend request to yourself.")

            # Check if a friend request has already been sent from the sender to the receiver
            if Friendship.objects.filter(from_user=from_user, to_user=to_user).exists():
                logger.warning("Friend request already sent to this user.")
                raise ValidationError(
                    "You've already sent a friend request to this user."
                )

            # Check if a friend request has already been received from the sender by the receiver
            if Friendship.objects.filter(from_user=to_user, to_user=from_user).exists():
                logger.warning("Friend request already received from this user.")
                raise ValidationError(
                    "Do not send a friend request to the same user again."
                )

            # Create a new Friendship object representing the friend request
            friend_request = Friendship.objects.create(
                from_user=from_user, to_user=to_user
            )

            # Serialize the newly created Friendship object
            serializer = FriendshipSerializer(friend_request)

            # Return a success response with the serialized data of the new friend request
            return {
                "message": "Friend request sent successfully.",
                "data": serializer.data,
            }, status.HTTP_201_CREATED

        # Catch IntegrityError exceptions, typically raised for database integrity constraints violations
        except IntegrityError as e:
            logger.error(f"Failed to create friendship record: {e}")
            return {
                "error": "An unexpected error occurred."
            }, status.HTTP_500_INTERNAL_SERVER_ERROR

        # Catch ValidationError exceptions, raised for validation errors
        except ValidationError as e:
            logger.warning(f"Friend request validation error: {e}")
            return {"error": str(e)}, status.HTTP_400_BAD_REQUEST
