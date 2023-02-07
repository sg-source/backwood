from django.db.models import Q

from backwood import settings
from main.models import Product


class RecentlyViewedProducts:
    """Storing recently viewed products based on cookie as list including
    products id. It stores last 4 visited products"""
    
    def __init__(self, request):
        self.request = request
        self.session = request.session
        recently_viewed: list[Product.id] = self.session.get(settings.RECENTLY_VIEWED_SESSION_ID)
        if not recently_viewed:
            recently_viewed = self.session[settings.RECENTLY_VIEWED_SESSION_ID] = []
        self.recently_viewed: list[Product.id] = recently_viewed
    
    def __repr__(self):
        return str(self.recently_viewed)
    
    def __getitem__(self, item: int):
        """Instead of getting item by index, we receive element
         by its value. I don't remember why, let it lie here quietly"""
        try:
            index = self.recently_viewed.index(item)
            return self.recently_viewed[index]
        except ValueError:
            return None
    
    def __delitem__(self, item: int):
        if item:
            index = self.recently_viewed.index(item)
            del self.recently_viewed[index]
        else:
            raise ValueError("This element doesn't exist in the list")
    
    def __iter__(self) -> Product:
        products = Product.active_objects.filter(Q(pk__in=self.recently_viewed)).select_related('category') \
            .only(
                'category__name',
                'category__absolute_url',
                'absolute_url',
                'slug',
                'name',
                'price',
                'is_discount',
                'sum_discount',
                'image',
            )
        sorted_products = sorted(products, key=lambda x: self.recently_viewed.index(x.id), reverse=True)
        for item in sorted_products:
            yield item
    
    def __len__(self):
        return len(self.recently_viewed)
    
    def update(self, product_id: int):
        
        if product_id in set(self.recently_viewed):
            element = self.recently_viewed.pop(self.recently_viewed.index(product_id))
            self.update(element)
        else:
            if len(self.recently_viewed) >= 4:
                self.recently_viewed.pop(0)
            self.recently_viewed.append(product_id)
            self.save()
    
    def save(self):
        self.session.modified = True
    
    def remove(self, product_id: int):
        del self[product_id]
        self.save()
    
    def clear(self):
        del self.session[settings.RECENTLY_VIEWED_SESSION_ID]
        self.save()
