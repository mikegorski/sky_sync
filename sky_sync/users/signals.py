from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import User, Dashboard


@receiver(post_save, sender=User)
def create_dashboard(sender, instance, created, **kwargs):
    """
    Signal handler to create a Dashboard instance for a newly created User.

    Args:
        sender (User): The User model class.
        instance (User): The newly created User instance.
        created (bool): Indicates if the User instance was just created.

    """
    if created:
        Dashboard.objects.create(user=instance)
