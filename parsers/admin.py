from django.contrib import admin

from parsers.models import (
    Parser, Browser, TranslateParser, Language, Page, 
    Captcha, Block, TranslateImageParser, ParserSettings,
)
from preferences.admin import PreferencesAdmin


@admin.register(ParserSettings)
class ParserSettingsAdmin(PreferencesAdmin):
    pass


class LanguageInline(admin.StackedInline):
    model = Language
    extra = 0


class CaptchaInline(admin.StackedInline):
    model = Captcha
    extra = 0


class BlockInline(admin.StackedInline):
    model = Block
    extra = 0


@admin.register(Parser)
class ParserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'parser_name',
    )
    inlines = (BlockInline, CaptchaInline, LanguageInline)

    def parser_name(self, obj):
        return str(obj)


@admin.register(Browser)
class BrowserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'wsEndpoint',
    )


@admin.register(TranslateParser)
class TranslateParserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
    )


@admin.register(TranslateImageParser)
class TranslateImageParserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
    )


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = (
        'index',
        'parser',
        'updated',
        'created',
    )
