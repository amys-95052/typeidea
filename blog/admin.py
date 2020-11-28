from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from typeidea.base_admin import BaseOwnerAdmin
from .models import Post,Category,Tag
from .adminforms import PostAdminForm
from typeidea.custom_site import custom_site
from django.contrib.admin.models import LogEntry


@admin.register(Category,site=custom_site)      # model中的类注册到管理后台
class CategoryAdmin(BaseOwnerAdmin):
    list_display = ('name','status','is_nav','created_time','post_count')
    filed = ('name','status','is_nav')
    '''
    # obj是当前要保存的的对象，form时页面提交过来的表单对象，change标记是新增还是更新
    # 重写save_model方法，保存数据到数据库之前，把owner这个字段设定为当前的登录用户
    def save_model(self, request, obj, form, change):
        obj.owner = request.user     # 给obj.owner复制，自动设置owner
        return super().save_model(request,obj,form,change)
    '''
    # 分类的文章数量
    def post_count(self,obj):   # obj 是Post类实例
        return obj.post_set.count()

    post_count.short_description = '文章数量'


@admin.register(Tag,site=custom_site)
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


# 自定义过滤器（文章分类的过滤器），右侧展示的过滤器
class CategoryOwnerFilter(admin.SimpleListFilter):
    title = '分类过滤器'
    parameter_name = 'owner_category'   # 查询时URL参数的名字

    def lookups(self, request, model_admin):  # 返回右侧过滤器要展示的内容
        return Category.objects.filter(owner=request.user).values_list('id','name')

    def queryset(self, request, queryset):  # Queryset 列表页展示的所有数据
        category_id = self.value()   # 拿到URL参数的内容
        if category_id:
            return queryset.filter(category_id=self.value())
        return queryset




@admin.register(Post,site=custom_site)
class PostAdmin(BaseOwnerAdmin):            # ModelAdmin类是模型在Admin界面中的表现，定义子类来定义模式在界面的显示方式
    form = PostAdminForm
    list_display = [                          # 配置列表页面展示的字段属性
        'title','category','status',
        'created_time','operator',
        'owner',
    ]
    list_display_links = []                  # 哪些字段可以作为链接，点击可以进入相关的编辑页面,oneTooneField\ManytoManyField\oneToManyFiled
    list_filter = [CategoryOwnerFilter]               # 自定义的过滤器配置到ModelAdmin
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
            reverse('cus_admin:blog_post_change',args=(obj.id,))   # 根据名称解析出URL地址,数据记录的id
        )
    operator.short_description = '操作'
    '''
    def save_model(self, request, obj, form, change):     # 文章创建时，后台自动添加当前用户为作者
        obj.owner = request.user     
        return super(PostAdmin,self).save_model(request,obj,form,change)
        
    def get_queryset(self.request):                     # 文章列表只显示当前登录用户的文章
        qs = super(PostAdmin,self).get_queryset(request)
        return qs.filter(owner=request.owner)
    '''

@admin.register(LogEntry,site=custom_site)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ['object_repr','object_id','action_flag','user','change_message']