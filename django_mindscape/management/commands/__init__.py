from django_mindscape import Brain


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
