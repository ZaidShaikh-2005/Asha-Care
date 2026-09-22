from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render
)
from django.utils.encoding import force_bytes
from django.utils.http import (
    urlsafe_base64_decode,
    urlsafe_base64_encode
)

from django.db.models import Q

from .models import Family, Member, Village


# =========================================================
# LOGIN
# =========================================================

def login_view(request):

    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':

        pin = request.POST.get(
            'pin',
            ''
        ).strip()

        if len(pin) != 6 or not pin.isdigit():

            return render(
                request,
                'login.html',
                {
                    'error': (
                        'Please enter a valid 6-digit PIN.'
                    )
                }
            )

        user = authenticate(
            request,
            username='asha',
            password=pin
        )

        if user is not None:

            login(
                request,
                user
            )

            return redirect('dashboard')

        return render(
            request,
            'login.html',
            {
                'error': (
                    'Incorrect PIN. Please try again.'
                )
            }
        )

    return render(
        request,
        'login.html'
    )


# =========================================================
# LOGOUT
# =========================================================

@login_required
def logout_view(request):

    logout(request)

    return redirect('login')


# =========================================================
# DASHBOARD
# =========================================================

@login_required
def dashboard(request):

    from django.utils import timezone

    total_families = Family.objects.count()

    total_members = Member.objects.count()

    total_male_members = Member.objects.filter(
        gender='Male'
    ).count()

    total_female_members = Member.objects.filter(
        gender='Female'
    ).count()

    total_pregnant = Member.objects.filter(
        gender='Female',
        currently_pregnant=True
    ).count()

    # =====================================================
    # AYUSHMAN CARD SUBMITTED
    # =====================================================

    ayushman_card_submitted = (
        Member.objects
        .exclude(
            ayushman_card_number__isnull=True
        )
        .exclude(
            ayushman_card_number=''
        )
        .count()
    )

    # =====================================================
    # AYUSHMAN CARD PENDING
    # =====================================================

    ayushman_card_pending = (
        Member.objects.filter(
            Q(
                ayushman_card_number__isnull=True
            )
            |
            Q(
                ayushman_card_number=''
            )
        )
        .count()
    )

    # =====================================================
    # ABHA CARD PENDING
    # =====================================================

    abha_card_pending = (
        Member.objects.filter(
            Q(
                abha_number__isnull=True
            )
            |
            Q(
                abha_number=''
            )
        )
        .count()
    )

    # =====================================================
    # ALL PREGNANT LADIES
    # =====================================================

    pregnant_members = (
        Member.objects
        .filter(
            gender='Female',
            currently_pregnant=True
        )
        .select_related(
            'family'
        )
        .order_by(
            'family__house_number',
            'name'
        )
    )

    today = timezone.localdate()

    # =====================================================
    # PREGNANT LADIES DUE THIS MONTH
    # =====================================================

    pregnant_due_this_month = (
        Member.objects
        .filter(
            gender='Female',
            currently_pregnant=True,
            expected_delivery_date__year=today.year,
            expected_delivery_date__month=today.month
        )
        .select_related(
            'family'
        )
        .order_by(
            'expected_delivery_date'
        )
    )

    return render(
        request,
        'dashboard.html',
        {
            'total_families': total_families,

            'total_members': total_members,

            'total_male_members': (
                total_male_members
            ),

            'total_female_members': (
                total_female_members
            ),

            'total_pregnant': (
                total_pregnant
            ),

            'ayushman_card_submitted': (
                ayushman_card_submitted
            ),

            'ayushman_card_pending': (
                ayushman_card_pending
            ),

            'abha_card_pending': (
                abha_card_pending
            ),

            'pregnant_members': (
                pregnant_members
            ),

            'pregnant_due_this_month': (
                pregnant_due_this_month
            ),
        }
    )


# =========================================================
# AYUSHMAN CARD SUBMITTED
# =========================================================

@login_required
def ayushman_submitted(request):

    members = (
        Member.objects
        .exclude(
            ayushman_card_number__isnull=True
        )
        .exclude(
            ayushman_card_number=''
        )
        .select_related(
            'family__village'
        )
        .order_by(
            'family__village__village_number',
            'family__house_number',
            'name'
        )
    )

    return render(
        request,
        'ayushman_submitted.html',
        {
            'members': members
        }
    )


# =========================================================
# AYUSHMAN CARD PENDING
# =========================================================

