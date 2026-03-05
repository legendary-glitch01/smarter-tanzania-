from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Profile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, registration_method='email')
    else:
        # Ensure profile exists even if signal didn't fire on creation
        if not hasattr(instance, 'profile') or instance.profile is None:
            try:
                Profile.objects.get(user=instance)
            except Profile.DoesNotExist:
                Profile.objects.create(user=instance, registration_method='email')