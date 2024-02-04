from rest_framework import permissions


class IsSuperUser(permissions.BasePermission):
    """ "システム開発者か判別する為のクラス"""

    def has_permission(self, request, view):
        """権限の有無を確認する

        Args:
            request (Request):
            view (Callable):

        Returns:
            bool
        """

        return request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        """対象のオブジェクトに対して権限の有無を確認する

        Args:
            request (Request):
            view (Callable):
            obj (Model):

        Returns:
            bool
        """

        return request.user.is_superuser


class IsAdminUser(permissions.BasePermission):
    """ "管理者か判別する為のクラス"""

    def has_permission(self, request, view):
        """権限の有無を確認する

        Args:
            request (Request):
            view (Callable):

        Returns:
            bool
        """

        if request.user.is_superuser:
            return True
        elif request.user.is_authenticated:
            return request.user.groups.name == "管理者"
        else:
            return False

    def has_object_permission(self, request, view, obj):
        """対象のオブジェクトに対して権限の有無を確認する

        Args:
            request (Request):
            view (Callable):
            obj (Model):

        Returns:
            bool
        """

        if request.user.is_superuser:
            return True
        elif request.user.is_authenticated:
            return request.user.groups.name == "管理者"
        else:
            return False
