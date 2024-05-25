from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect


class MemoryAccessMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return self.handle_no_permission()
        if not user == self.get_object().user:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)
