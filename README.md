django-oss-storage
==================

django storage backend for aliyun oss

Install
-------

settings
--------
`DEFAULT_FILE_STORAGE` or `STATICFILES_STORAGE` should be set:
```Python
DEFAULT_FILE_STORAGE = 'storages.backends.aliyun_oss.OssStorage'
STATICFILES_STORAGE = 'storages.backends.aliyun_oss.OssStorage'
```
when using oss as your storage backend.

``OSS_ACCESS_KEY_ID``

``OSS_SECRET_ACCESS_KEY``

``OSS_HOST``

``OSS_STORAGE_BUCKET_NAME``


