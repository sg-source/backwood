from .favourites import Favourites


def favourites(request):
    favourites = Favourites(request)
    return {'favourites': favourites, 'favourites_len': len(Favourites(request))}
