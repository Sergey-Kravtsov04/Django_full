from datetime import datetime
from django.contrib.auth import get_user_model
from django.shortcuts import render,redirect
from .models import BlogPost, Comment
from .forms import BlogModelForm, CommentModelForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required,permission_required

def title(request):
    title = "О нашем сайте"
    blog = BlogPost.objects.all()
    blogs = list(reversed(blog))[:3]  #Тут типизация ОБЯЗАТЕЛЬНА. Без неё вообще никак
    return render(request, 'main/main_title.html',{"title":title, "blogs":blogs})
def contact(request):
    title="О нас"
    User = get_user_model()
    users = User.objects.all()
    return render(request, 'main/main_contact.html',{"title":title,"users":users })
def index(request):
    blogs = BlogPost.objects.all()
    search = request.GET.get("search")

    if search:
        blogs = blogs.filter(title__icontains=search)  #Фильтруем по наличию введенной строки
    paginator = Paginator(blogs,2)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    title = "Список постов"
    return render(request, 'main/main.html', {"page_obj": page_obj, "blogs": blogs, "title": title})

def detail(request, pk):
    blogs = BlogPost.objects.all()
    blog = blogs.get(pk=pk)
    title = blog.title  #Обращаемся не ко всем тайтлам, а к конкретному

    count = str(request.GET.get("post"))
    comments = Comment.objects.filter(blog=blog).order_by("-date_published")  #Сортировка по дате публикации(сначала новые тк "-" в конце)
    # Делаем бесконечную прокрутку постов блога. Замыкаем их в кольцо,соединяя последний пост с первым
    if count == "prev":
        if blog.id == blogs.first().id:
            return redirect("main:main_detail", pk=blogs.last().id)
        prev_blog = blogs.filter(id__lt=blog.id).last()
        return redirect("main:main_detail", pk=prev_blog.id)
    #
    if count == "next":
        if blog.id == blogs.last().id:
            return redirect("main:main_detail", pk=blogs.first().id)
        next_blog = blogs.filter(id__gt=blog.id).first()
        return redirect("main:main_detail", pk=next_blog.id)
    #Создаём контекст внутри функции, чтобы не передавать всё это в рендер
    context = {
        "blog": blog,
        "title": title,
        "comments": comments
    }
    if request.method == "POST":
        form = CommentModelForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.date_published = datetime.now()
            new_comment.blog = blog
            new_comment.save()
            return redirect("main:main_detail", pk=pk)
    else:
        form = CommentModelForm()
    context["form"] = form
    return render(request, 'main/main_detail.html', context)
@permission_required("main.add_blogpost")
@login_required
def create_main(request):
    title = "Создание блога"
    action = "Создание"
    if request.method == "POST":
        form = BlogModelForm(request.POST, request.FILES)
        if form.is_valid():
            new_blog = form.save(commit=False)
            new_blog.user = request.user
            new_blog.date_published = datetime.now()
            new_blog.save()
            return redirect("main:title")
    else:
        form = BlogModelForm()
    return render(request,'main/create_update_main.html',{"title": title, "form": form,"action": action})

def is_owner(func):
    def wrapper(request, *args, **kwargs):
        blog_id = kwargs["pk"]
        if blog_id:
            blog = BlogPost.objects.get(pk=blog_id)
            if blog.user == request.user or request.user.is_superuser:
                return func(request, *args, **kwargs)
        return redirect("main:title")
    return wrapper
@is_owner
@login_required
def update_main(request,pk):
    title = "Обновить"
    blog = BlogPost.objects.get(pk=pk)
    action = f"Закончить редактирование блога '{blog.title}'"
    if request.method == "POST":
        form = BlogModelForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            return redirect("main:main_detail", pk=pk)
    else:
        form = BlogModelForm(instance=blog)
    return render(request, 'main/create_update_main.html', {"title": title, "form": form, "action": action})
@is_owner
@login_required
def delete_blog(request,pk):
    blog = BlogPost.objects.get(pk=pk)
    blog.delete()
    return redirect("main:news")
