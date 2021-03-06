django-mindscape
========================================

- (todo: gentle introduction)
- (todo: add information about use case)

features
----------------------------------------

- collecting information about dependencies of models (model -> parent)
- collecting information about reverse dependencies of models (model -> [children])
- listing model with dependencies-considered order.

(`dependencies-considered order` means, when i < j, models[i] doesn't depends on models[j])

how to use
----------------------------------------

.. code-block:: python

    from django_mindscape import ModelMapProvider, Walker, Brain
    from django.apps import apps

    walker = Walker(apps.get_models(), brain=Brain())
    p = ModelMapProvider(walker)

    """
    when ParentModel : YourModel = 1 : N
    and OtherModel is existed.
    """

    # model dependencies (bottom up)
    for relation in p.dependencies[YourModel].dependencies:
        print(relation.from_.model)  # <YourModel>
        print(relation.to.model)  # <ParentModel>
        print(relation.type)  # relation type (candidates: 11, 1M, MM)

    # reverse dependencies (top down)
    for rnode in p.reverse_dependencies[ParentModel].dependencies:
        print(rnode.node.model)  # <YourModel>

    # clustered model list
    for cluster in p.cluster_models:  # [[ParentModel, YourModel], [OtherModel]]
        for model in cluster:
            print(model)

    # ordered model list
    for model in p.ordered_models:  # [ParentModel, YourModel, OtherModel]
        print(model)

