"""Main models for app"""
from datetime import datetime, timedelta
from decimal import Decimal
import random

from django.db.models import Q, Case, When, Value as V, BooleanField
from django.utils.safestring import mark_safe
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


COLOURS = (
    ('#BEBEBE', 'grey'),
    ('#0000FF', 'blue'),
    ('#00FF00', 'green'),
    ('#FFC0CB', 'pink'),
    ('#EEEE00', 'yellow'),
    ('#F5F5DC', 'beige'),
    ('#FFD39B', 'light wood'),
    ('#8B7355', 'dark wood'),
    ('#000000', 'black'),
    ('#FFFFFF', 'white'),
    ('#FFE4C4', 'bisque'),
    ('#BDB76B', 'dark khaki'),
    ('#DEB887', 'burlywood'),
    ('#CDC8B1', 'cornsilk'),
)

COUNTRYS = (
    ('italy', 'italy'),
    ('germany', 'germany'),
    ('switzerland', 'switzerland'),
    ('portugal', 'switzerland'),
    ('poland', 'poland'),
    ('england', 'england'),
)

DISCOUNTS = (
    (5, 5),
    (10, 10),
    (15, 15),
    (20, 20),
)

MATERIALS = (
    ('Fabric', (
        ('fabric', 'fabric'),
        ('cotton', 'cotton'),
        ('velvet', 'velvet'),
        ('corduroy', 'corduroy'),
    )
     ),
    ('Wood', (
        ('wood', 'wood'),
        ('oak', 'oak'),
        ('wallnut', 'wallnut'),
        ('rubbeewood', 'rubbeewood'),
        ('solid wood', 'solid wood'),
        ('cane', 'cane'),
        ('jute', 'jute'),
        ('linen mix', 'linen mix'),
        ('mango wood', 'mango wood'),
        ('mango wood', 'mango wood'),
    
    )
     ),
    ('Leather', (
        ('leather', 'leather'),
        ('wool', 'wool'),
        ('sheepskin', 'sheepskin'),
    )
     ),
    ('Other', (
        ('concrete', 'concrete'),
        ('metal', 'metal'),
        ('brass', 'brass'),
        ('plastic', 'plastic'),
        ('polyurethane', 'polyurethane'),
        ('stone', 'stone'),
    )
     )
)

WARRANTY = (
    (12, '12'),
    (24, '24'),
    (36, '36'),
    (48, '48'),
)

NEW_PRODUCTS_DELTA_DAYS = 180


