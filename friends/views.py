from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from .models import FriendRequest
from .serializers import FriendRequestSerializer

class FriendRequestView(generics.CreateAPIView):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        from_user = self.request.user
        to_user = User.objects.get(email=self.request.data['to_user'])
        serializer.save(from_user=from_user, to_user=to_user)



from rest_framework.throttling import UserRateThrottle

class FriendRequestThrottle(UserRateThrottle):
    rate = '3/min'  # Limit 3 requests per minute



from django.core.cache import cache

class FriendsListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        friends = cache.get(f'friends_{self.request.user.id}')
        if not friends:
            friends = self.request.user.friends.all()
            cache.set(f'friends_{self.request.user.id}', friends, timeout=60*15)  # Cache for 15 minutes
        return friends