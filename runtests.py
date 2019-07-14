#!/usr/bin/env python
import django
import logging
import os
import sys

from django.conf import settings
from django.test.runner import DiscoverRunner
from edc_test_utils import DefaultTestSettings
from os.path import abspath, dirname


app_name = 'edc_action_item'
base_dir = dirname(abspath(__file__))

DEFAULT_SETTINGS = DefaultTestSettings(
    calling_file=__file__,
    BASE_DIR=base_dir,
    APP_NAME=app_name,
    ETC_DIR=os.path.join(base_dir, app_name, "tests", "etc"),
    INSTALLED_APPS=[
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
        "django.contrib.sites",
        "django_crypto_fields.apps.AppConfig",
        "django_revision.apps.AppConfig",
        "django_collect_offline.apps.AppConfig",
        "django_collect_offline_files.apps.AppConfig",
        "rest_framework",
        "rest_framework.authtoken",
        "simple_history",
        "edc_auth.apps.AppConfig",
        "edc_protocol.apps.AppConfig",
        "edc_identifier.apps.AppConfig",
        "edc_device.apps.AppConfig",
        "edc_notification.apps.AppConfig",
        "edc_registration.apps.AppConfig",
        "edc_visit_schedule.apps.AppConfig",
        "edc_action_item.apps.AppConfig",
    ],
    add_dashboard_middleware=True,
    use_test_urls=True,
).settings


# if DEFAULT_SETTINGS.get('EMAIL_ENABLED'):
#     DEFAULT_SETTINGS.update(
#         EMAIL_HOST=env.str("DJANGO_EMAIL_HOST"),
#         EMAIL_PORT=env.int("DJANGO_EMAIL_PORT"),
#         EMAIL_HOST_USER=env.str("DJANGO_EMAIL_HOST_USER"),
#         EMAIL_HOST_PASSWORD=env.str("DJANGO_EMAIL_HOST_PASSWORD"),
#         EMAIL_USE_TLS=env("DJANGO_EMAIL_USE_TLS"),
#         MAILGUN_API_KEY=env("MAILGUN_API_KEY"),
#         MAILGUN_API_URL=env("MAILGUN_API_URL"),
#     )


def main():
    if not settings.configured:
        settings.configure(**DEFAULT_SETTINGS)
    django.setup()
    tags = [t.split('=')[1] for t in sys.argv if t.startswith('--tag')]
    failures = DiscoverRunner(failfast=False, tags=tags).run_tests(
        [f'{app_name}.tests'])
    sys.exit(failures)


if __name__ == "__main__":
    logging.basicConfig()
    main()
