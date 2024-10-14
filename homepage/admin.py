from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Post

class CustomAdminSite(admin.AdminSite):
    site_header = "My Custom Admin"
    site_title = "Custom Admin Title"
    index_title = "Welcome to My Admin"

    def each_context(self, request):
        context = super().each_context(request)
        context['custom_css'] = mark_safe('<link rel="stylesheet" type="text/css" href="/static/homepage/css/custom_admin.css">')
        context['custom_js'] = mark_safe('<script type="text/javascript" src="/static/homepage/js/custom_admin.js"></script>')
        return context

admin_site = CustomAdminSite(name='custom_admin')

# Register your models with the custom admin site
admin_site.register(Post)

# Optionally, if you have more models, register them here
