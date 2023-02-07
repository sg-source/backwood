from django.urls import path

from . import views
from .views import FavouritesDetailView, FavouritesUpdateView, FavouritesRemoveView

app_name = 'favourites'

urlpatterns = [
    path('', FavouritesDetailView.as_view(extra_context={'title': 'My Favourites'}), name='detail'),
    path('add/<int:product_id>', FavouritesUpdateView.as_view(), name='add'),
    path('remove/<int:product_id>', FavouritesRemoveView.as_view(), name='remove'),

]