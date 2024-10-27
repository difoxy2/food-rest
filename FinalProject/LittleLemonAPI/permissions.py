from rest_framework import permissions

class IsManager(permissions.BasePermission):
    message = 'Request sender is not Manager'
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True        
        if request.user.groups.filter(name='Manager').exists():
            return True
    #def has_object_permission(self, request, view, obj):

class IsCustomer(permissions.BasePermission):
    message = 'Request sender is not Customer'
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True        
        if (not request.user.groups.exists()):
            return True
    #def has_object_permission(self, request, view, obj):

class IsDeliverycrew(permissions.BasePermission):
    message = 'Request sender is not Deliverycrew'
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True        
        if request.user.groups.filter(name='Deliverycrew').exists():
            return True
    #def has_object_permission(self, request, view, obj):
        