class ActiveObjectsManager(models.Manager):
    
    def get_queryset(self):
        """By default, It is supposed to get only active products"""
        
        return super().get_queryset().filter(Q(is_active=True))
    
    def get_products_for_main_filter(self):
        """Getting products for ProductsListView"""
        current_date = datetime.today()
        start_date = current_date - timedelta(days=NEW_PRODUCTS_DELTA_DAYS)
        
        return self.get_queryset().select_related('category') \
            .select_related('product_sub_type').only(
            'category__name',
            'category__absolute_url',
            'product_sub_type__absolute_url',
            'product_sub_type__name_singular',
            'absolute_url',
            'slug',
            'name',
            'price',
            'image',
            'image_second',
            'short_description',
            'is_discount',
            'sum_discount',
        ).annotate(
            new=Case(When(Q(created_at__gte=start_date) &
                          Q(created_at__lte=current_date),
                          then=V(True)), default=V(False), output_field=BooleanField()))
    
    def get_certain_product(self):
        """Getting specific product for ProductDetailView"""
        current_date = datetime.today()
        start_date = current_date - timedelta(days=NEW_PRODUCTS_DELTA_DAYS)
        
        return self.get_queryset().select_related('category') \
            .select_related('product_type') \
            .only(
            'category__name',
            'category__absolute_url',
            'product_type__absolute_url',
            'product_type__name',
            'absolute_url',
            'sku',
            'slug',
            'quantity',
            'description',
            'weight',
            'product_dimensions',
            'country',
            'warranty',
            'recommended_load',
            'name',
            'price',
            'image',
            'image_second',
            'colour',
            'short_description',
            'is_discount',
            'sum_discount',
        ).annotate(
            new=Case(When(Q(created_at__gte=start_date) &
                          Q(created_at__lte=current_date),
                          then=V(True)), default=V(False), output_field=BooleanField()))
    
    @property
    def miniproduct(self):
        """Getting a common products fields for MainView or
        other specific blocks (recently viewed etc.)"""
        
        return self.get_queryset().select_related('category').only(
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
    
    @property
    def miniproduct_with_product_type(self):
        """It's like self.miniproduct, only with JOIN product_type"""
        
        return self.get_queryset().select_related('category') \
            .select_related('product_type').only(
            'category__name',
            'category__absolute_url',
            'product_type__name',
            'product_type__absolute_url',
            'absolute_url',
            'slug',
            'name',
            'price',
            'is_discount',
            'sum_discount',
            'image',
        )


class ProductCategory(models.Model):
    absolute_url = models.URLField(
        verbose_name='absolute url',
        blank=True,
        null=True,
    )
    name = models.CharField(
        verbose_name='name',
        blank=False,
        max_length=40,
        unique=True,
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        db_index=True,
        verbose_name='Slug'
    )
    image = models.ImageField(
        upload_to='products_categories',
        blank=True,
        null=True,
    )
    description = models.CharField(
        verbose_name='description',
        max_length=128,
        blank=True,
    )
    notes = models.CharField(
        verbose_name='notes',
        max_length=64,
        blank=True,
    )
    created_at = models.DateTimeField(
        verbose_name='created at',
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        verbose_name='updated at',
        auto_now=True,
    )
    is_active = models.BooleanField(
        verbose_name='active',
        default=True,
    )
    
    objects = models.Manager()
    active_objects = ActiveObjectsManager()
    
    def __str__(self):
        return str(self.name)
    
    def __repr__(self):
        return str(self.name)
    
    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    
    @property
    def get_absolute_url(self):
        return reverse('main:shop', kwargs={'slug': self.slug})
    
    @property
    def admin_image(self) -> str:
        """Getting product image for admin panel"""
        
        if self.image:
            return mark_safe(
                u'<a href="{0}" target="_blank"><img src="{1}" width="100"/></a>'.format(
                    self.absolute_url, self.image.url)
            )
        return '<img src="/static/admin/img/icon-no.svg" alt="False">'
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, allow_unicode=True)
        self.absolute_url = self.get_absolute_url
        super().save(*args, **kwargs)


class ProductType(models.Model):
    absolute_url = models.URLField(
        verbose_name='absolute url',
        blank=True,
        null=True,
    )
    name = models.CharField(
        verbose_name='name',
        blank=False,
        unique=True,
        max_length=40,
    )
    name_singular = models.CharField(
        verbose_name='name singular',
        blank=False,
        unique=True,
        max_length=40,
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        db_index=True,
        verbose_name='url',
    )
    image = models.ImageField(
        upload_to='products_types',
    )
    description = models.CharField(
        verbose_name='description',
        max_length=128,
        blank=True,
    )
    notes = models.CharField(
        verbose_name='notes',
        max_length=64,
        blank=True,
    )
    created_at = models.DateTimeField(
        verbose_name='created at',
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        verbose_name='updated at',
        auto_now=True,
    )
    is_active = models.BooleanField(
        verbose_name='active',
        default=True,
    )
    
    objects = models.Manager()
    active_objects = ActiveObjectsManager()
    
    def __str__(self):
        return str(self.name)
    
    def __repr__(self):
        return str(self.name)
    
    class Meta:
        verbose_name = 'product type'
        verbose_name_plural = 'product types'
    
    @property
    def get_absolute_url(self):
        return reverse('main:shop', kwargs={'slug': self.slug})
    
    @property
    def admin_image(self) -> str:
        """Getting product image for admin panel"""
        
        if self.image:
            return mark_safe(
                u'<a href="{0}" target="_blank"><img src="{1}" width="100"/></a>'.format(
                    self.absolute_url, self.image.url)
            )
        return '<img src="/static/admin/img/icon-no.svg" alt="False">'
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, allow_unicode=True)
        self.absolute_url = self.get_absolute_url
        super().save(*args, **kwargs)


