from .base import *   # 引入base中的所有配置

DEBUG = True      # 开发环境
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}