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
Your Aliyun OSS access key, as a string.

``OSS_SECRET_ACCESS_KEY``
Your Aliyun OSS secret access key, as a string.

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
Your Aliyun OSS bucket name, as a string.