class ProductSubType(models.Model):
    product_type = models.ForeignKey(
        ProductType,
        on_delete=models.CASCADE,
    )
    absolute_url = models.URLField(
        verbose_name='absolute url',
        blank=True,
        null=True,
    )
    name = models.CharField(
        verbose_name='name',
        blank=False,
        unique=True,
        max_length=40,
    )
    name_singular = models.CharField(
        verbose_name='name singular',
        blank=False,
        unique=True,
        max_length=40,
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        db_index=True, verbose_name='url',
    )
    image = models.ImageField(
        upload_to='products_subtypes',
        blank=True,
    )
    description = models.CharField(
        verbose_name='description', max_length=128,
        blank=True,
    )
    notes = models.CharField(
        verbose_name='notes',
        max_length=64,
        blank=True,
    )
    created_at = models.DateTimeField(
        verbose_name='created at',
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        verbose_name='updated at',
        auto_now=True,
    )
    is_active = models.BooleanField(
        verbose_name='active',
        default=True,
    )
    
    objects = models.Manager()
    active_objects = ActiveObjectsManager()
    
    def __str__(self):
        return str(self.name)
    
    class Meta:
        verbose_name = 'product subtype'
        verbose_name_plural = 'product subtypes'


class Product(models.Model):
    category = models.ForeignKey(
        ProductCategory,
        on_delete=models.SET_NULL,
        null=True,
    )
    product_type = models.ForeignKey(
        ProductType,
        on_delete=models.SET_NULL,
        null=True,
    )
    product_sub_type = models.ForeignKey(
        ProductSubType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    absolute_url = models.URLField(
        verbose_name='absolute url',
        blank=True,
        null=True,
    )
    sku = models.CharField(
        verbose_name='SKU',
        blank=True,
        unique=True,
        max_length=124,
        editable=False,
    )
    name = models.CharField(
        verbose_name='name',
        blank=False,
        unique=True,
        max_length=124)
    slug = models.SlugField(
        max_length=255,
        unique=True,
        db_index=True,
        verbose_name='url',
        editable=False,
    )
    created_at = models.DateTimeField(
        verbose_name='created at',
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        verbose_name='updated at',
        auto_now=True,
    )
    image = models.ImageField(
        upload_to='products_images',
        blank=True,
        null=True,
    )
    image_second = models.ImageField(
        upload_to='products_images',
        blank=True,
        null=True,
    )
    colour = models.CharField(
        max_length=40,
        choices=COLOURS,
        blank=True,
        null=True,
    )
    price = models.DecimalField(
        verbose_name='price',
        max_digits=8,
        decimal_places=2,
        blank=True,
        null=True,
    )
    is_discount = models.BooleanField(
        verbose_name='discount',
        default=False,
        blank=True,
        null=True,
    )
    sum_discount = models.PositiveIntegerField(
        verbose_name='sum discount',
        choices=DISCOUNTS,
        blank=True,
        null=True,
    )
    quantity = models.PositiveIntegerField(
        verbose_name='quantity',
        blank=True,
        null=True,
    )
    is_active = models.BooleanField(
        verbose_name='active',
        default=True,
        blank=True,
        null=True,
    )
    short_description = models.TextField(
        verbose_name='short description',
        max_length=200,
        blank=True,
        null=True,
    )
    description = models.TextField(
        verbose_name='description',
        max_length=960,
        blank=True,
        null=True,
    )
    notes = models.CharField(
        verbose_name='notes',
        max_length=64,
        blank=True,
        null=True,
    )
    product_dimensions = models.CharField(
        verbose_name='product dimensions',
        max_length=40,
        blank=True,
        null=True,
    )
    weight = models.PositiveIntegerField(
        verbose_name='weight',
        blank=True,
        null=True,
    )
    packaging_dimensions = models.CharField(
        verbose_name='packaging dimensions',
        max_length=128,
        blank=True,
        null=True,
    )
    country = models.CharField(
        verbose_name='country',
        choices=COUNTRYS,
        max_length=40,
        blank=True,
        null=True,
    )
    warranty = models.PositiveIntegerField(
        verbose_name='warranty in month',
        choices=WARRANTY,
        blank=True,
        null=True,
    )
    recommended_load = models.PositiveIntegerField(
        verbose_name='recommended load',
        blank=True,
        null=True,
    )
    
    objects = models.Manager()
    active_objects = ActiveObjectsManager()
    
    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'
        unique_together = (
            ('name', 'image'),
            ('name', 'sku'),
            ('name', 'colour', 'product_sub_type'),
            ('name', 'created_at', 'image'),
            ('name', 'sku', 'created_at', 'image'),
        )
        indexes = (
            models.Index(fields=[
                'name',
                'sku',
                'is_discount',
            ]),
        )
        constraints = (models.UniqueConstraint(fields=('name', 'sku'),
                                               name=' %(app_label)s_%(class)s_title_price_constraint'),
                       )
    
    def __str__(self):
        return str(self.name)
    
    def save(self, *args, **kwargs):
        """Generating arbitrary data for some fields before saving """
        
        # generate a datetime in format yyyy-mm-dd hh:mm:ss.000000
        def gen_datetime(min_year=2020, max_year=datetime.now().year):
            start = datetime(min_year, 1, 1, 00, 00, 00)
            years = max_year - min_year + 1
            end = start + timedelta(days=365 * years)
            return start + (end - start) * random.random()
        
        sku = self.sku
        if sku:
            super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)
            primary_key = '{:04d}'.format(self.pk)
            category = self.category.primary_key
            product_type = self.product_type.primary_key
            product_sub_type = self.product_sub_type.primary_key
            product_sub_type_name = self.product_sub_type.name_singular
            name = self.name
            self.created_at = gen_datetime(min_year=2020)
            self.colour = COLOURS[random.randint(0, len(COLOURS) - 1)][random.randint(0, 1)]
            self.price = Decimal('{:.2f}'.format(random.randint(200, 4000)))
            self.is_discount = random.choice([True, False])
            if self.is_discount:
                self.sum_discount = DISCOUNTS[random.randint(0, len(DISCOUNTS) - 1)][random.randint(0, 1)]
            else:
                self.sum_discount = None
            self.quantity = random.randint(0, 100)
            self.description = "Lorem Ipsum is simply dummy text of the printing and typesetting industry. " \
                               "Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, " \
                               "when anunknown printer took a galley of type and scrambled it to " \
                               "make a type specimen book. " \
                               "It has survived not only five centuries, but also the leap into " \
                               "electronic typesetting, " \
                               "remaining essentially unchanged. " \
                               "It was popularised in the 1960s with the release of Letraset sheets " \
                               "containing Lorem Ipsum passages. It has survived not only five centuries, but " \
                               "also the leap into electronic typesetting, remaining essentially unchanged. " \
                               "It was popularised in the 1960s with the release. " \
                               "Ipsum is simply dummy text of the printing and typesetting industry. " \
                               "Lorem Ipsum has been the industry's"
            self.product_dimensions = f'{random.randint(0, 140)} X ' \
                                      f'{random.randint(0, 100)} X {random.randint(0, 180)}'
            self.weight = random.randint(60, 450)
            self.packaging_dimensions = f'{random.randint(0, 140)} X ' \
                                        f'{random.randint(0, 100)} X {random.randint(0, 180)}'
            self.country = COUNTRYS[random.randint(0, len(COUNTRYS) - 1)][random.randint(0, 1)]
            self.warranty = WARRANTY[random.randint(0, len(WARRANTY) - 1)][random.randint(0, 1)]
            self.recommended_load = random.randint(100, 200)
            
            sku = f'{category}{product_type}{product_sub_type}{primary_key}'
            self.sku = sku
            value = f'{name}-{self.colour}-{product_sub_type_name}'
            self.slug = slugify(value, allow_unicode=True)
            super().save(*args, **kwargs)
    
    @property
    def admin_image(self) -> str:
        """Getting product image for admin panel"""
        
        if self.image:
            return mark_safe(
                u'<a href="{0}" target="_blank"><img src="{1}" width="100"/></a>'.format(
                    self.absolute_url, self.image.url)
            )
        return '<img src="/static/admin/img/icon-no.svg" alt="False">'
    
    @property
    def get_total_price(self) -> Decimal:
        if self.is_discount:
            return Decimal('{:.2f}'.format(self.price * (100 - self.sum_discount) / 100))
        return Decimal('{:.2f}'.format(self.price))
    
    @property
    def get_absolute_url(self):
        return reverse('main:product_detail', kwargs={'slug': self.slug})


class PageHitCount(models.Model):
    """Accounting for the number of page visits"""
    url = models.URLField(verbose_name='url', unique=True)
    count = models.PositiveBigIntegerField(verbose_name='count', default=0)
    
    objects = models.Manager()
