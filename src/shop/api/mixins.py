from rest_framework import mixins, viewsets


class RetriveListModelViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    pass


class CreateModelViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    pass
