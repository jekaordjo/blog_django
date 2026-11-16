from django.db.models import Count, Q
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.generic import DetailView, ListView

from .models import Category, Post, Tag


class SidebarMixin:
    """Добавляет в контекст рубрики и теги для боковой колонки."""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        published = Q(posts__status="published", posts__published_at__lte=timezone.now())
        context["categories"] = Category.objects.annotate(
            posts_count=Count("posts", filter=published)
        ).filter(posts_count__gt=0)
        context["tags"] = Tag.objects.filter(published).distinct()
        return context


class PostListView(SidebarMixin, ListView):
    paginate_by = 10
    template_name = "blog/post_list.html"

    def get_queryset(self):
        return Post.objects.published().select_related("category")


class CategoryPostListView(SidebarMixin, ListView):
    paginate_by = 10
    template_name = "blog/post_list.html"

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs["slug"])
        return Post.objects.published().filter(category=self.category).select_related("category")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_category"] = self.category
        return context


class TagPostListView(SidebarMixin, ListView):
    paginate_by = 10
    template_name = "blog/post_list.html"

    def get_queryset(self):
        self.tag = get_object_or_404(Tag, slug=self.kwargs["slug"])
        return Post.objects.published().filter(tags=self.tag).select_related("category")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_tag"] = self.tag
        return context


class PostDetailView(DetailView):
    template_name = "blog/post_detail.html"

    def get_queryset(self):
        return Post.objects.published().select_related("category").prefetch_related("tags")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        published = Post.objects.published()
        date = self.object.published_at
        context["prev_post"] = published.filter(published_at__lt=date).first()
        context["next_post"] = (
            published.filter(published_at__gt=date).order_by("published_at").first()
        )
        return context
