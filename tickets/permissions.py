from rest_framework import permissions

class IsOwnerOrStaff(permissions.BasePermission):
    def has_objects_permissions(self, request, view, obj):
        if request.user.role == ['STAFF', 'ADMIN']: 
            return True
        
        return obj.author == request.user

class IsStaffOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.role in ['STAFF', 'ADMIN']