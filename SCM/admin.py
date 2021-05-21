from django.contrib import admin
from .models import User, SCM1, Agent, UserProfile, Category

admin.site.register(Category)
admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(SCM1)
admin.site.register(Agent)

