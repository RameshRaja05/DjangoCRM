from django.contrib.auth.mixins import AccessMixin
from django.urls import reverse
from django.shortcuts import redirect

class OrganisorAndLoginRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated. and is an organiser"""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_organisor:
            return redirect(reverse('leads:lead-list'))
        return super().dispatch(request, *args, **kwargs)