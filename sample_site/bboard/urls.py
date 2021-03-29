from django.urls import path

from .views import index, BbByRubricView, BbCreateView, BbDetailView

urlpatterns = [
    path('detail/<int:pk>/', BbDetailView.as_view(), name='detail'),
    # URL параметр в <>, int - целочисленный тип параметра
    # rubric id — имя параметра контроллера, которому будет присвоено значение этого URL параметра
    # параметризованный параметр
    path('<int:rubric_id>/', BbByRubricView.as_view(), name='by_rubric'),
    # path('<int:rubric_id>/', by_rubric, name='by_rubric'),
    path('', index, name='index'),
    path('add/', BbCreateView.as_view(), name='add'),
]
