from django.core.management.base import BaseCommand
from . import ExcludeDjango, Formatter, get_model
from django_mindscape import get_mmprovider
from collections import OrderedDict
from optparse import make_option
import json


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option("--label", dest="label", action="store_true", default=False, help="describe by label"),
    )

    def to_dict(self, formatter, dependencies, m, use_label=False):
        history = {}   # model -> dependencies.

        def rec(node, D):
            if node.model in history:
                return history[node.model].copy()
            history[node.model] = D
            if use_label:
                D["model"] = node.model._meta.verbose_name
            else:
                D["model"] = formatter(node.model)
            if node.dependencies:
                if use_label:
                    D["parents"] = {getattr(node.model, rel.name).field.verbose_name: rec(rel.to, OrderedDict()) for rel in node.dependencies}
                else:
                    D["parents"] = {rel.name: rec(rel.to, OrderedDict()) for rel in node.dependencies}
            return D
        return rec(dependencies[m], OrderedDict())

    def handle(self, *apps, **kwargs):
        mmprovider = get_mmprovider(brain=ExcludeDjango())
        formatter = Formatter(kwargs)
        r = []
        dependencies = mmprovider.dependencies
        target_models = list(map(get_model, apps))
        if target_models:
            for m in target_models:
                if m is not None:
                    r.append(self.to_dict(formatter, dependencies, m, use_label=kwargs.get("label")))
        else:
            for m in dependencies.keys():
                r.append(self.to_dict(formatter, dependencies, m, use_label=kwargs.get("label")))
        print(json.dumps(r, indent=2, ensure_ascii=False))
