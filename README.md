# cd-docker-ansible

sudo yum install -y epel-release
sudo yum -y update
sudo yum install -y docker-compose
sudo yum install -y docker
sudo yum update -y python2
sudo yum install -y python2-pip
sudo pip install pip --upgrade
sudo pip install ansible --upgrade

sudo pip install boto boto3 awscli #these are for talking to aws

sudo yum install -y git

#this bit is for setting up a proxy
sudo mkdir /etc/systemd/system/docker.service.d

sudo systemctl start docker

sudo pip install django==1.9

mkdir -p cd-docker-Ansible/src
cd cd-docker-Ansible/src
django-admin startproject todobackend

sudo pip install virtualenv
cd ..

virtualenv venv
source venv/bin/activiate

sudo pip install pip --upgrade
sudo pip install django==1.9
pip install djangorestframework==3.3
pip install django-cors-headers==1.1

cd src
python manage.py startapp todo

settings.py
add to installed apps in settings.py file and rest_framework and corsheaders
add 'corsheaders.middleware.CorsMiddleware', to middleware classes in 2nd place
add CORS_ORIGIN_ALLOW_ALL = True to bottom (not for prod)

echo '
class TodoItem(models.Model):
  title = models.CharField(max_lenth=256, null=True, blank=True)
  completed = models.BooleanField(blank=True, default=False)
  url = models.CharField(max_length=256, null=True, blank=True)
  order = models.IntegerField(null=True, blank=True)' >> todo/models.py

python manage.py makemigrations todo
python manage.py migrate

echo "
from rest_framework import serializers
from todo.models import TodoItem

class TodoItemSerializer(serializers.HyperlinkedModelSerializer):
  url = serializers.ReadOnlyField()
  class Meta:
    model = TodoItem
	fields = ('url', 'title', 'completed', 'order')" > todo/serializers.py

echo "
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
    return Response(status=status.HTTP_204_NO_CONTENT)" > todo/views.py

add url(r'^', include('todo.urls')), and add import for include from django.conf.urls to todobackend/urls.py

echo "
from django.conf.urls import url, include
from todo import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter(trailing_slash=False)
router.register(r'todos', views.TodoItemViewSet)

urlpatterns = [
url(r'^', include(router.urls)),
]" > todo/urls.py

python manage.py runserver
