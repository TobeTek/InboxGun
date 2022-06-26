from django.shortcuts import render, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy

from . import models

# Create your views here.
class PostListView(ListView):
    model = models.Post
    paginate_by = 5


class PostCreateView(CreateView):
    model = models.Post
    fields = "__all__"
    success_url = reverse_lazy("blog:all")


class PostDetailView(DetailView):
    model = models.Post


class PostUpdateView(UpdateView):
    model = models.Post
    fields = "__all__"
    success_url = reverse_lazy("blog:all")


class PostDeleteView(DeleteView):
    model = models.Post
    success_url = reverse_lazy("blog:all")


# def post_list(request):
#     posts = models.Post.published.all()
#     return render(request, "blog/post/list.html", {"posts": posts})


# def post_detail(request, year, month, day, post):
#     post = get_object_or_404(
#         models.Post,
#         slug=post,
#         status=models.Post.StatusChoices.published,
#         publish__year=year,
#         publish__month=month,
#         publish__day=day,
#     )
#     return render(request, "blog/post/detail.html", {"post": post})