@login_required
def ayushman_pending(request):

    members = (
        Member.objects
        .filter(
            Q(
                ayushman_card_number__isnull=True
            )
            |
            Q(
                ayushman_card_number=''
            )
        )
        .select_related(
            'family__village'
        )
        .order_by(
            'family__village__village_number',
            'family__house_number',
            'name'
        )
    )

    return render(
        request,
        'ayushman_pending.html',
        {
            'members': members
        }
    )


# =========================================================
# ABHA CARD PENDING
# =========================================================

@login_required
def abha_pending(request):

    members = (
        Member.objects
        .filter(
            Q(
                abha_number__isnull=True
            )
            |
            Q(
                abha_number=''
            )
        )
        .select_related(
            'family__village'
        )
        .order_by(
            'family__village__village_number',
            'family__house_number',
            'name'
        )
    )

    return render(
        request,
        'abha_pending.html',
        {
            'members': members
        }
    )


# =========================================================
# ADD FAMILY
# =========================================================

@login_required
def add_family(request):

    villages = (
        Village.objects
        .all()
        .order_by(
            'village_number'
        )
    )

    if request.method == 'POST':

        family_name = request.POST.get(
            'family_name'
        )

        village_id = request.POST.get(
            'village_id'
        )

        house_number = request.POST.get(
            'house_number'
        )

        family_number = request.POST.get(
            'family_number'
        )

        contact_number = request.POST.get(
            'contact_number'
        )

        address = request.POST.get(
            'address'
        )

        area = request.POST.get(
            'area'
        )

        pin_code = request.POST.get(
            'pin_code'
        )

        # Check village

        village = Village.objects.filter(
            id=village_id
        ).first()

        if not village:

            return render(
                request,
                'add_family.html',
                {
                    'villages': villages,
                    'error': (
                        'Please select a valid village.'
                    )
                }
            )

        # Check house number

        try:

            house_number = int(
                house_number
            )

        except (
            TypeError,
            ValueError
        ):

            return render(
                request,
                'add_family.html',
                {
                    'villages': villages,
                    'error': (
                        'Please select a valid house number.'
                    )
                }
            )

        if (
            house_number < 1
            or house_number > village.total_houses
        ):

            return render(
                request,
                'add_family.html',
                {
                    'villages': villages,
                    'error': (
                        'Invalid house number for selected village.'
                    )
                }
            )

        # Save Family

        family = Family.objects.create(

            family_name=family_name,

            village=village,

            house_number=house_number,

            family_number=family_number,

            contact_number=contact_number,

            address=address,

            area=area,

            pin_code=pin_code

        )

        return redirect(
            f'/add-member/?family_id={family.id}'
        )

    return render(
        request,
        'add_family.html',
        {
            'villages': villages
        }
    )


# =========================================================
# FAMILY LIST
# =========================================================

@login_required
def family_list(request):

    search = request.GET.get(
        'search',
        ''
    ).strip()

    village_id = request.GET.get(
        'village'
    )

    families = (
        Family.objects
        .select_related(
            'village'
        )
        .all()
    )

    # Filter by selected village

    if village_id:

        families = families.filter(
            village_id=village_id
        )

    # Search

    if search:

        families = families.filter(
            Q(
                family_name__icontains=search
            )
            |
            Q(
                village__name__icontains=search
            )
            |
            Q(
                house_number__icontains=search
            )
        )

    families = families.order_by(
        'village__village_number',
        'house_number',
        'family_name'
    )

    # Group families village-wise

    villages_with_families = []

    current_village = None

    current_families = []

    for family in families:

        if (
            current_village is None
            or current_village.id != family.village.id
        ):

            if current_village is not None:

                villages_with_families.append({
                    'village': current_village,
                    'families': current_families
                })

            current_village = family.village

            current_families = []

        current_families.append(
            family
        )

    if current_village is not None:

        villages_with_families.append({
            'village': current_village,
            'families': current_families
        })

    return render(
        request,
        'family_list.html',
        {
            'villages_with_families': (
                villages_with_families
            ),

            'search': search,

            'selected_village_id': (
                village_id
            ),
        }
    )


# =========================================================
# FAMILY DETAIL
# =========================================================

@login_required
def family_detail(
    request,
    family_id
):

    family = get_object_or_404(
        Family,
        id=family_id
    )

    members = (
        family.members
        .all()
        .order_by(
            'id'
        )
    )

    return render(
        request,
        'family_detail.html',
        {
            'family': family,
            'members': members,
        }
    )


