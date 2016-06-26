from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class Bunch:
    def __init__(self, values):
        self.__dict__.update(**values)


def enum(**enums):
    return type('Enum', (), enums)


def enum_name(enumerator, value):
    for choice in enumerator:
        if value == choice[0]:
            return choice[1]
    raise ValueError


def paginate_results(query, serializer, context, page=1, size=10):
    from WebPanel.serializers import PaginationSerializer
    paginator = Paginator(query, size)
    try:
        results = paginator.page(page)
    except PageNotAnInteger:
        results = paginator.page(1)
    except EmptyPage:
        results = paginator.page(paginator.num_pages)
    context.update({'serializer': serializer})
    return PaginationSerializer(instance=results, context=context).data
