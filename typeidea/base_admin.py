# 抽象Adimin基类
# 抽象author类：当前用户再每个模块（分类、提交）只能看到自己的文章
from django.contrib import admin

class BaseOwnerAdmin(admin.ModelAdmin):
    '''
    1. 用来自动补充文章、分类、标签、侧边栏、有脸这些model的owner字段
    2.用来针对queryset过滤当前用户
    '''
    exclude = ['owner']

    def get_queryset(self,request):   # admin默认会展示所有对象。通过重写get_queryset方法，我们可以控制所需要获取的对象
        qs = super().get_queryset(request)  # super()由于调用父类方法，Python3.x 和 Python2.x 的一个区别是: Python 3 可以使用直接使用 super().xxx 代替 super(Class, self).xxx
        return qs.filter(owner=request.user)

    def save_model(self, request, obj, form, change):   # 文章创建时，后台自动添加当前用户为作者
        obj.owner = request.user
        return super().save_model(request,obj,form,change)