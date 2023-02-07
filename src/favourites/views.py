from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView
from django.views.generic.edit import BaseUpdateView, DeletionMixin

from .favourites import Favourites
from main.models import Product


class FavouritesDetailView(TemplateView):
    template_name = 'favourites/favourites_list.html'
    

@method_decorator(require_POST, name='dispatch')
class FavouritesUpdateView(BaseUpdateView):
    def setup(self, request, *args, **kwargs):
        self.favourites = Favourites(request)
        super().setup(request, *args, **kwargs)
     
    def update(self, request, *args, **kwargs):
        pk = self.kwargs.get('product_id')
        product = get_object_or_404(Product, pk=pk)
        if product:
            self.favourites.update(int(product.id))
            if request.POST['location'] and request.POST['location'] != '/':
                return render(request, 'main/includes/header.html')
            return render(request, 'main/includes/header_actions.html')
        
    def post(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class FavouritesRemoveView(DeletionMixin, View):
    
    def setup(self, request, *args, **kwargs):
        self.favourites = Favourites(request)
        super().setup(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        if self.favourites:
            pk = self.kwargs.get('product_id')
        
            if pk is not None:
                product = get_object_or_404(Product, pk=pk)
                self.favourites.delete(product.id)
                if self.favourites:
                    return render(request, 'favourites/includes/favourites_list-table.html')
                
                return render(request, 'favourites/includes/empty_favourites.html')
