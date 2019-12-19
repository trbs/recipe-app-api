from rest_framework.decorators import action
from rest_framework.response import Response

from rest_framework import viewsets, mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag, Ingredient, Recipe

from recipe import serializers

from django.shortcuts import render, get_object_or_404

from django.core.paginator import Paginator


class BaseRecipeAttrViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin):
	#Base viewset for user owned attributes
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)

	def get_queryset(self):
		#Return objects for the current authenticated user only
		assigned_only = bool(
			int(self.request.query_params.get('assigned_only',0)))
		queryset= self.queryset
		if assigned_only:
			queryset = queryset.filter(recipe__isnull=False)
		
		return queryset.filter(user=self.request.user).order_by('-name').distinct()

	def perform_create(self, serializer):
		#Create a new tag/ingredient
		serializer.save(user=self.request.user)


class TagViewSet(BaseRecipeAttrViewSet):
	"""Manage tags in the database"""
	queryset = Tag.objects.all()
	serializer_class = serializers.TagSerializer


class IngredientViewSet(BaseRecipeAttrViewSet):
	#Manage ingredients in the database
	queryset = Ingredient.objects.all()
	serializer_class = serializers.IngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet):
	#Manage the recipes
	serializer_class = serializers.RecipeSerializer
	queryset = Recipe.objects.all()

	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)

	def _params_to_ints(self, qs):
		#convert a string of IDs to a list of integers
		return [float(str_id) for str_id in qs.split(',')]
	def get_queryset(self):
		tags = self.request.query_params.get('tags')
		ingredients = self.request.query_params.get('ingredients')
		queryset = self.queryset
		if tags:
			tag_ids = self._params_to_ints(tags)
			queryset = queryset.filter(tags__id__in=tag_ids)

		if ingredients:
			ingredient_ids = self._params_to_ints(ingredients)
			queryset = queryset.filter(ingredients__id__in=ingredient_ids)
		return queryset.filter(user=self.request.user)

	def get_serializer_class(self):
		#Return serializer class for detail
		if self.action == 'retrieve':
			return serializers.RecipeDetailSerializer
		elif self.action == 'upload_image':
			return serializers.RecipeImageSerializer
		
		return serializers.RecipeSerializer

	def perform_create(self, serializer):
		#Create a new Recipe
		serializer.save(user=self.request.user)

	@action(methods=['POST'], detail=True, url_path='upload_image')
	def upload_image(self, request, pk=None):
	#Upload an image to a recipe
		recipe = self.get_object()
		serializer = self.get_serializer(
			recipe,
			data=request.data
		)

		if serializer.is_valid():
			serializer.save()
			return Response(
				serializer.data,
				status=status.HTTP_200_OK
			)

		return Response(
			serializer.errors,
			status=status.HTTP_400_BAD_REQUEST
		)

def detail(request,recipe_id):
	recipe = get_object_or_404(Recipe, pk=recipe_id)
	return render(request, 'recipe/detail.html', {'recipe':recipe})

def all_recipes(request):
	recipe=Recipe.objects.all()
	tag=Tag.objects

	paginator = Paginator(recipe, 3)
	page = request.GET.get('page',1)
	recipe = paginator.get_page(page)

	return render(request, 'recipe/all_recipes.html',{'recipes':recipe, 'tags':tag})

