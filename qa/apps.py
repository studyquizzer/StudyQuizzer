from django.apps import AppConfig


class QaConfig(AppConfig):
    name = "qa"

    def ready(self):
        import qa.signals
