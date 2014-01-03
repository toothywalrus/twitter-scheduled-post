from rest_framework import viewsets, generics

from .models import WebPage, Link
from .serializers import WebPageSerializer, LinkSerializer

# class WebPageDetail(generics.RetrieveUpdateDestroyAPIView):
#     model = WebPage
#     serializer_class = WebPageSerializer
#     permission_classes = [
#         permissions.AllowAny
#     ]

# class WebPageList(generics.ListAPIView):
#     model = WebPage
#     serializer_class = WebPageSerializer
#     permission_classes = [
#         permissions.AllowAny
#     ]

class WebPageViewSet(viewsets.ModelViewSet):
	queryset = WebPage.objects.all()
	serializer_class = WebPageSerializer
	
class PageLinkList(generics.ListAPIView):
    model = Link
    serializer_class = LinkSerializer
    
    def get_queryset(self):
        queryset = super(PageLinkList, self).get_queryset()
        return queryset.filter(page__pk=self.kwargs.get('pk'))