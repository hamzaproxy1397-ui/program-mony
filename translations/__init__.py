# -*- coding: utf-8 -*-
"""
نظام الترجمة والتعريب
Translation and Localization System
"""

from .translation_manager import (
    TranslationManager,
    translation_manager,
    _,
    set_language,
    get_current_language,
    is_rtl,
    get_available_languages,
    get_language_name
)

__all__ = [
    'TranslationManager',
    'translation_manager',
    '_',
    'set_language',
    'get_current_language',
    'is_rtl',
    'get_available_languages',
    'get_language_name'
]
