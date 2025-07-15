from rest_framework.generics import CreateAPIView

from booking.serializers import BookSerializer


class BookCreateView(CreateAPIView):
    serializer_class = BookSerializer
