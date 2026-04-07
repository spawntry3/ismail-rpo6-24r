from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Avg
from django.contrib import messages
from django.http import HttpResponseForbidden, JsonResponse

from .models import Ad, Category, City, Favorite, Review
from .forms import UserRegisterForm, AdForm, ReviewForm


def home_page(request):
    top_ad = Ad.objects.filter(is_moderated=True, is_top=True).select_related('category', 'city').order_by('?').first()
    recent_ads = Ad.objects.filter(is_moderated=True).select_related('category', 'city').order_by('?')[:8]
    context = {
        'top_ad': top_ad,
        'recent_ads': recent_ads,
        'total_ads': Ad.objects.filter(is_moderated=True).count(),
    }
    return render(request, 'index.html', context)


def all_ads_page(request):
    ads = Ad.objects.filter(is_moderated=True).select_related('category', 'city').order_by('-is_top', '-created_at')
    context = {'ads': ads}
    return render(request, 'ad_list.html', context)


def ads_by_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    ads = Ad.objects.filter(category=category, is_moderated=True).select_related('category', 'city').order_by('-is_top', '-created_at')
    context = {'category': category, 'ads': ads}
    return render(request, 'ads-by-category.html', context)


def search_page(request):
    return render(request, 'search.html')


def search_results(request):
    query = request.GET.get('q', '')
    results = []
    if query:
        results = Ad.objects.filter(
            is_moderated=True
        ).filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        ).select_related('category', 'city').order_by('-is_top', '-created_at')
    context = {'query': query, 'results': results}
    return render(request, 'search-results.html', context)


def api_ads_feed(request):
    ads = Ad.objects.filter(is_moderated=True).select_related('category', 'city').order_by('-is_top', '-created_at')
    payload = [
        {
            'uuid': str(ad.uuid),
            'title': ad.title,
            'description': ad.description,
            'price': ad.price,
            'is_top': ad.is_top,
            'image_url': ad.image_url,
            'category': ad.category.name,
            'city': ad.city.name,
            'created_at': ad.created_at.isoformat(),
            'author': ad.author.username,
        }
        for ad in ads
    ]
    return JsonResponse(payload, safe=False)


def read_ad_page(request, uuid):
    ad = get_object_or_404(Ad, uuid=uuid)
    related_ads = Ad.objects.filter(
        category=ad.category, is_moderated=True
    ).exclude(uuid=uuid).select_related('category', 'city').order_by('?')[:4]
    is_favorite = request.user.is_authenticated and Favorite.objects.filter(user=request.user, ad=ad).exists()
    author_reviews = Review.objects.filter(reviewed_user=ad.author).select_related('reviewer')
    avg_rating = author_reviews.aggregate(avg=Avg('rating'))['avg']
    user_review = None
    can_review = request.user.is_authenticated and request.user != ad.author
    if can_review:
        user_review = Review.objects.filter(reviewer=request.user, reviewed_user=ad.author).first()
    review_form = ReviewForm(instance=user_review)
    context = {
        'ad': ad,
        'related_ads': related_ads,
        'is_favorite': is_favorite,
        'author_reviews': author_reviews,
        'avg_rating': avg_rating,
        'reviews_count': author_reviews.count(),
        'can_review': can_review,
        'review_form': review_form,
        'user_review': user_review,
    }
    return render(request, 'read-ad.html', context)


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home_page')
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Аккаунт создан! Теперь войдите.')
            return redirect('login_page')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('profile_page')
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('profile_page')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home_page')


@login_required
def profile_page(request):
    my_ads = Ad.objects.filter(author=request.user).select_related('category', 'city').order_by('-created_at')
    favorites = Favorite.objects.filter(user=request.user).select_related('ad__category', 'ad__city')
    return render(request, 'profile.html', {'my_ads': my_ads, 'favorites': favorites})


@login_required
def ad_create_view(request):
    if request.method == 'POST':
        form = AdForm(request.POST)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.author = request.user
            ad.is_moderated = False
            ad.save()
            messages.success(request, 'Объявление отправлено на проверку.')
            return redirect('profile_page')
    else:
        form = AdForm()
    return render(request, 'ad-form.html', {'form': form})


@login_required
def ad_update_view(request, uuid):
    ad = get_object_or_404(Ad, uuid=uuid)
    if ad.author != request.user:
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = AdForm(request.POST, instance=ad)
        if form.is_valid():
            form.save()
            messages.success(request, 'Объявление обновлено.')
            return redirect('read_ad_page', uuid=ad.uuid)
    else:
        form = AdForm(instance=ad)
    return render(request, 'ad-form.html', {'form': form})


@login_required
def ad_delete_view(request, uuid):
    ad = get_object_or_404(Ad, uuid=uuid)
    if ad.author != request.user:
        return HttpResponseForbidden()
    if request.method == 'POST':
        ad.delete()
        messages.success(request, 'Объявление удалено.')
        return redirect('profile_page')
    return render(request, 'ad-confirm-delete.html', {'ad': ad})


@login_required
def toggle_favorite(request, uuid):
    ad = get_object_or_404(Ad, uuid=uuid)
    fav, created = Favorite.objects.get_or_create(user=request.user, ad=ad)
    if not created:
        fav.delete()
    return redirect(request.META.get('HTTP_REFERER', 'home_page'))


@login_required
def submit_review(request, uuid):
    ad = get_object_or_404(Ad, uuid=uuid)
    if request.method != 'POST':
        return redirect('read_ad_page', uuid=uuid)

    if request.user == ad.author:
        messages.error(request, 'Нельзя оставлять отзыв самому себе.')
        return redirect('read_ad_page', uuid=uuid)

    existing_review = Review.objects.filter(reviewer=request.user, reviewed_user=ad.author).first()
    form = ReviewForm(request.POST, instance=existing_review)
    if form.is_valid():
        review = form.save(commit=False)
        review.reviewer = request.user
        review.reviewed_user = ad.author
        review.save()
        if existing_review:
            messages.success(request, 'Ваш отзыв обновлен.')
        else:
            messages.success(request, 'Спасибо! Ваш отзыв сохранен.')
    else:
        messages.error(request, 'Проверьте правильность оценки и комментария.')
    return redirect('read_ad_page', uuid=uuid)
