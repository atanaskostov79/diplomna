from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import DetailView, ListView

from .forms import CommentForm
from .models import Category, Posts


def post_queryset():
    return Posts.objects.select_related('category').annotate(comment_count=Count('comments'))


class PostListView(ListView):
    model = Posts
    # template_name = 'posts/list_view.html'
    template_name = 'index.html'
    context_object_name = 'posts'
    queryset = post_queryset()


class CategoryPostListView(ListView):
    model = Posts
    template_name = 'posts/category.html'
    context_object_name = 'posts'

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.category = get_object_or_404(Category, slug=kwargs['slug'])

    def get_queryset(self):
        return post_queryset().filter(category=self.category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        context['section_title'] = self.category.name
        return context


class PostDetailView(DetailView):
    model = Posts
    template_name = 'posts/detail.html'
    context_object_name = 'post'
    queryset = post_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_posts'] = post_queryset().exclude(pk=self.object.pk)[:5]
        context['comments'] = self.object.comments.all()
        context.setdefault('comment_form', CommentForm())
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.object
            comment.save()
            return redirect('post-detail', pk=self.object.pk)
        context = self.get_context_data(comment_form=form)
        return self.render_to_response(context)
