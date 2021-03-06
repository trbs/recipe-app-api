"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
import user.views, recipe.views, frontend.views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', include('user.urls')),
    path('api/recipe/', include('recipe.urls')),
    path('api/token',TokenObtainPairView.as_view()),
    path('api/token/refresh',TokenRefreshView.as_view()),
    path('index/',include('frontend.urls')),
    path('', user.views.home, name='home'),
    path('all_recipes/', recipe.views.all_recipes, name="all_recipes"),
    path('all_recipes/<int:recipe_id>/', recipe.views.detail, name='detail'),
    path('create_recipe/', recipe.views.create_recipe, name="create_recipe"),
    path('add_ingredients/',user.views.AddIngredientView.as_view(),name="add_ingredients"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
