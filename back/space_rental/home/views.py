from django.shortcuts import render, redirect, get_object_or_404
from home.models import Space, SpaceCategory, SpaceCategoryMapping, SpaceWithCategories
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
        spaces = SpaceWithCategories.objects.filter(user=user)  # 해당 사용자가 등록한 공간만 가져오기
    except CustomUser.DoesNotExist:
        spaces = []

    # 모든 카테고리 가져오기
    categories = SpaceCategory.objects.all()

    return render(request, 'space_reg.html', {'spaces': spaces, 'categories': categories})

@login_required
def update_space(request, space_id):
    space = get_object_or_404(Space, pk=space_id)

    auth_user = request.user
    try:
        user = CustomUser.objects.get(email=auth_user.username)
    except CustomUser.DoesNotExist:
        return redirect('my_page')

    if space.user != user:
        return redirect('my_page')  # 권한이 없으면 마이페이지로 리디렉션

    if request.method == 'POST':
        # 폼 데이터 가져오기
        space_name = request.POST.get('space_name')
        description = request.POST.get('description', '')
        address = request.POST.get('address')
        capacity = request.POST.get('capacity')
        price_per_date = request.POST.get('price_per_date')
        category_ids = request.POST.getlist('category_name')  # 수정된 카테고리 ID 가져오기

        # 공간 정보 업데이트
        space.space_name = space_name
        space.description = description
        space.address = address
        space.capacity = int(capacity)
        space.price_per_date = int(price_per_date)
        space.save()

        # 기존 카테고리 매핑 삭제 및 새로운 매핑 추가
        SpaceCategoryMapping.objects.filter(space=space).delete()
        for category_id in category_ids:
            try:
                category = SpaceCategory.objects.get(category_id=category_id)
                SpaceCategoryMapping.objects.create(space=space, category=category)
            except SpaceCategory.DoesNotExist:
                continue

        return redirect('space_reg')  # 수정 완료 후 마이페이지로 리디렉션

    # GET 요청: 공간 정보 수정 폼 표시
    all_categories = SpaceCategory.objects.all()
    selected_categories = SpaceCategoryMapping.objects.filter(space=space).values_list('category_id', flat=True)

    return render(
        request,
        'update_space.html',
        {'space': space, 'all_categories': all_categories, 'selected_categories': list(selected_categories)},
    )
