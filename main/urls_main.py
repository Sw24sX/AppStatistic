from django.urls import path
from .views import MainViews


urlpatterns = [
    path('app/statistic/', MainViews.Reviews.as_view()),
    path('search/', MainViews.SearchApps.as_view()),
    path('search/app_store/', MainViews.FindAppInAppStore.as_view()),
]
