from rest_framework import serializers
from administration.models import Article, CarouselImage

from users.serializers import UserSerializer

class ArticleSerializer(serializers.ModelSerializer):
	created_by = serializers.SerializerMethodField(read_only=True)
	#created_at = serializers.SerializerMethodField(read_only=True)
	short_content = serializers.SerializerMethodField(read_only=True)

	class Meta:
		model = Article
		fields = ['id', 'title', 'content', 'short_content', 'picture', 'created_at', 'created_by']

	def get_created_by(self, obj):
		user = obj.created_by
		serializer = UserSerializer(user, many=False)
		if(serializer.data['first_name']):
			return serializer.data['first_name']
		return serializer.data['email']

	def get_short_content(self, obj):
		content = obj.content
		return content[:200]

class CarouselImageSerializer(serializers.ModelSerializer):
	class Meta:
		model = CarouselImage
		fields = ['id', 'title', 'description', 'picture']

