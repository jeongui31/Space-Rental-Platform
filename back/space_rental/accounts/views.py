from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User as AuthUser
from django.db import IntegrityError
from django.utils.timezone import now
from accounts.models import User, Host
from django.db.models import ObjectDoesNotExist


def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip().lower()  # 공백 제거 및 소문자 변환
        password = request.POST.get('password', '').strip()
        
        try:
            user = User.objects.get(email=email)  # 이메일로 사용자 검색
            print(f"Debug: Found user = {user}")
            if user.password == password:  # 비밀번호 확인
                auth_user = authenticate(username=email, password=password)
                if not auth_user:
                    auth_user = AuthUser.objects.create_user(username=email, password=password)
                login(request, auth_user)
                return redirect('/home/')  # 홈 페이지로 리디렉션
            else:
                return render(request, 'login.html', {'error': '잘못된 비밀번호입니다.'})
        except ObjectDoesNotExist:
            print("Debug: User does not exist")
            return render(request, 'login.html', {'error': '존재하지 않는 사용자입니다.'})

    return render(request, 'login.html')

def user_signup(request):
    if request.method == 'POST':
        # POST 데이터에서 값 가져오기
        user_name = request.POST.get('user_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        role = request.POST.get('role')
        company_name = request.POST.get('company_name', '')
        business_license = request.POST.get('business_license', '')

        try:
            # Host인 경우 추가 유효성 검사
            if role == 'host' and not business_license:
                error = '사업자 번호를 입력해야 합니다.'
                return render(request, 'signup.html', {
                    'error': error,
                    'user_name': user_name,
                    'email': email,
                    'phone': phone,
                    'role': role,
                    'company_name': company_name,
                })

            # User 객체 생성 및 저장
            user = User(
                user_name=user_name,
                email=email,
                phone=phone,
                password=password,
                role=role,
                user_created_at=now(),
                user_updated_at=now()
            )
            user.save()

            # Host인 경우 Host 객체 추가 저장
            if role == 'host':
                host = Host(
                    user=user,
                    company_name=company_name,
                    business_license=business_license,
                )
                host.save()

            return redirect('login')  # 성공 시 로그인 페이지로 리디렉션

        except IntegrityError:
            error = '이미 사용 중인 이메일 또는 전화번호입니다.'
            return render(request, 'signup.html', {
                'error': error,
                'user_name': user_name,
                'email': email,
                'phone': phone,
                'role': role,
                'company_name': company_name,
            })
        except Exception as e:
            error = str(e)
            return render(request, 'signup.html', {
                'error': error,
                'user_name': user_name,
                'email': email,
                'phone': phone,
                'role': role,
                'company_name': company_name,
            })
    else:
        # GET 요청일 경우 빈 폼 렌더링
        return render(request, 'signup.html')