import markdown
import nh3
from django.db import models
from django.urls import reverse
from django.utils import timezone

ALLOWED_ATTRIBUTES = {
    **nh3.ALLOWED_ATTRIBUTES,
    "div": {"class"},
    "span": {"class"},
    "pre": {"class"},
    "code": {"class"},
}


def render_markdown(text):
    html = markdown.markdown(
        text,
        extensions=["fenced_code", "codehilite", "tables"],
        extension_configs={"codehilite": {"guess_lang": False}},
    )
    return nh3.clean(html, attributes=ALLOWED_ATTRIBUTES)


class Category(models.Model):
    """
    Category Post
    """

    name = models.CharField(verbose_name="Название категории", max_length=100)
    slug = models.SlugField(verbose_name="URL", max_length=50, unique=True)

    class Meta:
        db_table = "blog_category"
        ordering = ["name"]
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("blog:category", kwargs={"slug": self.slug})


class Tag(models.Model):
    """
    Tag Post
    """

    name = models.CharField(verbose_name="Название тега", max_length=50)
    slug = models.SlugField(verbose_name="URL", max_length=50, unique=True)

    class Meta:
        db_table = "blog_tag"
        ordering = ["name"]
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("blog:tag", kwargs={"slug": self.slug})


class Post(models.Model):
    """
    Models Post
    """

    STATUS_OPTIONS = (("published", "Опубликовано"), ("draft", "Черновик"))

    title = models.CharField(verbose_name="Название поста", max_length=255)
    slug = models.SlugField(verbose_name="URL", max_length=255, unique=True)
    summary = models.CharField(verbose_name="Описание поста", max_length=300)
    body = models.TextField(verbose_name="Основной текст")
    body_html = models.TextField(verbose_name="Текст в html", editable=False, blank=True)
    category = models.ForeignKey(
        to=Category,
        verbose_name="Категория",
        on_delete=models.PROTECT,
        related_name="posts",
    )
    tags = models.ManyToManyField(to=Tag, related_name="posts", blank=True)
    status = models.CharField(
        choices=STATUS_OPTIONS, default="draft", verbose_name="Статус поста", max_length=10
    )
    published_at = models.DateTimeField(null=True, blank=True, verbose_name="Время публикации")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время добавления")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Время обновления")

    class Meta:
        db_table = "blog_post"
        ordering = ["-published_at", "-created_at"]
        indexes = [models.Index(fields=["status", "-published_at"])]
        verbose_name = "Пост"
        verbose_name_plural = "Посты"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.body_html = render_markdown(self.body)
        if self.status == "published" and self.published_at is None:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("blog:post_detail", kwargs={"slug": self.slug})

    @property
    def reading_time(self):
        return max(1, round(len(self.body.split()) / 200))
