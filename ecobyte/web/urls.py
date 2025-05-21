from django.urls import path
from . import views


app_name = "web"

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('food-listings/', views.food_listings, name='food_listings'),
    path('food-listings/<int:listing_id>/claim/', views.claim_food, name='claim_food'),
    path('my-listings/', views.my_listings, name='my_listings'),
    path('donor/dashboard/', views.donor_dashboard, name='donor_dashboard'),
    path('collector/dashboard/', views.collector_dashboard, name='collector_dashboard'),
    path('donor/add-listing/', views.add_listing, name='add_listing'),
    path('donor/delete-listing/<int:listing_id>/', views.delete_listing, name='delete_listing'),
]