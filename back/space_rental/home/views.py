from django.shortcuts import render, redirect
from home.models import Space, SpaceCategory, SpaceCategoryMapping
from accounts.models import User as CustomUser
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    return render(request, 'home.html')

@login_required
def my_page(request):
    return render(request, 'my_page.html')

@login_required
def space_reg(request):
    if request.method == 'POST':
        # 폼 데이터 가져오기
        space_name = request.POST.get('space_name')
        description = request.POST.get('description', '')
        address = request.POST.get('address')
        capacity = request.POST.get('capacity')
        price_per_date = request.POST.get('price_per_date')
        category_ids = request.POST.getlist('category_name')  # 체크된 모든 카테고리 ID 가져오기

        # 현재 로그인한 사용자 가져오기
        auth_user = request.user
        try:
            user = CustomUser.objects.get(email=auth_user.username)
        except CustomUser.DoesNotExist:
            return render(request, 'my_page.html', {'error': '사용자를 찾을 수 없습니다.'})

        # Space 객체 생성 및 저장
        space = Space(
            space_name=space_name,
            description=description,
            address=address,
            capacity=int(capacity),
            price_per_date=int(price_per_date),
            user=user,
        )
        space.save()

        # SpaceCategoryMapping 생성
        for category_id in category_ids:
            try:
                category = SpaceCategory.objects.get(category_id=category_id)
                mapping = SpaceCategoryMapping(space=space, category=category)
                mapping.save()
            except SpaceCategory.DoesNotExist:
                continue  # 유효하지 않은 카테고리는 무시

        return redirect('space_reg')  # 등록 후 다시 공간 등록 페이지로 리디렉션

    # GET 요청: 로그인한 사용자가 등록한 공간 가져오기
    auth_user = request.user
    try:
        user = CustomUser.objects.get(email=auth_user.username)
        spaces = Space.objects.filter(user=user)  # 해당 사용자가 등록한 공간만 가져오기
    except CustomUser.DoesNotExist:
        spaces = []

    # 모든 카테고리 가져오기
    categories = SpaceCategory.objects.all()

    return render(request, 'space_reg.html', {'spaces': spaces, 'categories': categories})