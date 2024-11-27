from django.shortcuts import render, redirect, get_object_or_404
from home.models import Space, SpaceCategory, SpaceCategoryMapping, SpaceWithCategories
from accounts.models import User as CustomUser, Host
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from django.db.models import ObjectDoesNotExist


@login_required
def home(request):
    places = Space.objects.all()  # 모든 장소를 가져옴
    return render(request, 'home.html', {'places': places})

@login_required
def my_page(request):
    auth_user = request.user
    try:
        user = CustomUser.objects.get(email=auth_user.username)
    except CustomUser.DoesNotExist:
        return render(request, 'my_page.html', {'error': '사용자를 찾을 수 없습니다.'})

    role = user.role.lower()  # role 값을 소문자로 변환하여 처리 (예: "guest", "host")

    if role == "guest":
        # Guest 사용자에게 표시할 예약 내역
        reservations = []  # 예약 내역 가져오기 (로직 필요)
        context = {
            'role': role,
            'user': user,
            'reservations': reservations,
        }
    elif role == "host":
        # Host 사용자에게 표시할 등록된 공간
        spaces = SpaceWithCategories.objects.filter(user=user)
        context = {
            'role': role,
            'user': user,
            'spaces': spaces,
        }
    else:
        # 예외 처리
        context = {'error': '알 수 없는 사용자 유형입니다.'}

    return render(request, 'my_page.html', context)

import requests

@login_required
def space_reg(request):
    if request.method == 'POST':
        # 폼 데이터 가져오기
        space_name = request.POST.get('space_name')
        description = request.POST.get('description', '')
        address = request.POST.get('address')
        capacity = request.POST.get('capacity')
        price_per_date = request.POST.get('price_per_date')
        category_ids = request.POST.getlist('category_name')

        # 이미지 파일 가져오기
        image_file = request.FILES.get('image')  # HTML 폼의 이미지 필드
        image_url = None

        if image_file:
            # Imgbb API에 이미지 업로드
            imgbb_api_key = "afacb4ce431ff6c3171943864161107f"  # 여기에 Imgbb API 키 입력
            imgbb_endpoint = "https://api.imgbb.com/1/upload"

            try:
                response = requests.post(
                    imgbb_endpoint,
                    data={'key': imgbb_api_key},
                    files={'image': image_file}
                )
                if response.status_code == 200:
                    image_url = response.json().get('data', {}).get('url')  # 업로드된 이미지 URL
                else:
                    print("Imgbb API Error:", response.json())
            except Exception as e:
                print("Image upload failed:", e)

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
            image=image_url,  # 이미지 URL 저장
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
        spaces = SpaceWithCategories.objects.filter(user=user)
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

@login_required
def booking_management(request):
    auth_user = request.user
    try:
        user = CustomUser.objects.get(email=auth_user.username)
    except CustomUser.DoesNotExist:
        return render(request, 'my_page.html', {'error': '사용자를 찾을 수 없습니다.'})

    # 예약 처리 관련 데이터 가져오기
    if user.role.lower() == 'host':
        bookings = []  # 예약 데이터 로드 로직 추가
    else:
        return redirect('my_page')  # 호스트가 아닌 경우 접근 금지

    return render(request, 'booking_management.html', {'bookings': bookings})

@login_required
def edit_user_info(request):
    try:
        auth_user = request.user
        user = CustomUser.objects.get(email=auth_user.username)
    except CustomUser.DoesNotExist:
        return render(request, 'edit_user_info.html', {'error': '사용자를 찾을 수 없습니다.'})

    if request.method == 'GET':
        context = {
            'email': user.email,
            'password': user.password,  # 비밀번호는 암호화되어 있으므로 보통은 표시하지 않음
            'user_name': user.user_name,
            'phone': user.phone,
            'role': user.role,
        }

        if user.role.lower() == 'host':
            try:
                host = Host.objects.get(user=user)
                context.update({
                    'company_name': host.company_name,
                    'business_license': host.business_license,
                })
            except ObjectDoesNotExist:
                context.update({'company_name': '', 'business_license': ''})

        return render(request, 'edit_user_info.html', context)

    elif request.method == 'POST':
        user.user_name = request.POST.get('user_name', user.user_name)
        user.phone = request.POST.get('phone', user.phone)

        new_password = request.POST.get('password')
        if new_password:
            user.password = new_password

        user.save()

        if user.role.lower() == 'host':
            company_name = request.POST.get('company_name', '')
            business_license = request.POST.get('business_license', '')

            try:
                host = Host.objects.get(user=user)
                host.company_name = company_name
                host.business_license = business_license
                host.save()
            except ObjectDoesNotExist:
                Host.objects.create(
                    user=user,
                    company_name=company_name,
                    business_license=business_license
                )

        return redirect('my_page')  # 수정 완료 후 마이페이지로 리디렉션
