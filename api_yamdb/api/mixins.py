from rest_framework import mixins, viewsets


class MyMixinViewSet(
        mixins.ListModelMixin,
        mixins.CreateModelMixin,
        mixins.DestroyModelMixin,
        viewsets.GenericViewSet):
    """Mixin for Category and Genre classes."""
    pass
