from django.urls import path

from booking import views

app_name = "booking"
urlpatterns = [
    path("book/", views.BookCreateView.as_view(), name="book"),
    path("<int:pk>/cancel/", views.CancelDestroyView.as_view(), name="cancel"),
]
