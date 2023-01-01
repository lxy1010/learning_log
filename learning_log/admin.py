from django.contrib import admin

from .models import Topic, Entry

# 创建完模型后在此处注册模型

admin.site.register(Topic)

admin.site.register(Entry)