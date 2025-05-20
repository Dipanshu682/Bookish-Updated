from django.urls import path
from . import views

urlpatterns = [
    path('', views.BookListView.as_view(), name='book-list'),
    path('book_detail/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    path('book_sell/', views.BookSellView.as_view(), name='book-sell'),
    path('book/<int:pk>/edit/', views.BookUpdateView.as_view(), name='book-update'),
    path('book/<int:pk>/delete/', views.BookDeleteView.as_view(), name='book-delete'),

    path('buy/<int:pk>/', views.BuyNowView.as_view(), name='buy-now'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('remove-from-cart/<int:pk>/', views.RemoveFromCartView.as_view(), name='remove-from-cart'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),

    path('cart/add/<int:pk>/', views.CartAddView.as_view(), name='cart-add'),
    path('cart/decrease/<int:pk>/', views.CartDecreaseView.as_view(), name='cart-decrease'),

    path('my-books/', views.UserBookListView.as_view(), name='user-books'),
    path('profile/', views.ProfileDetailView.as_view(), name='profile'),
    path('profile/update/', views.ProfileUpdateView.as_view(), name='profile-update'),
]
 