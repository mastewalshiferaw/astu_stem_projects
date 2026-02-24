from rest_framework import permissions

class IsOwnerOrStaff(permissions.BasePermission):
    def has_objects_permissions(self, request, view, obj):
        if request.user.role == ['STAFF', 'ADMIN']: 
            return True
        
        return obj.author == request.user