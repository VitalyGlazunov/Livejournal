from django.utils import timezone

from users.models import Profile


class SubscriptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        users_to_update = Profile.objects.filter(status='User VIP', vip_status_expiry__isnull=False)
        for profile in users_to_update:
            if profile.vip_status_expiry < timezone.now():
                profile.status = 'User'
                profile.vip_status_expiry = None
                profile.save()
        response = self.get_response(request)
        return response
