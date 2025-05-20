from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from .models import Book, CartItem, Profile
from .forms import BookForm, CustomUserCreationForm
from django.db.models import Q
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import TemplateView

# Create your views here.

class SignupView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


class BookSellView(LoginRequiredMixin, CreateView):
    model = Book
    form_class = BookForm
    template_name = 'book/book_form.html'
    success_url = reverse_lazy('book-list')

    def form_valid(self, form):
        form.instance.seller = self.request.user
        return super().form_valid(form)


class BookUpdateView(UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'book/book_update.html'

    def get_queryset(self):
        return Book.objects.filter(seller=self.request.user)

    def get_success_url(self):
        return reverse_lazy('book-detail', kwargs={'pk': self.object.pk})


class BookDeleteView(DeleteView):
    model = Book
    template_name = 'book/book_confirm_delete.html'
    success_url = reverse_lazy('book-list')

    def get_queryset(self):
        return Book.objects.filter(seller=self.request.user)


class BookListView(ListView):
    model = Book
    template_name = 'book/book_list.html'
    context_object_name = 'books'
    paginate_by = 5

    def get_queryset(self):
        queryset = Book.objects.all().order_by('-created_at')
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            ).distinct()
        return queryset


class BookDetailView(DetailView):
    model = Book
    template_name = 'book/book_detail.html'
    context_object_name = 'book'


class BuyNowView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        return render(request, 'book/order_confirmation.html', {'book': book})

    def post(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        messages.success(request, f"Purchased {book.title} successfully! (Dummy Payment)")
        return redirect('book-list')
    

class CartAddView(LoginRequiredMixin, View):
    def post(self, request, pk):
        book = get_object_or_404(Book, pk=pk)

        # Prevent user from adding their own listed book
        if book.seller == request.user:
            messages.error(request, "You cannot add your own book to cart.")
            return redirect('book-detail', pk=book.pk)

        cart_item, created = CartItem.objects.get_or_create(user=request.user, book=book)

        if cart_item.quantity < book.quantity:
            cart_item.quantity += 1
            cart_item.save()
        else:
            messages.warning(request, "No more stock available for this book.")

        return redirect('cart')
    

class CartDecreaseView(LoginRequiredMixin, View):
    def post(self, request, pk):
        cart_item = get_object_or_404(CartItem, pk=pk, user=request.user)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
        return redirect('cart')


class CartView(LoginRequiredMixin, TemplateView):
    template_name = 'book/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_items = CartItem.objects.filter(user=self.request.user).select_related('book')
        total = sum(item.book.price * item.quantity for item in cart_items)
        for item in cart_items:
            item.total_price = item.book.price * item.quantity
        context['cart_items'] = cart_items
        context['cart_total'] = total
        return context


class RemoveFromCartView(LoginRequiredMixin, View):
    login_url = 'login'

    def post(self, request, pk):
        cart_item = get_object_or_404(CartItem, id=pk, user=request.user)
        cart_item.delete()
        messages.success(request, "Item removed from cart.")
        return redirect('cart')


class CheckoutView(LoginRequiredMixin, View):
    login_url = 'login'

    def post(self, request):
        CartItem.objects.filter(user=request.user).delete()
        messages.success(request, "Checkout successful! (Dummy Payment)")
        return redirect('book-list')


class UserBookListView(LoginRequiredMixin, ListView):
    model = Book
    template_name = 'book/user_books.html'
    context_object_name = 'books'

    def get_queryset(self):
        return Book.objects.filter(seller=self.request.user)


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'book/profile_detail.html'

    def get_object(self):
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return profile


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    fields = ['bio', 'location']
    template_name = 'book/profile_update.html'
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user.profile
