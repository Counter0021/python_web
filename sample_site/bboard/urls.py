from django.urls import path

from .views import BbIndexView, BbByRubricView, BbAddView, BbDetailView, BbEditView, BbDeleteView, BbRedirectView, \
    rubrics, bbs

urlpatterns = [
    path('detail/<int:pk>/', BbDetailView.as_view(), name='detail'),
    path('detail/<int:year>/<int:month>/<int:day>/<int:pk>/', BbRedirectView.as_view(), name='old_detail'),
    # URL параметр в <>, int - целочисленный тип параметра
    # rubric id — имя параметра контроллера, которому будет присвоено значение этого URL параметра
    # параметризованный параметр
    path('<int:rubric_id>/', BbByRubricView.as_view(), name='by_rubric'),
    # path('<int:rubric_id>/', by_rubric, name='by_rubric'),
    path('', BbIndexView.as_view(), name='index'),
    path('add/', BbAddView.as_view(), name='add'),
    path('update/<int:pk>/', BbEditView.as_view(), name='update'),
    path('delete/<int:pk>/', BbDeleteView.as_view(), name='delete'),
    path('add_form/', rubrics, name='add_form'),
    path('bbs/<int:rubric_id>', bbs, name='bbs'),
]
