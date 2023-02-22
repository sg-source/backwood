from backwood import settings_base as settings

from main.models import Product


class Favourites:

    def __init__(self, request):
        self.request = request
        self.session = request.session
        favourites: list[Product.id] = self.session.get(settings.FAVOURITES_SESSION_ID)
        if not favourites:
            favourites = self.session[settings.FAVOURITES_SESSION_ID] = []
        self.favourites: list[Product.id] = favourites

    def __repr__(self):
        return str(self.favourites)

    def __getitem__(self, item: int):
        if item:
            index = self.favourites.index(item)
            return self.favourites[index]
        raise ValueError("This element doesn't exist in the list")

    def __contains__(self, item):
        if item in self.favourites:
            return True
        return False

    def __iter__(self) -> Product:
        products = Product.active_objects.filter(pk__in=self.favourites)
        for item in products:
            yield item

    def __len__(self):
        return len(self.favourites)

    def update(self, product_id: int):
        if product_id in set(self.favourites):
            self.delete(product_id)
        else:
            self.favourites.append(product_id)
            self.save()

    def save(self):
        self.session.modified = True

    def delete(self, product_id: int):
        self.favourites.remove(product_id)
        self.save()

    def clear(self):
        del self.session[settings.FAVOURITES_SESSION_ID]
        self.save()
