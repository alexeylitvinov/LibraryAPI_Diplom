from rest_framework.permissions import BasePermission


class IsLibrarian(BasePermission):
    """ Установка прав для библиотекаря """
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.groups.filter(name='librarian').exists()
        return False