# =========================================================
# ADD MEMBER
# =========================================================

@login_required
def add_member(request):

    families = (
        Family.objects
        .all()
        .order_by(
            'family_name'
        )
    )

    if request.method == 'POST':

        family_id = request.POST.get(
            'family'
        )

        family = get_object_or_404(
            Family,
            id=family_id
        )

        name = request.POST.get(
            'name'
        )

        gender = request.POST.get(
            'gender'
        )

        blood_group = request.POST.get(
            'blood_group'
        )

        relation = request.POST.get(
            'relation'
        )

        # Pregnancy information

        currently_pregnant = (
            gender == 'Female'
            and request.POST.get(
                'currently_pregnant'
            ) == 'Yes'
        )

        pregnancy_start_date = None

        expected_delivery_date = None

        if currently_pregnant:

            pregnancy_start_date = (
                request.POST.get(
                    'pregnancy_start_date'
                ) or None
            )

            expected_delivery_date = (
                request.POST.get(
                    'expected_delivery_date'
                ) or None
            )

        date_of_birth = request.POST.get(
            'date_of_birth'
        )

        religion = request.POST.get(
            'religion'
        )

        caste = request.POST.get(
            'caste'
        )

        bpl = (
            request.POST.get(
                'bpl'
            ) == 'Yes'
        )

        mobile_number = request.POST.get(
            'mobile_number'
        )

        bpl_number = request.POST.get(
            'bpl_number'
        )

        ayushman_card_number = request.POST.get(
            'ayushman_card_number'
        )

        aadhaar_number = request.POST.get(
            'aadhaar_number'
        )

        abha_number = request.POST.get(
            'abha_number'
        )

        # PHOTO IS OPTIONAL

        profile_photo = request.FILES.get(
            'profile_photo'
        )

        ayushman_card_file = request.FILES.get(
            'ayushman_card_file'
        )

        aadhaar_card_file = request.FILES.get(
            'aadhaar_card_file'
        )

        abha_card_file = request.FILES.get(
            'abha_card_file'
        )

        disease = request.POST.get(
            'disease'
        )

        alive_status = request.POST.get(
            'alive_status'
        )

        remarks = request.POST.get(
            'remarks'
        )

        Member.objects.create(

            family=family,

            name=name,

            profile_photo=profile_photo,

            gender=gender,

            blood_group=blood_group,

            relation=relation,

            currently_pregnant=(
                currently_pregnant
            ),

            pregnancy_start_date=(
                pregnancy_start_date
            ),

            expected_delivery_date=(
                expected_delivery_date
            ),

            date_of_birth=date_of_birth,

            religion=religion,

            caste=caste,

            bpl=bpl,

            mobile_number=mobile_number,

            bpl_number=bpl_number,

            ayushman_card_number=(
                ayushman_card_number
            ),

            aadhaar_number=aadhaar_number,

            abha_number=abha_number,

            ayushman_card_file=(
                ayushman_card_file
            ),

            aadhaar_card_file=(
                aadhaar_card_file
            ),

            abha_card_file=(
                abha_card_file
            ),

            disease=disease,

            alive_status=alive_status,

            remarks=remarks

        )

        return redirect(
            'family_detail',
            family_id=family.id
        )

    return render(
        request,
        'add_member.html',
        {
            'families': families
        }
    )


# =========================================================
# MEMBER LIST
# =========================================================

@login_required
def member_list(request):

    search = request.GET.get(
        'search',
        ''
    ).strip()

    families = (
        Family.objects
        .select_related(
            'village'
        )
        .prefetch_related(
            'members'
        )
        .order_by(
            'village__village_number',
            'house_number',
            'family_name'
        )
    )

    if search:

        search_query = Q(
            members__name__icontains=search
        )

        try:

            house_number = int(
                search
            )

            search_query |= Q(
                house_number=house_number
            )

        except ValueError:

            pass

        search_query |= Q(
            family_name__icontains=search
        )

        families = families.filter(
            search_query
        ).distinct()

    families_with_members = []

    for family in families:

        members = (
            family.members
            .all()
            .order_by(
                'id'
            )
        )

        if members.exists():

            families_with_members.append({
                'family': family,
                'members': members,
            })

    return render(
        request,
        'member_list.html',
        {
            'families': families_with_members,
            'search': search,
        }
    )


