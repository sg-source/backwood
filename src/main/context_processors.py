from .recently_viewed import RecentlyViewedProducts


def recently_viewed(request):
    recently_viewed_products = RecentlyViewedProducts(request)
    return {'recently_viewed': recently_viewed_products, 'recently_viewed_len': len(RecentlyViewedProducts(request))}


def accept_header_banner(request):
    is_accepted = request.COOKIES.get('header_banner')
    return {'header_banner': False} if is_accepted == 'accepted' else {'header_banner': True}
