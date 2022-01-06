from rest_framework import permissions

class ISAUthorOrReadOnly(permissions.BasePermission):
    """Запрещает изменять или удалять чужой контент."""

    def has_permission(self, request, view):
        return(
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user)

class IsFollowerOrReadOnly(permissions.BasePermission):
    """Запрещает управлять чужими подписками."""

    def has_permission(self, request, view):
        return (request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (obj.user == request.user)