# =========================================================
# MEMBER DETAIL
# =========================================================

@login_required
def member_detail(
    request,
    member_id
):

    member = get_object_or_404(
        Member,
        id=member_id
    )

    return render(
        request,
        'member_detail.html',
        {
            'member': member,
            'edit_mode': False,
        }
    )


# =========================================================
# EDIT MEMBER
# =========================================================

@login_required
def edit_member(
    request,
    member_id
):

    member = get_object_or_404(
        Member,
        id=member_id
    )

    if request.method == 'POST':

        member.name = request.POST.get(
            'name'
        )

        member.gender = request.POST.get(
            'gender'
        )

        member.blood_group = request.POST.get(
            'blood_group'
        )

        member.relation = request.POST.get(
            'relation'
        )

        # Pregnancy information

        member.currently_pregnant = (
            member.gender == 'Female'
            and request.POST.get(
                'currently_pregnant'
            ) == 'Yes'
        )

        if member.currently_pregnant:

            member.pregnancy_start_date = (
                request.POST.get(
                    'pregnancy_start_date'
                ) or None
            )

            member.expected_delivery_date = (
                request.POST.get(
                    'expected_delivery_date'
                ) or None
            )

        else:

            member.pregnancy_start_date = None

            member.expected_delivery_date = None

        member.date_of_birth = request.POST.get(
            'date_of_birth'
        )

        member.religion = request.POST.get(
            'religion'
        )

        member.caste = request.POST.get(
            'caste'
        )

        member.bpl = (
            request.POST.get(
                'bpl'
            ) == 'Yes'
        )

        member.mobile_number = request.POST.get(
            'mobile_number'
        )

        member.bpl_number = request.POST.get(
            'bpl_number'
        )

        member.ayushman_card_number = (
            request.POST.get(
                'ayushman_card_number'
            )
        )

        member.aadhaar_number = (
            request.POST.get(
                'aadhaar_number'
            )
        )

        member.abha_number = (
            request.POST.get(
                'abha_number'
            )
        )

        member.disease = request.POST.get(
            'disease'
        )

        member.alive_status = request.POST.get(
            'alive_status'
        )

        member.remarks = request.POST.get(
            'remarks'
        )

        family_id = request.POST.get(
            'family'
        )

        if family_id:

            member.family = get_object_or_404(
                Family,
                id=family_id
            )

        if request.FILES.get(
            'profile_photo'
        ):

            member.profile_photo = (
                request.FILES.get(
                    'profile_photo'
                )
            )

        if request.FILES.get(
            'ayushman_card_file'
        ):

            member.ayushman_card_file = (
                request.FILES.get(
                    'ayushman_card_file'
                )
            )

        if request.FILES.get(
            'aadhaar_card_file'
        ):

            member.aadhaar_card_file = (
                request.FILES.get(
                    'aadhaar_card_file'
                )
            )

        if request.FILES.get(
            'abha_card_file'
        ):

            member.abha_card_file = (
                request.FILES.get(
                    'abha_card_file'
                )
            )

        member.save()

        return redirect(
            'member_detail',
            member_id=member.id
        )

    families = (
        Family.objects
        .all()
        .order_by(
            'family_name'
        )
    )

    return render(
        request,
        'member_detail.html',
        {
            'member': member,
            'families': families,
            'edit_mode': True
        }
    )


# =========================================================
# FORGOT PIN
# =========================================================

def forgot_pin(request):

    if request.user.is_authenticated:

        return redirect(
            'dashboard'
        )

    if request.method == 'POST':

        email = request.POST.get(
            'email',
            ''
        ).strip()

        try:

            user = User.objects.get(
                username='asha',
                email__iexact=(
                    'ashaanursing2026@gmail.com'
                )
            )

        except User.DoesNotExist:

            return render(
                request,
                'forgot_pin.html',
                {
                    'error': (
                        'Please enter the registered '
                        'ASHA Care email address.'
                    )
                }
            )

        uid = urlsafe_base64_encode(
            force_bytes(
                user.pk
            )
        )

        token = default_token_generator.make_token(
            user
        )

        reset_link = request.build_absolute_uri(
            f'/reset-pin/{uid}/{token}/'
        )

        send_mail(

            subject=(
                'ASHA Care - Reset Your PIN'
            ),

            message=(

                'You requested to reset your '
                'ASHA Care PIN.\n\n'

                f'Open the following link to create '
                f'a new 6-digit PIN:\n\n'

                f'{reset_link}\n\n'

                'If you did not request this, you can '
                'safely ignore this email.'
            ),

            from_email=None,

            recipient_list=[
                'ashaanursing2026@gmail.com'
            ],

            fail_silently=False
        )

        return render(
            request,
            'forgot_pin.html',
            {
                'success': (
                    'A PIN reset link has been sent to '
                    'ashaanursing2026@gmail.com.'
                )
            }
        )

    return render(
        request,
        'forgot_pin.html'
    )


