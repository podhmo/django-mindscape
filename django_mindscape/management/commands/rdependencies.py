from django.core.management.base import BaseCommand
from . import ExcludeDjango, Formatter
from django_mindscape import get_mmprovider
from collections import OrderedDict
from optparse import make_option
import json


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option("-s", "--short", dest="short", action="store_true", default=False, help="using short format"),
        make_option("--label", dest="label", action="store_true", default=False, help="describe by label"),
    )

    def to_dict(self, rwalker, formatter, rnode, use_label=False):
        history = {}   # model -> dependencies.

        def rec(rnode, D):
            if rnode.node.model in history:
                return history[rnode.node.model].copy()
            history[rnode.node.model] = D
            D["model"] = formatter(rnode.node.model)
            if rnode.dependencies:
                D["children"] = {rwalker.relname_map[(rnode, sub)]: rec(sub, OrderedDict()) for sub in rnode.dependencies}
            return D
        return rec(rnode, OrderedDict())

    def handle(self, *apps, **kwargs):
        mmprovider = get_mmprovider(brain=ExcludeDjango())
        formatter = Formatter(kwargs)
        r = []
        mmprovider.rwalker.walkall()
        for rnode in mmprovider.rwalker.toplevel:
            r.append(self.to_dict(mmprovider.rwalker, formatter, rnode, use_label=kwargs.get("label")))
        print(json.dumps(r, indent=2, ensure_ascii=False))
