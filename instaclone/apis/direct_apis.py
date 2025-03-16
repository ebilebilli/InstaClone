from django.shortcuts import get_object_or_404
from rest_framework.views import APIView, Response, status
from django.db.models import Q
from apis.permission_control import HeHasPermission, IsAuthenticated, AllowAny, TokenAuthentication, IsOwner
from profiles.models import Profile
from direct_messages.models import DirectMessage
from direct_messages.serializers import DirectMessageSerializer
from profiles.serializers import ProfileSerializer


class SendMessageToOpenProfileAPIView(APIView):
    """API endpoint for sending messages to public profiles."""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, profile_id, *args, **kwargs):
        """Send a direct message to an open profile.
        
        Args:
            request: HTTP request object containing message data
            profile_id: ID of the profile to send message to
            
        Returns:
            Response: Serialized message data on success, error details on failure
        """
        profile = get_object_or_404(Profile, id=profile_id)

        if profile.user == request.user:
            return Response({'Message': 'You cannot send message to yourself'},
                           status=status.HTTP_400_BAD_REQUEST)
        
        serializer = DirectMessageSerializer(request.data, many=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SendMessageToPrivateProfileAPIView(APIView):
    """API endpoint for sending messages to private profiles."""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, HeHasPermission]

    def post(self, request, profile_id, *args, **kwargs):
        """Send a direct message to a private profile.
        
        Args:
            request: HTTP request object containing message data
            profile_id: ID of the profile to send message to
            
        Returns:
            Response: Serialized message data on success, error details on failure
        """
        profile = get_object_or_404(Profile, id=profile_id)

        if profile.user == request.user:
            return Response({'Message': 'You cannot send message to yourself'},
                           status=status.HTTP_400_BAD_REQUEST)
        
        serializer = DirectMessageSerializer(request.data, many=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileMessageListAPIView(APIView):  
    """API endpoint for listing messages for a specific profile."""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsOwner]

    def get(self, request, profile_id):
        """Retrieve all messages for a specific profile.
        
        Args:
            request: HTTP request object
            profile_id: ID of the profile to retrieve messages for
            
        Returns:
            Response: Serialized list of messages or error message
        """
        messages = DirectMessage.objects.filter(Q(sender_user=request.user) & Q(receiver_user=request.user))
        profile = get_object_or_404(Profile, id=profile_id)
        if request.user != profile.user:
            return Response({'message': 'You are not authorized.'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = DirectMessageSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OpenProfileMessageManagementAPIView(APIView):
    """API endpoint for managing messages with open profiles."""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, profile_id):
        """Retrieve messages between current user and an open profile.
        
        Args:
            request: HTTP request object
            profile_id: ID of the profile to retrieve messages for
            
        Returns:
            Response: Serialized list of messages or error message
        """
        profile = get_object_or_404(Profile, id=profile_id)
        messages = DirectMessage.objects.filter(
            (Q(sender_user=request.user) & Q(receiver_user=profile.user)) | 
            (Q(sender_user=profile.user) & Q(receiver_user=request.user))
        )
        serializer = DirectMessageSerializer(messages, many=True)
        if serializer:
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'Message': 'There is not any message'}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, profile_id):
        """Delete a specific message sent by the current user.
        
        Args:
            request: HTTP request object
            profile_id: ID of the message to delete
            
        Returns:
            Response: Success message or error message
        """
        chat = get_object_or_404(DirectMessage, id=profile_id)
        if chat.sender_user != request.user:
            return Response({'message': 'You are not authorized.'}, status=status.HTTP_400_BAD_REQUEST)
        
        chat.delete()
        return Response({'message': 'Comment deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
    
    def patch(self, request, profile_id):
        """Update a specific message sent by the current user.
        
        Args:
            request: HTTP request object containing updated message data
            profile_id: ID of the message to update
            
        Returns:
            Response: Serialized updated message or error details
        """
        chat = get_object_or_404(DirectMessage, id=profile_id)
        if chat.sender_user != request.user:
            return Response({'message': 'You are not authorized.'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = DirectMessageSerializer(chat, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PrivateProfileMessageManagementAPIView(APIView):
    """API endpoint for managing messages with private profiles."""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, HeHasPermission]

    def get(self, request, profile_id):
        """Retrieve messages between current user and a private profile.
        
        Args:
            request: HTTP request object
            profile_id: ID of the profile to retrieve messages for
            
        Returns:
            Response: Serialized list of messages or error message
        """
        profile = get_object_or_404(Profile, id=profile_id)
        messages = DirectMessage.objects.filter(
            (Q(sender_user=request.user) & Q(receiver_user=profile.user)) | 
            (Q(sender_user=profile.user) & Q(receiver_user=request.user))
        )
        serializer = DirectMessageSerializer(messages, many=True)
        if serializer:
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'Message': 'There is not any message'}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, profile_id):
        """Delete a specific message sent by the current user to a private profile.
        
        Args:
            request: HTTP request object
            profile_id: ID of the message to delete
            
        Returns:
            Response: Success message or error message
        """
        chat = get_object_or_404(DirectMessage, id=profile_id)
        if chat.sender_user != request.user:
            return Response({'message': 'You are not authorized.'}, status=status.HTTP_400_BAD_REQUEST)
        
        chat.delete()
        return Response({'message': 'Comment deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
    
    def patch(self, request, profile_id):
        """Update a specific message sent by the current user to a private profile.
        
        Args:
            request: HTTP request object containing updated message data
            profile_id: ID of the message to update
            
        Returns:
            Response: Serialized updated message or error details
        """
        chat = get_object_or_404(DirectMessage, id=profile_id)
        if chat.sender_user != request.user:
            return Response({'message': 'You are not authorized.'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = DirectMessageSerializer(chat, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)