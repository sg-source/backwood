from .recently_viewed import RecentlyViewedProducts


def recently_viewed(request):
    recently_viewed_products = RecentlyViewedProducts(request)
    return {'recently_viewed': recently_viewed_products, 'recently_viewed_len': len(RecentlyViewedProducts(request))}
