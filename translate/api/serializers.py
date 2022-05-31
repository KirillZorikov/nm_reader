from ast import parse
import asyncio
from collections import OrderedDict

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.conf import settings

from parsers.models import (
    Parser, TranslateParser, Language, Captcha,
    Browser, Block, TranslateImageParser, Page,
)
from utils.browser import check_page_open
from translate.utils import run_async2


class LanguageSerializers(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = (
            'name', 'code',
        )


class LanguageFullSerializers(LanguageSerializers):
    class Meta(LanguageSerializers.Meta):
        fields = LanguageSerializers.Meta.fields + (
            'source', 'destination',
        )


class TranslateParserListSerializer(serializers.ModelSerializer):
    timeout = serializers.IntegerField(source='parser.timeout')
    max_pages = serializers.IntegerField(source='parser.max_pages_count')
    languages = LanguageSerializers(source='parser.language_set', many=True)

    class Meta:
        model = TranslateParser
        fields = (
            'slug', 'name', 'languages',
            'timeout', 'max_pages',
        )

    def to_representation(self, instance):
        parser_data = super().to_representation(instance)
        slug = instance.slug
        if not slug.endswith('_api'):
            return parser_data
        parser = TranslateParser.objects.filter(slug=slug[:-4]).first()
        data = super().to_representation(parser)
        parser_data['languages'] = data['languages']
        return parser_data


class TranslateParserDetailSerializer(serializers.ModelSerializer):
    languages = LanguageSerializers(source='language_set', many=True)

    class Meta:
        model = Parser
        fields = (
            'languages',
        )


class TranslateParserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TranslateParser
        fields = (
            'name',
            'url',
            'slug',
        )


class TranslateImageParserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TranslateImageParser
        fields = (
            'name',
            'url',
            'slug',
        )


class BlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Block
        fields = (
            'name',
            'css_selector',
        )


class CaptchaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Captcha
        exclude = ('id', 'parser')


class ParserSerializer(serializers.ModelSerializer):
    related_parser = serializers.SerializerMethodField()
    blocks = BlockSerializer(source='block_set', many=True)
    languages = LanguageFullSerializers(source='language_set', many=True)
    captcha_data = CaptchaSerializer(source='captcha_set', many=True)

    class Meta:
        model = Parser
        fields = (
            'type',
            'related_parser',
            'blocks',
            'languages',
            'captcha_data',
            'timeout',
            'max_pages_count',
        )

    def get_related_parser(self, obj):
        type_to_serializer = {
            TranslateParser: TranslateParserSerializer,
            TranslateImageParser: TranslateImageParserSerializer,

        }
        related_parser = obj.get_related_parser()
        return type_to_serializer[type(related_parser)](
            instance=related_parser
        ).data

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['blocks'] = {x['name']: x['css_selector'] for x in ret['blocks']}
        return ret


class TranslateSerializer(serializers.Serializer):
    src = serializers.CharField()
    dst = serializers.CharField()
    reload = serializers.BooleanField(required=False)
    page = serializers.IntegerField(required=False)

    def validate_page(self, value):
        slug = self.context['slug']
        page = Page.objects.annotate_parser_slug().filter(
            parser_slug=slug, index=value
        )
        if not page:
            raise ValidationError(
                f'wrong page {value} for the {slug} service '
                f'choose one from the /api/pages/status endpoint'
            )
        return value

    def validate(self, attrs):
        slug = self.context['slug']
        lang_list = [attrs['src'], attrs['dst']]
        count_obj = Language.objects.annotate_parser_slug().filter(
            code__in=lang_list, parser_slug=slug,
        ).count()
        if len(lang_list) != count_obj:
            raise ValidationError('wrong language code')
        return attrs

    def is_valid(self, raise_exception=False):
        result = super().is_valid(raise_exception)
        data = self.validated_data
        self.validated_data['data'] = (data.get('paragraphs') or
                                       data.get('image'))
        self.validated_data.pop('paragraphs') if 'paragraphs' in data else 0
        self.validated_data.pop('image') if 'image' in data else 0
        return result


class TextTranslateSerializer(TranslateSerializer):
    paragraphs = serializers.ListSerializer(child=serializers.CharField())

    def validate_paragraphs(self, value):
        text = '\n\n'.join(value)
        max_count = settings.TRANSLATE_MAX_CHARS_COUNT
        if len(text) > max_count:
            raise ValidationError(f'maximum number of characters '
                                  'reached: {max_count}')
        return value


class ImageTranslateSerializer(TranslateSerializer):
    image = serializers.ImageField()


class YandexCaptchaSerializer(serializers.Serializer):
    page_index = serializers.IntegerField()
    browser_id = serializers.IntegerField()
    service_slug = serializers.CharField()
    solution = serializers.CharField()

    def validate(self, attrs):
        browser = Browser.objects.filter(pk=attrs['browser_id']).first()
        if not browser:
            raise ValidationError('wrong browser_id')
        parser = Parser.objects.annotate_related_parser_slug().filter(
            related_parser_slug=attrs['service_slug']
        ).first()
        if not parser:
            raise ValidationError('wrong service_slug')
        related_parser = parser.get_related_parser()
        page_open = asyncio.run(run_async2(
            check_page_open,
            page_index=attrs['page_index'], endpoint=browser.wsEndpoint,
            service_url=related_parser.url, yandex_captcha_check=True
        ))
        if not page_open:
            raise ValidationError('wrong page_index')
        return attrs
