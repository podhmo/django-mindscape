from django_mindscape import Brain
from importlib import import_module


class ExcludeDjango(Brain):
    def is_skip(self, model):
        return super(ExcludeDjango, self).is_skip(model) or model.__module__.startswith("django.")


class BaseFormatter(object):
    def tablename(self, m):
        return m._meta.db_table

    def modelname(self, m):
        return self.__call__(m)


class LabelFormatter(BaseFormatter):
    def __call__(self, m):
        return getattr(m._meta, "verbose_name", m.__name__)


class DefaultFormatter(BaseFormatter):
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


def Formatter(options):
    if options.get("label"):
        return LabelFormatter()
    else:
        return DefaultFormatter(options)


def get_model(modelpath):
    module, name = modelpath.rsplit(".", 1)
    try:
        return getattr(import_module(module), name, None)
    except ImportError:
        return None
