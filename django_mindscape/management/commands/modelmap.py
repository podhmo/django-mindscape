from django.core.management.base import BaseCommand
from . import ExcludeDjango, Formatter, get_model
from django.apps import apps as registry
from django_mindscape import ModelMapProvider, BidirectionalWalker
from collections import OrderedDict
from optparse import make_option
import json


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option("-s", "--short", dest="short", action="store_true", default=False, help="using short format"),
        make_option("--label", dest="label", action="store_true", default=False, help="describe by label"),
    )

    def to_dict(self, formatter, mmprovider, m, use_label=False):
        r = OrderedDict()
        r["11"] = OrderedDict()
        r["1M"] = OrderedDict()
        r["M1"] = OrderedDict()
        r["MM"] = OrderedDict()
        for rel in sorted(mmprovider.dependencies[m].dependencies, key=lambda rel: rel.name):
            r[rel.type][rel.name] = formatter(rel.to.model)
        return r

    def handle(self, *apps, **kwargs):
        formatter = Formatter(kwargs)
        r = OrderedDict()
        target_models = list(map(get_model, apps))
        mmprovider = ModelMapProvider(BidirectionalWalker(registry.get_models(), brain=ExcludeDjango()))
        if target_models:
            target_models = [m for m in target_models if m]
            for m in target_models:
                r[formatter(m)] = self.to_dict(formatter, mmprovider, m)
        else:
            target_models = registry.get_models()
            for m in sorted(mmprovider.dependencies.keys(), key=lambda m: m.__name__):
                r[formatter(m)] = self.to_dict(formatter, mmprovider, m)
        print(json.dumps(r, indent=2, ensure_ascii=False))
