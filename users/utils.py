import random
import string

from django.conf import settings
from django.core.mail import send_mail
from django.utils.text import slugify

"""
random_string_generator is located here:
http://joincfe.com/blog/random-string-generator-in-python/
"""
# from yourapp.utils import random_string_generator


def random_string_generator(
    size=10, chars=string.ascii_lowercase + string.digits
):
    return "".join(random.choice(chars) for _ in range(size))


def unique_slug_generator(instance, new_slug=None):
    """
    This is for a Django project and it assumes your instance
    has a model with a slug field and a title character (char) field.
    """
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
            slug=slug, randstr=random_string_generator(size=4)
        )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug


def sendemail(user_email, username):
    subject = "Thank you for registering to our site"
    message = f"""Dear {username},

             Thanks for registering on our site, it means a world to us.

             We welcome you to the crackerbox platform where we help you study seamlessly with our out of the box
             artificial intelligent examiner, grammar buster and many more tools at your fingertips.

             We wish you a great study time on our site."""
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [
        user_email,
    ]
    send_mail(subject, message, email_from, recipient_list)