# =========================================================
# RESET PIN
# =========================================================

def reset_pin(
    request,
    uidb64,
    token
):

    if request.user.is_authenticated:

        return redirect(
            'dashboard'
        )

    try:

        uid = urlsafe_base64_decode(
            uidb64
        ).decode()

        user = User.objects.get(
            pk=uid
        )

    except (
        TypeError,
        ValueError,
        OverflowError,
        User.DoesNotExist
    ):

        user = None

    if (
        user is None
        or not default_token_generator.check_token(
            user,
            token
        )
    ):

        return render(
            request,
            'reset_pin.html',
            {
                'error': (
                    'This PIN reset link is invalid '
                    'or has expired.'
                ),

                'valid_link': False
            }
        )

    if request.method == 'POST':

        new_pin = request.POST.get(
            'new_pin',
            ''
        ).strip()

        confirm_pin = request.POST.get(
            'confirm_pin',
            ''
        ).strip()

        if (
            len(new_pin) != 6
            or not new_pin.isdigit()
        ):

            return render(
                request,
                'reset_pin.html',
                {
                    'error': (
                        'PIN must contain exactly '
                        '6 digits.'
                    ),

                    'valid_link': True
                }
            )

        if new_pin != confirm_pin:

            return render(
                request,
                'reset_pin.html',
                {
                    'error': (
                        'The PINs do not match.'
                    ),

                    'valid_link': True
                }
            )

        user.set_password(
            new_pin
        )

        user.save()

        return render(
            request,
            'reset_pin.html',
            {
                'success': (
                    'Your PIN has been successfully '
                    'reset. You can now login with '
                    'your new PIN.'
                ),

                'valid_link': True,

                'reset_complete': True
            }
        )

    return render(
        request,
        'reset_pin.html',
        {
            'valid_link': True
        }
    )


# =========================================================
# ADD VILLAGE
# =========================================================

@login_required
def add_village(request):

    if request.method == 'POST':

        name = request.POST.get(
            'name'
        )

        total_houses = request.POST.get(
            'total_houses'
        )

        if (
            not total_houses
            or int(total_houses) < 1
        ):

            villages = (
                Village.objects
                .all()
                .order_by(
                    'village_number'
                )
            )

            return render(
                request,
                'add_village.html',
                {
                    'error': (
                        'Total houses must be at least 1.'
                    ),

                    'villages': villages
                }
            )

        last_village = (
            Village.objects
            .order_by(
                '-village_number'
            )
            .first()
        )

        village_number = (
            last_village.village_number + 1
            if last_village
            else 1
        )

        Village.objects.create(

            village_number=village_number,

            name=name,

            total_houses=int(
                total_houses
            )

        )

        return redirect(
            'add_village'
        )

    villages = (
        Village.objects
        .all()
        .order_by(
            'village_number'
        )
    )

    return render(
        request,
        'add_village.html',
        {
            'villages': villages
        }
    )


# =========================================================
# HOUSE DETAIL
# =========================================================

@login_required
def house_detail(
    request,
    village_id,
    house_number
):

    village = get_object_or_404(
        Village,
        id=village_id
    )

    if (
        house_number < 1
        or house_number > village.total_houses
    ):

        return render(
            request,
            'house_detail.html',
            {
                'village': village,

                'house_number': house_number,

                'families': [],

                'error': (
                    'Invalid house number.'
                )
            }
        )

    families = (
        Family.objects
        .filter(
            village=village,
            house_number=house_number
        )
        .prefetch_related(
            'members'
        )
        .order_by(
            'family_name'
        )
    )

    return render(
        request,
        'house_detail.html',
        {
            'village': village,

            'house_number': house_number,

            'families': families
        }
    )