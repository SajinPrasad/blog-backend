from rest_framework.serializers import (
    ModelSerializer,
    ImageField,
    SerializerMethodField,
)
from rest_framework.exceptions import ValidationError
from PIL import Image

from .models import Post


class PostSerializer(ModelSerializer):
    image = ImageField(required=False)
    author = SerializerMethodField(read_only=True)

    class Meta:
        model = Post
        fields = ["id", "title", "description", "image", "user", "author"]
        extra_kwargs = {"user": {"read_only": True}}

    def to_representation(self, instance):
        """Including the full url with the image."""
        data = super().to_representation(instance)
        request = self.context.get("request")
        if instance.image and request:
            data["image"] = request.build_absolute_uri(instance.image.url)
        return data

    def get_author(self, obj):
        """Returning the full name of author"""
        return obj.user.get_full_name()

    def validate_image(self, image):
        try:
            img = Image.open(image)
            img.verify()

            # Allowed image formats.
            if img.format not in ["JPEG", "PNG", "GIF"]:
                raise ValidationError(
                    "Only JPEG, PNG, and GIF image formats are supported."
                )

        except Exception as e:
            raise ValidationError("Unsupported image")

        # Maximum allowed image size
        max_size_mb = 5
        if image.size > max_size_mb * 1024 * 1024:
            raise ValidationError(f"Image size exceeds {max_size_mb} MB.")

        return image

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)
