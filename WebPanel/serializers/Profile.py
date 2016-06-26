import serpy


class SimpleProfileSerializer(serpy.Serializer):
    id = serpy.IntField()
    avatar = serpy.MethodField('get_avatar')
    display = serpy.StrField()

    def get_avatar(self, obj):
        return obj.avatar.url if obj.avatar else None
