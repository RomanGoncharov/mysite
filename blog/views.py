from django.http import HttpResponseRedirect, HttpResponse
from blog.models import BlogPost, PostComment
from django.contrib.auth.models import User
from blog.forms import AddNote, PostCommentForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import UpdateView, CreateView, DeleteView, FormView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from pure_pagination.mixins import PaginationMixin
from django.conf import settings
from django.core.urlresolvers import reverse
import json


class LoginRequiredView(object):

    @method_decorator(login_required())
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredView, self).dispatch(request, *args, **kwargs)


def main_view(request):

    if request.user.is_authenticated():
        return HttpResponseRedirect('blog/'+str(request.user.id)+'/page')
    else:
        return HttpResponseRedirect('auth/login')


class PostListView(PaginationMixin, ListView):
    page = 1
    paginate_by = settings.POSTS_ON_PAGE

    def get_queryset(self):
        self.queryset = BlogPost.posts.filter(author=self.kwargs['user_id'])
        return self.queryset

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        context['author_post'] = User.objects.get(id=self.kwargs['user_id'])
        return context


class PostAdd(LoginRequiredView, CreateView):
        model = BlogPost
        form_class = AddNote
        template_name = 'add_post.html'
        success_url = '/'

        def get(self, request, *args, **kwargs):
            return super(PostAdd, self).get(self, request, *args, **kwargs)

        def form_valid(self, form):
            # # if object==None:
            # #     form.instance.author=self.request.user
            # else:
            form.instance.author = self.request.user
            return super(PostAdd, self).form_valid(form)


class PostUpdate(LoginRequiredView, UpdateView):
        model = BlogPost
        form_class = AddNote
        success_url = '/'
        template_name = "change_post.html"

        def get_object(self, queryset=None):
            obj = super(PostUpdate, self).get_object(queryset)
            if self.request.user != obj.author:
                obj = None
            return obj

        def render_to_response(self, context, **response_kwargs):
            if self.object is None:
                return HttpResponseRedirect("/")
            else:
                return super(PostUpdate,self).render_to_response(context, **response_kwargs)


class PostDelete(LoginRequiredView, DeleteView):
    model = BlogPost
    success_url = '/'
    template_name = "delete_post.html"

    def get_object(self, queryset=None):
            obj = super(PostDelete,self).get_object(queryset)
            if self.request.user != obj.author:
                obj = None
            return obj

    def render_to_response(self, context, **response_kwargs):
            if self.object is None:
                return HttpResponseRedirect("/")
            else:
                return super(PostDelete, self).render_to_response(context, **response_kwargs)


class PostView(LoginRequiredView, DetailView, FormView):
    template_name = 'post_detail.html'
    model = BlogPost
    form_class = PostCommentForm
    object = None

    def get_context_data(self, **kwargs):
        context = {}
        context['post'] = self.get_object()
        context['form'] = self.get_form(self.form_class)
        return super(PostView, self).get_context_data(**context)

    def form_valid(self, form):
        post = self.get_object()
        msg = form.cleaned_data['comment']
        user = self.request.user
        comment = PostComment.comments.create(user=user, comment=msg)
        post.comments.add(comment)
        return HttpResponseRedirect(reverse("blog:detail_post", args=[post.id]))


def LikeRequest(request, number, *args): #SpaT_edition
    comment = PostComment.comments.get(pk=number)
    user = request.user
    sum_like = comment.like
    if user in comment.users_like.all():
        comment.users_like.remove(user)
        comment.like = sum_like-1
    else:
        comment.users_like.add(user)
        comment.like = sum_like+1
    comment.save()

    # result_vote = 0
    # all_users = []
    # for req in queryset:
    #
    #     if req.id == int(number):
    #
    #         result_vote = req.vote
    #         flag = True
    #         for user1 in req.users.all():
    #             if user1.id == user.id:
    #                 flag = False
    #                 break
    #         if not flag:
    #             req.vote -= 1
    #
    #             result_vote = req.vote
    #             req.users.remove(user)
    #             req.save()
    #
    #             for i in req.users.all():
    #                 all_users.append(i.username)
    #
    #             break
    #
    #         req.vote += 1
    #         req.users.add(user)
    #         req.save()
    #         for i in req.users.all():
    #                 all_users.append(i.username)
    #         result_vote = req.vote
    #         break

    return HttpResponse(content=json.dumps({
        'status': 'OK',
        'like': comment.like,
        # 'listuser': all_users,
        }, sort_keys=True))
