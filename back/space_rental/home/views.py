from django.shortcuts import render, redirect, get_object_or_404
from home.models import Space, SpaceCategory, SpaceCategoryMapping, SpaceWithCategories, UserBookingView, Payment, Review, SpaceReviewAvg
from accounts.models import User as CustomUser, Host
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from django.db.models import ObjectDoesNotExist
from datetime import timedelta
from django.db import transaction



@login_required
def home(request):
    search_txt = request.GET.get('search_txt', '')
    category_id = request.GET.get('category', '')

    places = Space.objects.all()  # 모든 장소를 가져옴

    if search_txt and category_id:
        places = Space.objects.filter(
            space_name__icontains=search_txt,
            space_id__in=SpaceCategoryMapping.objects.filter(category_id=category_id).values('space_id')
        )

    elif search_txt:
        places = Space.objects.filter(space_name__icontains=search_txt)

    elif category_id:
        places = Space.objects.filter(space_id__in=SpaceCategoryMapping.objects.filter(category_id=category_id).values('space_id'))
       
    categories = SpaceCategory.objects.all()
    
    return render(request, 'home.html', {
        'places': places,
        'categories': categories,
        'search_txt': search_txt,
        'selected_category': category_id,
        })

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
        reservations = UserBookingView.objects.filter(email=user.email).order_by('-start_date')
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

        with transaction.atomic():
            try:

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
            except Exception as e:
                return render(request, 'space_reg.html',{
                    'error':f'공간 등록 중 오료가 발생했습니다: {str(e)}'
                })

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
        with transaction.atomic():
            try:
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
            except Exception as e:
                transaction.set_rollback(True)
                return redirect('space_reg', {'error':f'정보 수정 중 오류가 발생했습니다: {str (e)}'})
            
        return redirect('space_reg')  # 수정 완료 후 마이페이지로 리디렉션

    # GET 요청: 공간 정보 수정 폼 표시
    all_categories = SpaceCategory.objects.all()
    selected_categories = SpaceCategoryMapping.objects.filter(space=space).values_list('category_id', flat=True)

    return render(
        request,
        'update_space.html',
        {'space': space, 'all_categories': all_categories, 'selected_categories': list(selected_categories)},
    )


from datetime import date

@login_required
def booking_management(request):
    auth_user = request.user
    try:
        user = CustomUser.objects.get(email=auth_user.username)
    except CustomUser.DoesNotExist:
        return render(request, 'my_page.html', {'error': '사용자를 찾을 수 없습니다.'})

    if user.role.lower() != 'host':
        return redirect('my_page')  # 호스트가 아닌 경우 접근 금지

    # SQL 뷰에서 데이터 가져오기
    bookings = UserBookingView.objects.all()

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
        with transaction.atomic():
            try:
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
            except Exception as e:
                transaction.set_rollback(True)
                return render(request, 'edit_user_info.html', {'error': f'정보 수정 중 오류가 발생했습니다: {str(e)}'})

        return redirect('my_page')  # 수정 완료 후 마이페이지로 리디렉션

@login_required
def space_detail(request, space_id):
    space = get_object_or_404(Space, pk=space_id)
    review_avg = SpaceReviewAvg.objects.filter(space_id=space_id).first()
    reviews = Review.objects.filter(space=space).order_by('-review_created_at')
    # temp_total = 0
    # for i in reviews:
    #     temp_total = temp_total + i.review_rating

    # if not reviews:
    #     review_avg = 0.00
    # else:
    #     review_avg = temp_total / len(reviews)

    context = {
        'space': space,
        'reviews': reviews,
        'review_avg': round(review_avg.average_rating, 2) if review_avg else 0.00
    }
    return render(request, 'space_detail.html', context)

from django.http import JsonResponse
from home.models import Booking  # Booking 모델 임포트
import json

from datetime import timedelta, date

