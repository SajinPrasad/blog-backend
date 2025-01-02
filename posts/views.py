from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework.response import Response

from .serializers import PostSerializer
from .models import Post
from .permissions import PostOwnerOnly

# Create your views here.


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def post_create_view(request):
    serializer = PostSerializer(data=request.data, context={"request": request})

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([AllowAny])
def post_list_view(request):
    """Posts are listed all users"""
    posts = Post.objects.all()
    serialized_data = PostSerializer(posts, many=True, context={"request": request})

    return Response(serialized_data.data, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([AllowAny])
def post_retrieve_view(request, id):
    """Posts can be retrieved by any users."""
    try:
        post = Post.objects.get(id=id)
        serialized_data = PostSerializer(post, context={"request": request})

        return Response(serialized_data.data, status=status.HTTP_200_OK)
    except Post.DoesNotExist:
        return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def post_delete_view(request, id):
    """
    View for deleting posts.
    - Only accessed by the post owners.
    """
    try:
        post = Post.objects.get(id=id)
        permission = PostOwnerOnly()  # Object level permission for checking ownership.
        if not permission.has_object_permission(request, None, post):
            return Response(
                {"detail": "You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN,
            )

        post.delete()

        return Response({"message": "Post deleted"}, status=status.HTTP_200_OK)
    except Post.DoesNotExist:
        return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def post_edit_view(request, id):
    """
    View for editing posts.
    - Only accessed by the post owners.
    """
    try:
        post = Post.objects.get(id=id)

        permission = PostOwnerOnly()  # Object level permission for checking ownership.
        if not permission.has_object_permission(request, None, post):
            return Response(
                {"detail": "You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = PostSerializer(
            instance=post, data=request.data, partial=True, context={"request": request}
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Post.DoesNotExist:
        return Response(
            {"detail": "Post not found."},
            status=status.HTTP_404_NOT_FOUND,
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_my_posts(request):
    """Listing the posts owned by a user"""
    try:
        posts = Post.objects.filter(user=request.user.id)
        serialized_data = PostSerializer(posts, many=True, context={"request": request})

        return Response(serialized_data.data, status=status.HTTP_200_OK)
    except Post.DoesNotExist:
        return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)
