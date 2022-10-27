from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView
from .models import Post, Author, Subscribers
from .filters import PostFilter
from .forms import PostForm, ProfileForm, SubscribeForm
from django.shortcuts import redirect
from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import login_required
from django.core.cache import cache


class PostList(ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'posts'
    ordering = ['-creation_date']
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context


class PostDetail(DetailView):
    model = Post
    queryset = Post.objects.all()
    template_name = 'post.html'
    context_object_name = 'post'

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'post-{self.kwargs["pk"]}',
                        None)
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)

        return obj


class PostSearch(ListView):
    model = Post
    template_name = 'post_search.html'
    context_object_name = 'post_search'
    ordering = ['-creation_date']
    paginate_by = 1

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context


class PostDelete(DeleteView):
    template_name = 'post_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'


class PostCreate(PermissionRequiredMixin, CreateView):
    template_name = 'post_create.html'
    permission_required = ('accounts.add_post', 'accounts.change_post')
    form_class = PostForm


class PostUpdate(PermissionRequiredMixin, UpdateView):
    template_name = 'post_create.html'
    permission_required = ('accounts.add_post', 'accounts.change_post')
    form_class = PostForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


@login_required
def make_author(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
        Author.objects.create(user=user)
    return redirect('/news/')


class ProfileUpdate(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'profile_update.html'
    form_class = ProfileForm
    success_url = '/news/'

    def get_object(self, **kwargs):
        return self.request.user


class Subscribe(LoginRequiredMixin, CreateView):
    model = Subscribers
    template_name = 'subscribe.html'
    form_class = SubscribeForm
    success_url = '/news/'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['prefix'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.subscriber = self.request.user
        return super().form_valid(form)
