from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Suggestion
from taggit.models import Tag
from .forms import TestForm, SuggestionForm
from django.db.models import Q
from django.db.models.functions import Lower
from dal import autocomplete

def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 20


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 20

    def get_query_set(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        print(f"USER: {user}")
        return Post.objects.filter(author=user).order_by('date_posted')


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = TestForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        print("VALID FORM")
        print(self.request.user)
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'media']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class SearchResultsView(ListView):
    template_name = 'blog/search_results.html'
    model = Post
    ordering = ['date_posted']

    def get_queryset(self):
        query = self.request.GET.get('q')

        object_list = Post.objects.filter(
            Q(title__icontains=query) | Q(tags__name__iexact=query)
        )

        return object_list.order_by('-date_posted')


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})


class TagAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):

        if not self.request.user.is_authenticated:
            return Tag.objects.none()

        qs = Tag.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs

class suggestion(LoginRequiredMixin, CreateView):
    template_name = 'blog/suggestion.html'
    model = Suggestion

    form_class = SuggestionForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        print(self.request.user)
        return super().form_valid(form)