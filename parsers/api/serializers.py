from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from parsers.models import Parser, Page
from utils.browser import check_pages_created


class InitPagesSerializer(serializers.Serializer):
    service_slug = serializers.CharField()
    pages_count = serializers.IntegerField(required=False)

    def validate(self, attrs):
        parser = Parser.objects.annotate_related_parser_slug().filter(
            related_parser_slug=attrs['service_slug']
        ).first()
        if not parser:
            raise ValidationError('wrong service_slug')
        check, diff = check_pages_created(parser, attrs['service_slug'])
        if check:
            attrs.update({'inited': True})
        attrs.update({'diff': diff})
        attrs.update({'type': parser.type})
        return attrs


class ServiceMaxPagesSerializer(serializers.Serializer):
    service_slug = serializers.CharField()
    pages_count = serializers.IntegerField()


class ServiceTimeoutSerializer(serializers.Serializer):
    service_slug = serializers.CharField()
    timeout = serializers.IntegerField()
