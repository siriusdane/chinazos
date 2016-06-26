from WebPanel.serializers import ContextSerializer
import serpy


class PaginationSerializer(ContextSerializer):
    current = serpy.MethodField('get_current')
    next = serpy.MethodField('get_next')
    previous = serpy.MethodField('get_previous')
    results = serpy.MethodField('get_results')
    count = serpy.MethodField('get_count')

    def get_current(self, obj):
        return obj.number

    def get_next(self, obj):
        if obj.has_next():
            request = self.context.get('request')
            page = request.build_absolute_uri().split('?')
            return page[0] + '?page=' + str(obj.next_page_number())
        return None

    def get_previous(self, obj):
        if obj.has_previous():
            request = self.context.get('request')
            page = request.build_absolute_uri().split('?')
            return page[0] + '?page=' + str(obj.previous_page_number())
        return None

    def get_results(self, obj):
        serializer = self.context.get('serializer')
        return serializer(obj.object_list, many=True, context=self.context).data

    def get_count(self, obj):
        return obj.paginator.count
