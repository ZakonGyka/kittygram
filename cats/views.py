from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from rest_framework import mixins

from .models import Cat, Owner
from .serializers import CatSerializer, OwnerSerializer, CatListSerializer


# Описываем свой базовый класс вьюсета:
class CreateRetrieveViewSet(mixins.CreateModelMixin,
                            mixins.RetrieveModelMixin,
                            # mixins.ListModelMixin,
                            viewsets.GenericViewSet):
    # В теле класса никакой код не нужен! Пустячок, а приятно.
    pass


class LightCatViewSet(CreateRetrieveViewSet):
    queryset = Cat.objects.all()
    serializer_class = CatSerializer


class CatViewSet(viewsets.ModelViewSet):
    queryset = Cat.objects.all()
    serializer_class = CatSerializer

    def get_serializer_class(self):
        # Если запрошенное действие (action) — получение списка объектов ('list')
        if self.action == 'list':
            # ...то применяем CatListSerializer
            return CatListSerializer
        # А если запрошенное действие — не 'list', применяем CatSerializer
        return CatSerializer

    @action(detail=False, url_path='recent-white-cats')
    def recent_white_cats(self, request):
        # Нужны только последние два котика белого цвета
        cats = Cat.objects.filter(color='White')[:2]
        # Передадим queryset cats сериализатору
        # и разрешим работу со списком объектов
        serializer = self.get_serializer(cats, many=True)
        return Response(serializer.data)


class OwnerViewSet(viewsets.ModelViewSet):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer

# class CatList(generics.ListCreateAPIView):
#     queryset = Cat.objects.all()
#     serializer_class = CatSerializer

# class CatDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Cat.objects.all()
#     serializer_class = CatSerializer

'''
class APICAT(APIView):
    def get(self, request):
        cats = Cat.objects.all()
        serializer = CatSerializer(cats, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CatSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class APICatDetail(APIView):

    def patch(self, request, id):
        cat = Cat.objects.filter(id=id)
        serializer = CatSerializer(cat)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Функция cat_list работает при помощи декоратора @api_view
@api_view(['GET', 'POST'])
def cat_list(request):
    if request.method == 'POST':
        serializer = CatSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    cats = Cat.objects.all()
    serializer = CatSerializer(cats, many=True)
    return Response(serializer.data)
'''