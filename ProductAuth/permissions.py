from rest_framework.permissions import BasePermission

from rest_framework.permissions import BasePermission

class IsAdminorSuperuser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.role == 'Admin' or request.user.role == 'Superuser')

# class IsSuperuser(BasePermission):
#     def has_permission(self, request, view):
#         return request.user.is_authenticated and request.user.role == 'Superuser'

class IsStaff(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'Staff'

class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'Customer'


# # Custom Permission Classes
# class IsAdmin(BasePermission):
#     def has_permission(self, request, view):
#         return request.user.role == 'Admin'

# class IsSuperuser(BasePermission):
#     def has_permission(self, request, view):
#         return request.user.role == 'Superuser'

# class IsCustomer(BasePermission):
#     def has_permission(self, request, view):
#         return request.user.role == 'Customer'

# class IsStaff(BasePermission):
#     def has_permission(self, request, view):
#         return request.user.role == 'Staff'





# class IsAdminOrSuperuser(BasePermission):
#     def has_permission(self, request, view):
#         return request.user.is_superuser 

# class IsAdminOrSuperuser(permissions.BasePermission):
#     def has_permission(self, request, view):
#         # if not request.user.is_authenticated:
#         #     return False

#         # if request.method in permissions.SAFE_METHODS:
#         #     return True

#         if request.user.role in ['Admin', 'Superuser']:
#             print("request.user.role",request.user.role)
#             return True
#         else:
#             return False
# class admin(BasePermission):
#     def has_permission(self, request, view):
#         if request.user.role in ['Admin','']
