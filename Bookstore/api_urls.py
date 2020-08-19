from rest_framework import routers
from shop.api_views import BookViewSet, AuthorViewSet, PublisherViewSet

router = routers.SimpleRouter()
router.register('book', BookViewSet, base_name='book')
router.register('author', AuthorViewSet, base_name='author')
router.register('publisher', PublisherViewSet, base_name='publisher')
