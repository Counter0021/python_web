from django.urls import path

from .views import index, by_rubric, BbCreateView

urlpatterns = [
    # URL параметр в <>, int - целочисленный тип параметра
    # rubric id — имя параметра контроллера, которому будет присвоено значение этого URL параметра
    # параметризованный параметр
    path('<int:rubric_id>/', by_rubric, name='by_rubric'),
    path('', index, name='index'),
    path('add/', BbCreateView.as_view(), name='add'),
]
