"""
Django settings for DjangoTest project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '70&bp3kt!*8=0hx7m$otn=mqw5c@6btpo+$d0%vo%0p20ui-n+'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['*']
'''
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []
'''

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'networkmeasurement', #liaohui,add app that we create
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware', #if we delete this line,we can get post action from jquery 
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'DjangoTest.urls'

WSGI_APPLICATION = 'DjangoTest.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }
##altered by liaohui
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'network',
        'USER': 'root',
        'PASSWORD':'root',
        'HOST':'127.0.0.1',
        'PORT':3306,
    }
}

######end333333333333333333333

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

#LANGUAGE_CODE = 'en-us' #liaohui
LANGUAGE_CODE = 'zh-cn' #liaohui

#TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Shanghai' #BY LIAOHUI,it means UTC+8

USE_I18N = True

USE_L10N = True

#USE_TZ = True 
USE_TZ = False ##by liaohui to deal with timezone problem
#if we don't change this,we must use datetime.datetime.now().replace(tzinfo = utc) to insert into database,otherwise datetime in db my lay off 8 hours

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
#LIAOHUI
BASE_DIR = os.path.dirname(os.path.dirname(__file__)) #get project base dir
print BASE_DIR
STATIC_PATH = os.path.join(BASE_DIR, 'networkmeasurement/templates/assets').replace('\\','/')
print STATIC_PATH
# STATICFILES_DIRS = (
#     ('css',os.path.join(STATIC_PATH,'css').replace('\\','/') ),  
#     ('js',os.path.join(STATIC_PATH,'js').replace('\\','/') ), 
#     ('images',os.path.join(STATIC_PATH,'images').replace('\\','/') ), 
#     ('upload',os.path.join(STATIC_PATH,'upload').replace('\\','/') ), 
# )
#liaohui