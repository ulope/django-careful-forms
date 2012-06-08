DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

ROOT_URLCONF = 'careful_forms.tests.urls'

MIDDLEWARE_CLASSES = (
    'careful_forms.middleware.CarefulFormsMiddleware',
)

CAREFUL_ENABLED = True

INSTALLED_APPS = (
    'careful_forms.tests',
)

TEST_RUNNER = 'discover_runner.DiscoverRunner'
