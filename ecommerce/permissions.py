from rest_framework import permissions


# ! Custom Permission 
class IsObjectUserOrAdminUserElseReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        """
        Over riding this permissions for whole view
        where anyone can access safe methods but only
        authenticated user can access other methods
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        return  bool(request.user.is_authenticated)
    

    def has_object_permission(self, request, view, obj):
        """
        Over Riding the permissions for a object 
        so that only the user who created the object
        and admin users can perform other methods on it
        """
        if request.method in permissions.SAFE_METHODS:
            return True 
        
        return bool(
            obj.user==request.user or
            request.user.is_staff or
            request.user.is_superuser
        )