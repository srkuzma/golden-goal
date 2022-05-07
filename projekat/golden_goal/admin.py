from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(News)
admin.site.register(Comment)
admin.site.register(Present)
admin.site.register(Prediction)
admin.site.register(UserImage)
