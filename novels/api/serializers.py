from rest_framework import serializers

from parsers.models import SiteLanguage, NovelParser, Resource, Block
# from parsers.api.serializers import BlockSerializer


class BlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Block
        fields = (
            'name',
            'css_selector',
            'exclude_tags',
        )


class NovelServiceSerializer(serializers.ModelSerializer):
    code = serializers.CharField(
        source='parser.sitelanguage_set.all.main.code')

    class Meta:
        model = NovelParser
        fields = ('name', 'url', 'slug', 'icon', 'code')


class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ('urn', 'name', 'description')


class ResourceFullSerializer(ResourceSerializer):
    blocks = BlockSerializer(source='block_set', many=True)
    # url = serializers.CharField(source='novel_parser.url')

    class Meta(ResourceSerializer.Meta):
        fields = ResourceSerializer.Meta.fields + (
            'blocks', 'intercept_page_res',
        )

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['blocks'] = {x['name']: {
            'selector': x['css_selector'],
            'exclude': x['exclude_tags'],
        } for x in ret['blocks']}
        return ret


class SearchPageSerializer(ResourceFullSerializer):
    search_query_param = serializers.CharField(
        source='novel_parser.parser.search.search_query_param'
    )
    use_POST = serializers.BooleanField(
        source='novel_parser.parser.search.use_POST'
    )
    encoding = serializers.BooleanField(
        source='novel_parser.parser.search.encoding'
    )

    class Meta(ResourceFullSerializer.Meta):
        fields = ResourceFullSerializer.Meta.fields + (
            'search_query_param', 'use_POST', 'encoding'
        )


class ResourceFromUrlIncomeSerializer(serializers.Serializer):
    url = serializers.CharField()


class SearchIncomeSerializer(serializers.Serializer):
    keywords = serializers.CharField()


class AuthorIncomeSerializer(serializers.Serializer):
    data = serializers.CharField()


class TitleIncomeSerializer(serializers.Serializer):
    data = serializers.CharField()


class ChapterIncomeSerializer(serializers.Serializer):
    novel_id = serializers.CharField()
    chapter_id = serializers.CharField()
    page_num = serializers.CharField(required=False)