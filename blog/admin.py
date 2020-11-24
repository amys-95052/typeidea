from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from typeidea.base_admin import BaseOwnerAdmin
from .models import Post,Category,Tag


@admin.register(Category)      # model中的类注册到管理后台
class CategoryAdmin(BaseOwnerAdmin):
    list_display = ('name','status','is_nav','created_time','post_count')
    filed = ('name','status','is_nav')
    '''
    # obj是当前要保存的的对象，form时页面提交过来的表单对象，change标记是新增还是更新
    # 重写save_model方法，保存数据到数据库之前，把owner这个字段设定为当前的登录用户
    def save_model(self, request, obj, form, change):
        obj.owner = request.user     # 给obj.owner复制，自动设置owner
        return super(CategoryAdmin,self).save_model(request,obj,form,change)
    '''
    # 分类的文章数量
    def post_count(self,obj):   # obj 是Post类实例
        return obj.post_set.count()

    post_count.short_description = '文章数量'


@admin.register(Tag)
class TagAdmin(BaseOwnerAdmin):
    list_display = ('name','status','created_time','post_count')
    filed = ('name','status')
    '''
    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(TagAdmin,self).save_model(request,obj,form,change)
    '''
    # 标签的文章数量
    def post_count(self,obj):
        return obj.post_set.all().count()

    post_count.short_description = '文章数量'


# 自定义过滤器只展示当前用户的分类
class CategoryOwnerFilter(admin.SimpleListFilter):
    title = '分类过滤器'
    parameter_name = 'owner_category'

    def lookups(self, request, model_admin):  # 返回要展示的内容
        return Category.objects.filter(owner=request.user).values_list('id','name')

    def queryset(self, request, queryset):  # 根据 URL Query 的内容返回列表页数据。
        category_id = self.value()   # queryset 是列表页所有展示数据的集合
        if category_id:
            return queryset.filter(category_id=self.value())
        return queryset




@admin.register(Post)
class PostAdmin(BaseOwnerAdmin):            # ModelAdmin类是模型在Admin界面中的表现，定义子类来定义模式在界面的显示方式
    list_display = [                          # 配置列表页面展示的字段属性
        'title','category','status',
        'created_time','operator',
        'owner',
    ]
    list_display_links = []                  # 哪些字段可以作为链接，点击可以进入相关的编辑页面,oneTooneField\ManytoManyField\oneToManyFiled
    list_filter = [CategoryOwnerFilter]               # 配置过滤列，通过那些字段来过滤列表页
    search_fields = ['title','category__name'] # 配置搜索字段，通过上下划线(__)hiding关联搜索Model数据

    actions_on_top = True                     # 动作相关的配置，是否展示在本地
    actions_on_bottom = True

    # 编辑页面
    save_on_top =  True                      # 保存编辑等相关按钮是否在顶部展示
    #exclude = ['owner']

    fields =[
        ('category','title'),
        'desc',
        'status',
        'content',
        'tag',
    ]
    filter_vertical = ('tag',)

    def operator(self,obj):                    # 在list_dispaly在世自定义字段
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('admin:blog_post_change',args=(obj.id,))   # 根据名称解析出URL地址
        )
        operator.short_description = '操作'
    '''
    def save_model(self, request, obj, form, change):
        obj.owner = request.user     # 文章创建时，后台自动添加当前用户为作者
        return super(PostAdmin,self).save_model(request,obj,form,change)
    '''

