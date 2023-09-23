from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='home_page'),
    # Rooms rate API"S
    path('room-list/', views.RoomRateListView.as_view(), name='room_rate_list'),
    path('room/create/', views.RoomRateCreateView.as_view(), name='room_rate_create'),
    path('room/<int:pk>/update/', views.RoomRateUpdateView.as_view(), name='room_rate_update'),
    path('room/<int:pk>/delete/', views.RoomRateDeleteView.as_view(), name='room_rate_delete'),

    # Overridden room rate API's
    path('overridden-list/', views.OverriddenListView.as_view(), name='overridden_list'),
    path('overridden/create/', views.OverriddenCreateView.as_view(), name='overridden_create'),
    path('overridden/<int:pk>/update/', views.OverriddenUpdateView.as_view(), name='overridden_update'),
    path('overridden/<int:pk>/delete/', views.OverriddenDeleteView.as_view(), name='overridden_delete'),

    # Discounts API's
    path('discount-list/', views.DiscountListView.as_view(), name='discount_list'),
    path('discount/create/', views.DiscountCreateView.as_view(), name='discount_create'),
    path('discount/<int:pk>/update/', views.DiscountUpdateView.as_view(), name='discount_update'),
    path('discount/<int:pk>/delete/', views.DiscountDeleteView.as_view(), name='discount_delete'),

    # Discount Rate APIs
    path('discount-rate-list/', views.DiscountRoomRateListView.as_view(), name='discount_rate_list'),
    path('discount-rate/create/', views.DiscountRoomRateCreateView.as_view(), name='discount_rate_create'),
    path('discount-rate/<int:pk>/update/', views.DiscountRoomRateUpdateView.as_view(), name='discount_rate_update'),
    path('discount-rate/<int:pk>/delete/', views.DiscountRoomRateDeleteView.as_view(), name='discount_rate_delete'),

    # Calculate Lowest rate APIS
    path('filter-room-rates/', views.FilterRoomRates.as_view(), name='filter_room_rates'),
    path('rate-results/<str:room_id>/<str:start_date>/<str:end_date>/', views.CalculateFinalRate.as_view(),
         name='calculate_final_rate'),
]
