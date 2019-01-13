from django.contrib import admin

# Register your models here.

from blog.models import Article, Category,Comment,User


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'atc_topic', 'click_count', 'like_count','create_time')
    list_display_links =  ('id', 'atc_topic', 'click_count', 'like_count','create_time')
    fieldsets = (
        ('Article', {
            'fields': ('atc_topic','atc_desc', 'atc_content' )
        }),
        ('Time', {
            'classes': ('readonly',),
            'fields': ('create_time', 'update_time',)
        }),
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    fieldsets = (
        ('Base Info',{
            'fields':('cg_name',)
        }),
        ('Img Info', {
            'fields': ('imgpath',)
        }),
    )

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Base Info",{
            'fields':('username','password','first_name','last_name','email',),
        }),
        ("Advance Info", {
            'fields': ('chinese_name','desc'),
        }),
    )
