from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.detail import SingleObjectMixin

from .forms import CreateReviewForm
from .models import Book


class BookListView(LoginRequiredMixin, ListView):
    model = Book
    template_name = 'books_list.html'


class BookDetailView(PermissionRequiredMixin, DetailView):
    model = Book
    template_name = 'book_detail.html'
    permission_required = 'books.verified_user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CreateReviewForm()
        return context


class BookReviewFormView(SingleObjectMixin, FormView):
    template_name = 'book_detail.html'
    form_class = CreateReviewForm
    model = Book

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['book'] = self.get_object()
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("book_detail", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        form.save()
        return super(BookReviewFormView, self).form_valid(form)


class BookView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        view = BookDetailView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = BookReviewFormView.as_view()
        return view(request, *args, **kwargs)


class SearchResultsListView(ListView):
    model = Book
    template_name = 'search_results.html'

    def get_queryset(self):
        query=self.request.GET.get("q")
        return Book.objects.filter(Q(title__icontains=query) | Q(author__icontains=query))
