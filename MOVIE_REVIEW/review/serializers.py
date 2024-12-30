from rest_framework import serializers
from .models import Movie,Review,Like,Comment

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '_all_'
#handling 400 errors(invalid input)
    def validate_rating(self, value): # custom validation error and messages
        if value < 0 or value > 5:
            raise serializers.ValidationError("Rating must be between 0 and 5.")
        return value


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '_all_'

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '_all_'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '_all_'