from django.shortcuts import render, get_object_or_404
from .models import Category, Tool


def home(request):
    """首页视图"""
    featured_tools = Tool.objects.filter(is_published=True, is_featured=True)[:6]
    recent_tools = Tool.objects.filter(is_published=True)[:6]

    context = {
        'featured_tools': featured_tools,
        'recent_tools': recent_tools,
    }
    return render(request, 'tools/home.html', context)


def tool_list(request):
    """工具列表视图"""
    tools = Tool.objects.filter(is_published=True)
    categories = Category.objects.all()
    selected_category = request.GET.get('category')

    if selected_category:
        tools = tools.filter(category__slug=selected_category)

    context = {
        'tools': tools,
        'categories': categories,
        'selected_category': selected_category,
    }
    return render(request, 'tools/tool_list.html', context)


def tool_detail(request, slug):
    """工具详情视图"""
    tool = get_object_or_404(Tool, slug=slug, is_published=True)
    related_tools = Tool.objects.filter(
        category=tool.category,
        is_published=True
    ).exclude(id=tool.id)[:3]

    context = {
        'tool': tool,
        'related_tools': related_tools,
    }
    return render(request, 'tools/tool_detail.html', context)
