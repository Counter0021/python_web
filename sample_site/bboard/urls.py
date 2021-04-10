from django.urls import path, include

from .views import BbIndexView, BbByRubricView, BbAddView, BbDetailView, BbEditView, BbDeleteView, BbRedirectView, \
    rubrics, bbs, formset_processing, add_image, delete_image, api_rubrics, api_rubric_detail, APIRubrics, \
    APIRubricDetail, APIRubricList, APIRubricViewSet

from rest_framework.routers import DefaultRouter

# Маршруты метаконтроллера APIRubricViewSet
router = DefaultRouter()
router.register('rubrics', APIRubricViewSet)

# get

urlpatterns = [
    path('delete_image/<int:pk>/', delete_image, name='delete_image'),
    path('add_image/', add_image, name='add_image'),
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
    path('form/', formset_processing, name='form'),
    # path('get/<path:filename>', get, name='get'),
    path('api/rubrics/', api_rubrics),
    path('api/rubrics/<int:pk>/', api_rubric_detail),
    path('api/rubrics_class/', APIRubrics.as_view()),
    path('api/rubrics_class/<int:pk>/', APIRubricDetail.as_view()),
    path('api/rubrics_class_get/', APIRubricList.as_view()),
    # Список маршрутов метаконтроллера
    path('api/meta_controller/', include(router.urls)),
]
