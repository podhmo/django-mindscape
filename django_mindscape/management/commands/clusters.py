from django.core.management.base import BaseCommand
from . import ExcludeDjango, Formatter, get_model
from django_mindscape import get_mmprovider
from collections import OrderedDict
from optparse import make_option
import json


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option("-s", "--short", dest="short", action="store_true", default=False, help="using short format"),
    )

    def handle(self, *apps, **kwargs):
        mmprovider = get_mmprovider(brain=ExcludeDjango())
        formatter = Formatter(kwargs)
        D = OrderedDict()
        target_models = list(map(get_model, apps))
        if target_models:
            for model in target_models:
                for cluster in mmprovider.cluster_models:
                    if model in cluster:
                        D[model.__name__] = [formatter(m) for m in cluster]
        else:
            for cluster in mmprovider.cluster_models:
                D[cluster[0].__name__] = [formatter(m) for m in cluster]
        print(json.dumps(D, indent=2, ensure_ascii=False))
