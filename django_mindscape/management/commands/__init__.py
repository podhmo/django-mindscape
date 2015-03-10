from django_mindscape import Brain
from importlib import import_module


class ExcludeDjango(Brain):
    def is_skip(self, model):
        return super(ExcludeDjango, self).is_skip(model) or model.__module__.startswith("django.")


class Formatter(object):
    def __init__(self, options):
        self.options = options

    def short(self, m):
        return m.__name__

    def long(self, m):
        return "{}.{}".format(m.__module__, m.__name__)

    def __call__(self, m):
        if self.options.get("short"):
            return self.short(m)
        else:
            return self.long(m)


def get_model(modelpath):
    module, name = modelpath.rsplit(".", 1)
    try:
        return getattr(import_module(module), name, None)
    except ImportError:
        return None
