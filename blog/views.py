from django.shortcuts import render,HttpResponse
from .models import Post, Tag, Category
from config.models import Sidebar


def post_list(request,category_id=None,tag_id = None):
    category = None
    tag = None
    if tag_id:
        post_list,tag = Post.get_by_tag(tag_id)
    elif category_id:
        post_list,category = Post.get_by_category(category_id)
    else:
        post_list = Post.latest_posts()
    context ={
        'category':category,
        'tag':tag,
        'post_list':post_list,
        'sidebars':Sidebar.get_all(),
    }
    context.update(Category.get_nave())
    return render(request, 'blog/list.html', context=context)


def post_detail(request,post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoseNotExist:
        post = None
    context = {'post':post,'sidebars':Sidebar.get_all(),}
    context.update(Category.get_nave())
    return render(request,'blog/detail.html',context)