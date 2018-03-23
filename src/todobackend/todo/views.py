
from todo.models import TodoItem
from todo.serializers import TodoItemSerializer
from rest_framework import status
from rest_framework import viewsets
from rest_framework.reverse import reverse
from rest_framework.decorators import list_route
from rest_framework.response import Response

class TodoItemViewSet(viewsets.ModelViewSet):
  queryset = TodoItem.objects.all()
  serializer_class = TodoItemSerializer
  
  def preform_create(self, serializer):
    instance = serializer.save()
    instance.url = reverse('todoitem-detail', args=[instance.pk], request=self.request)
    instance.save()

  def delete(self, request):
    TodoItem.objects.all().delete()  #dangerous
    return Response(status=status.HTTP_204_NO_CONTENT)