@login_required
def booking(request, space_id):
    space = get_object_or_404(Space, pk=space_id)
    user = request.user
    if request.method == 'GET':
        today = date.today()

        # 예약된 날짜 가져오기 (Canceled 제외)
        reserved_dates = Booking.objects.exclude(
            booking_status='Canceled'
        ).filter(
            space=space,
            booking_status__in=['Pending', 'Confirmed']
        ).values('start_date', 'end_date')

        # 날짜 범위를 리스트로 변환
        disabled_dates = []
        for booking in reserved_dates:
            current_date = booking['start_date']
            while current_date <= booking['end_date']:
                disabled_dates.append(current_date.strftime('%Y-%m-%d'))
                current_date += timedelta(days=1)

        try:
            custom_user = CustomUser.objects.get(email=user.username)
            user_role = custom_user.role.lower()  # Convert to lowercase for consistency
        except CustomUser.DoesNotExist:
            user_role = None
            
        return render(request, 'booking.html', {
            'space': space,
            'today': today,
            'disabled_dates': disabled_dates,
            'user_role': user_role,
        })

    elif request.method == 'POST':
        data = json.loads(request.body)
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        payment_method = data.get('payment_method')

        if not start_date or not end_date:
            return JsonResponse({'error': '날짜를 모두 입력하세요.'}, status=400)

        if end_date < start_date:
            return JsonResponse({'error': '종료 날짜는 시작 날짜보다 이전일 수 없습니다.'}, status=400)

        try:
            user = CustomUser.objects.get(email=request.user.username)
        except CustomUser.DoesNotExist:
            return JsonResponse({'error': '사용자를 찾을 수 없습니다.'}, status=400)

        # Calculate total payment amount
        start_date_obj = date.fromisoformat(start_date)
        end_date_obj = date.fromisoformat(end_date)
        total_days = (end_date_obj - start_date_obj).days + 1
        total_amount = total_days * space.price_per_date
        with transaction.atomic():
            # 락 설정
            bookings_for_update = Booking.objects.filter(
                space=space,
                booking_status__in=['Pending', 'Confirm'],
                end_date__gte=start_date_obj,
                start_date__lte=end_date_obj
            ).select_for_update()

            if bookings_for_update.exists():
                return JsonResponse({'error':'선택한 날짜에 이미 예약이 있습니다.'}, status=400)

            try:

                # Create a new booking
                booking = Booking.objects.create(
                    user=user,
                    space=space,
                    start_date=start_date,
                    end_date=end_date,
                    booking_status='Pending',
                )

                # Create a payment record linked to the booking
                Payment.objects.create(
                    booking=booking,
                    amount=total_amount,
                    payment_method=payment_method,
                    payment_status='Success',  # Default status
                )
            except Exception as e:
                transaction.rollback()
                return JsonResponse({'error': str(e)}, status=400)

        return JsonResponse({'message': '예약과 결제가 완료되었습니다!'})





from django.http import HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

@login_required
@csrf_exempt
def accept_booking(request, booking_id):
    if request.method == 'POST':
        try:
            user = CustomUser.objects.get(email=request.user.username)
            if user.role.lower() != 'host':
                return HttpResponseForbidden("권한이 없습니다.")
            
            booking = get_object_or_404(Booking, pk=booking_id)
            if booking.booking_status == 'Pending':
                booking.booking_status = 'Confirmed'
                booking.save()
            return redirect('booking_management')
        except CustomUser.DoesNotExist:
            return HttpResponseForbidden("사용자를 찾을 수 없습니다.")
    return JsonResponse({'error': '잘못된 요청 방식입니다.'}, status=405)


@login_required
@csrf_exempt
def reject_booking(request, booking_id):
    if request.method == 'POST':
        try:
            user = CustomUser.objects.get(email=request.user.username)
            if user.role.lower() != 'host':
                return HttpResponseForbidden("권한이 없습니다.")
            
            booking = get_object_or_404(Booking, pk=booking_id)
            if booking.booking_status == 'Pending':
                booking.booking_status = 'Canceled'
                booking.save()
                
                # Update the payment status to Failed
                try:
                    payment = Payment.objects.get(booking=booking)
                    payment.payment_status = 'Failed'
                    payment.save()
                except Payment.DoesNotExist:
                    return JsonResponse({'error': '해당 예약과 연결된 결제가 없습니다.'}, status=400)
            return redirect('booking_management')
        except CustomUser.DoesNotExist:
            return HttpResponseForbidden("사용자를 찾을 수 없습니다.")
    return JsonResponse({'error': '잘못된 요청 방식입니다.'}, status=405)

@login_required
def update_booking_status(request, booking_id, status):
    booking = get_object_or_404(Booking, pk=booking_id)

    if booking.booking_status == 'Pending' and status == 'Canceled':
        booking.booking_status = 'Canceled'
        booking.save()
        return JsonResponse({'message': '예약이 거절되었습니다. 날짜가 다시 예약 가능 상태로 변경되었습니다.'})
    elif status == 'Confirmed':
        booking.booking_status = 'Confirmed'
        booking.save()
        return JsonResponse({'message': '예약이 승인되었습니다.'})
    else:
        return JsonResponse({'error': '잘못된 상태 업데이트 요청입니다.'}, status=400)

@login_required
@csrf_exempt
def review(request, booking_id):
    user = CustomUser.objects.get(email=request.user.username)
    booking = get_object_or_404(Booking, booking_id=booking_id)
    space = booking.space

    if booking.user != user:
        return render(request, 'review.html', {'space': space, 'error_message': '해당 예약에 대해 리뷰를 작성할 권한이 없습니다.'})

    if Review.objects.filter(booking=booking).exists():
        return render(request, 'review.html', {'space': space, 'error_message': '해당 예약에 대해 이미 리뷰를 작성하셨습니다.'})

    if request.method == 'GET':
    
        return render(request, 'review.html', {'space': space})

    if request.method == 'POST':
        try:
            review_rating = request.POST.get('review_rating', 5)
            comment = request.POST.get('comment')

            Review.objects.create(
                user=user,
                space=space,
                review_rating=review_rating,
                comment=comment,
                booking=booking
            )

            return redirect('my_page')
        except Exception as e:
            return render(request, 'review.html', {'space': space,'error_message':"리뷰를 저정하는 중 오류가 발생했습니다."
            })