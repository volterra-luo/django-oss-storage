django-oss-storage
==================

django storage backend for aliyun oss

Install
-------

```Python
python setup install
```

settings
--------
`DEFAULT_FILE_STORAGE`

This setting sets the path to the OSS storage class, this file will be installed to django's lib/site-packages folder, or keep it in PYTHONPATH if you store the storage file in other place:

```
DEFAULT_FILE_STORAGE = 'storages.backends.aliyun_oss.OssStorage'
```

`STATICFILES_STORAGE`

To allow django-admin.py collectstatic to automatically put your static files in your bucket set the following in your settings.py:

```Python

STATICFILES_STORAGE = 'storages.backends.aliyun_oss.OssStorage'
```
when using oss as your storage backend.

``OSS_ACCESS_KEY_ID``

>>Your Aliyun OSS access key, as a string.

``OSS_SECRET_ACCESS_KEY``

>>Your Aliyun OSS secret access key, as a string.

``OSS_HOST``

Aliyun OSS distributes their data center in Hangzhou, Beijing, Qingdao, and Hongkong, so you should explicitly set your  ``OSS_HOST`` where you would like to hold your bucket. Public access addresses available as following:

  * oss.aliyuncs.com (default) equivalent to oss-cn-hangzhou.aliyuncs.com
  * oss-cn-beijing.aliyuncs.com
  * oss-cn-qingdao.aliyuncs.com
  * oss-cn-hongkong.aliyuncs.com
 
The counterpart internal access addresses are:

  * oss-internal.aliyuncs.com equivalent to oss-cn-hangzhou-internal.aliyuncs.com
  * oss-cn-beijing-internal.aliyuncs.com
  * oss-cn-qingdao-internal.aliyuncs.com
  * oss-cn-hongkong-internal.aliyuncs.com
 

``OSS_STORAGE_BUCKET_NAME``

>>Your Aliyun OSS bucket name, as a string.

If you’d like to set headers sent with each file of the storage, please set ``OSS_HEADERS`` (optional):

``OSS_HEADERS``

```Python
OSS_HEADERS = {
    'Expires': 'Thu, 15 Apr 2100 00:00:00 GMT',
    'Cache-Control': 'max-age=86400',
}
```


