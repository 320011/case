from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from datetime import datetime, timedelta

from .forms import CaseStudyForm, CaseStudyTagForm, MedicalHistoryForm, MedicationForm, OtherForm  # , CaseTagForm
from .models import Tag, TagRelationship, CaseStudy, MedicalHistory, Medication, Attempt, Comment, Other

from django.db.models import Q


@login_required
def start_new_case(request):
    case = CaseStudy.objects.create(created_by=request.user)
    return HttpResponseRedirect(
        reverse("cases:create-new-case", kwargs={"case_study_id": case.id}))


@login_required
def create_new_case(request, case_study_id):
    # returns object (case_study), and boolean specifying whether an object was created
    case_study, created = CaseStudy.objects.get_or_create(pk=case_study_id)
    relevant_tags = TagRelationship.objects.filter(case_study=case_study)  # return Tags for that case_study
    medical_histories = MedicalHistory.objects.filter(case_study=case_study)
    medications = Medication.objects.filter(case_study=case_study)
    others = Other.objects.filter(case_study=case_study)
    # Check if the choice was in years format, if yes, integer division by 12.
    if case_study.age:
        if case_study.age_type == 'Y':
            case_study.age = case_study.age // 12
    if request.method == "POST":
        # Fixes mutable error
        request.POST = request.POST.copy()
        # obtain forms with fields populated from POST request
        case_study_form = CaseStudyForm(request.POST, instance=case_study)
        case_study_tag_form = CaseStudyTagForm(request.POST)
        medical_history_form = MedicalHistoryForm(request.POST)
        medication_form = MedicationForm(request.POST)
        other_form = OtherForm(request.POST)

        # if user adds medical history
        if request.POST["submission_type"] == "medical_history":
            body = request.POST["body"]  # obtain medical history body
            if body:
                # get or create new medical history relationship in the database
                mhx, created = MedicalHistory.objects.get_or_create(body=body, case_study=case_study)
                if created:
                    messages.success(request, 'Medical History added!')
                else:
                    messages.error(request,
                                   'This medical history already exists. If it is a repeated condition, please include when the condition occured.')

            medical_history_form = MedicalHistoryForm(request.POST)
            return render(request, "create_new_case.html",
                          {
                              "case_study_form": case_study_form,
                              "tags": relevant_tags,
                              "medical_histories": medical_histories,
                              "medications": medications,
                              "others": others,
                              # "case_study_question_form": case_study_question_form,
                              "case_study_tag_form": case_study_tag_form,
                              "medical_history_form": medical_history_form,
                              "medication_form": medication_form,
                              "other_form": other_form,
                          })

        # if user adds medication
        elif request.POST["submission_type"] == "medication":
            name = request.POST["name"]  # obtain medication name
            if name:
                # get or create new medication relationship in the database
                medication, created = Medication.objects.get_or_create(name=name, case_study=case_study)
                if created:
                    messages.success(request, 'Medication added!')
                else:
                    messages.error(request, 'This medication already exists.')
            medication_form = MedicationForm(request.POST)
            return render(request, "create_new_case.html",
                          {
                              "case_study_form": case_study_form,
                              "tags": relevant_tags,
                              "medical_histories": medical_histories,
                              "medications": medications,
                              "others": others,
                              "case_study_tag_form": case_study_tag_form,
                              "medical_history_form": medical_history_form,
                              "medication_form": medication_form,
                          })
            # if user adds other
        elif request.POST["submission_type"] == "other":
            other_body = request.POST["other_body"]  # obtain other
            if other_body:
                # get or create new medication relationship in the database
                other, created = Other.objects.get_or_create(other_body=other_body, case_study=case_study)
                if created:
                    messages.success(request, 'Other added!')
                else:
                    messages.error(request, 'This other item already exists.')
            other_form = OtherForm(request.POST)
            return render(request, "create_new_case.html",
                          {
                              "case_study_form": case_study_form,
                              "tags": relevant_tags,
                              "medical_histories": medical_histories,
                              "medications": medications,
                              "others": others,
                              "case_study_tag_form": case_study_tag_form,
                              "medical_history_form": medical_history_form,
                              "medication_form": medication_form,
                              "other_form": other_form,
                          })
        # if user adds tag
        elif request.POST["submission_type"] == "tag" and request.POST["tag_choice"]:
            # Create a new tag relationship for this case study.
            tag = Tag.objects.get(pk=int(request.POST["tag_choice"]))  # get tag object for tag_choice
            # get or create new tag relationship in the database
            created_tag_relationship, created = TagRelationship.objects.get_or_create(tag=tag, case_study=case_study)
            if created:
                messages.success(request, 'Tag added!')
            else:
                messages.error(request, 'This tag already exists.')

            case_study_tag_form = CaseStudyTagForm()
            return render(request, "create_new_case.html",
                          {
                              "case_study_form": case_study_form,
                              "tags": relevant_tags,
                              "medical_histories": medical_histories,
                              "medications": medications,
                              "others": others,
                              # "case_study_question_form": case_study_question_form,
                              "case_study_tag_form": case_study_tag_form,
                              "medical_history_form": medical_history_form,
                              "medication_form": medication_form,
                              "other_form": other_form,
                          })

        elif request.POST["submission_type"] == "save":
            # Checking for the type on submission, if years, store the value as months
            if request.POST['age_type'] == 'Y':
                request.POST['age'] = int(request.POST['age']) * 12
            if case_study_form.is_valid():
                case_study_form.save()
                # When page is re rendered, the value from the database is taken, so if years, render the correct value
                if request.POST['age_type'] == 'Y':
                    request.POST['age'] = int(request.POST['age']) // 12
                case_study_form = CaseStudyForm(request.POST, instance=case_study)
                messages.success(request, 'Case Study saved!')
                return render(request, "create_new_case.html",
                              {
                                  "case_study_form": case_study_form,
                                  "tags": relevant_tags,
                                  "medical_histories": medical_histories,
                                  "medications": medications,
                                  "others": others,
                                  "case_study_tag_form": case_study_tag_form,
                                  "medical_history_form": medical_history_form,
                                  "medication_form": medication_form,
                                  "other_form": other_form,
                              })
        elif request.POST["submission_type"] == "submit":
            if request.POST['age_type'] == 'Y':
                request.POST['age'] = int(request.POST['age']) * 12
            if case_study_form.is_valid():
                case_study_form.save()
                case_study.date_submitted = timezone.now()
                case_study.save()
                messages.success(request, 'Case Study created!')
                return HttpResponseRedirect(reverse('cases:view-case', args=[case_study.id]))
            else:
                if request.POST['age_type'] == 'Y':
                    request.POST['age'] = int(request.POST['age']) // 12
                case_study_form = CaseStudyForm(request.POST, instance=case_study)
                return render(request, "create_new_case.html",
                              {
                                  "case_study_form": case_study_form,
                                  "tags": relevant_tags,
                                  "medical_histories": medical_histories,
                                  "medications": medications,
                                  "others": others,
                                  # "case_study_question_form": case_study_question_form,
                                  "case_study_tag_form": case_study_tag_form,
                                  "medical_history_form": medical_history_form,
                                  "medication_form": medication_form,
                                  "other_form": other_form,
                              })
        else:
            return render(request, "create_new_case.html",
                          {
                              "case_study_form": case_study_form,
                              "tags": relevant_tags,
                              "medical_histories": medical_histories,
                              "medications": medications,
                              "others": others,
                              "case_study_tag_form": case_study_tag_form,
                              "medical_history_form": medical_history_form,
                              "medication_form": medication_form,
                              "other_form": other_form,
                          })
    else:
        case_study_form = CaseStudyForm(instance=case_study)
        case_study_tag_form = CaseStudyTagForm()
        medical_history_form = MedicalHistoryForm()
        medication_form = MedicationForm()
        other_form = OtherForm()
    return render(request, "create_new_case.html",
                  {
                      "case_study_form": case_study_form,
                      "tags": relevant_tags,
                      "medical_histories": medical_histories,
                      "medications": medications,
                      "others": others,
                      "case_study_tag_form": case_study_tag_form,
                      "medical_history_form": medical_history_form,
                      "medication_form": medication_form,
                      "other_form": other_form,
                  })




@login_required
def view_case(request, case_study_id):
    case_study = get_object_or_404(CaseStudy, pk=case_study_id)
    mhx = MedicalHistory.objects.filter(case_study=case_study)
    medications = Medication.objects.filter(case_study=case_study)
    tags = TagRelationship.objects.filter(case_study=case_study)
    total_average = case_study.get_average_score()
    user_average = case_study.get_average_score(user=request.user)
    user_attempts = Attempt.objects.filter(case_study=case_study, user=request.user).count()
    total_attempts = Attempt.objects.filter(case_study=case_study).count()
    comments = Comment.objects.filter(case_study=case_study_id).order_by("-comment_date")
    c = {
        "attempts": {
            "total_average": total_average,
            "total_attempts": total_attempts,
            "user_average": user_average,
            "user_attempts": user_attempts
        },
        "case": case_study,
        "mhx": mhx,
        "medications": medications,
        "tags": tags,
        "comments": comments
    }
    return render(request, "view_case.html", c)


def validate_answer(request, case_study_id):
    case = get_object_or_404(CaseStudy, pk=case_study_id)
    choice = request.GET.get('choice', None)
    success = False
    # Get message
    if choice == case.answer:
        success = True
    message = "<strong>Correct Answer: " + case.answer + "</strong><br><em>" + case.get_answer_from_character(
        case.answer) + "</em><br>You answered incorrectly. Your answer was <strong>" + choice + "</strong>, " + case.get_answer_from_character(
        choice)
    if success:
        message = "<strong>Correct Answer: " + case.answer + "</strong><br><em>" + case.get_answer_from_character(
            case.answer) + "</em><br>You answered correctly."
    # Get attempts information
    Attempt.objects.create(user_answer=choice, case_study=case, user=request.user, attempt_date=timezone.now())
    total_average = case.get_average_score()
    user_average = case.get_average_score(user=request.user)
    user_attempts = Attempt.objects.filter(case_study=case, user=request.user).count()
    total_attempts = Attempt.objects.filter(case_study=case).count()
    # Get comments
    comments = Comment.objects.filter(case_study=case_study_id)
    comments_json = serializers.serialize('json', comments)
    data = {
        'attempts': {
            'total_average': total_average,
            'total_attempts': total_attempts,
            'user_average': user_average,
            'user_attempts': user_attempts
        },
        'success': success,
        'answer_message': message,
        'feedback': case.feedback,
        'comments': comments_json
    }
    return JsonResponse(data)


def submit_comment(request, case_study_id):
    case = get_object_or_404(CaseStudy, pk=case_study_id)
    body = request.GET.get('body', None)
    is_anon = request.GET.get('is_anon', None).capitalize()
    # Create comment 
    if request.user.is_tutor: 
        comment = Comment.objects.create(comment=body, case_study=case, user=request.user, is_anon=False,
                                        comment_date=timezone.now())
    else: 
        comment = Comment.objects.create(comment=body, case_study=case, user=request.user, is_anon=is_anon,
                                        comment_date=timezone.now())
    data = {
        'comment': {
            'body': body,
            'date': timezone.now(),
            'is_anon': comment.is_anon == 'True'
        },
        'user': {
            'name': request.user.get_full_name(),
            'is_staff': request.user.is_staff,
            'is_tutor': request.user.is_tutor
        }
    }
    return JsonResponse(data)





@login_required
def search(request):
    get = request.GET
    cases = CaseStudy.objects.filter(is_submitted=True, is_deleted=False)

    # Keywords
    key_cases = None
    keywords = get.get("key_words")
    if keywords is not None and len(keywords) !=0:
        key_cases = CaseStudy.objects.none()
        kw_list=keywords.split()
        for k in kw_list:
            keyword_cases = cases.filter(Q(description__icontains=k) | Q(height__icontains=k) |
                Q(weight__icontains=k) | Q(scr__icontains=k) | Q(age_type__icontains=k) |
                Q(age__icontains=k) | Q(answer_a__icontains=k) | Q(answer_b__icontains=k) |
                Q(answer_c__icontains=k) | Q(answer_d__icontains=k))
            key_cases = key_cases.union(keyword_cases)
    else:
        keywords = ''
    
    # Tags
    tag_cases = None
    tag_list=get.getlist('tag_choice')
    if len(tag_list) != 0:
        tag_cases = CaseStudy.objects.none()
        filter_ids = []
        for case in cases:
            case_tags = TagRelationship.objects.filter(case_study=case)
            for tag in case_tags:
                if tag.tag.name in tag_list:
                    filter_ids.append(case.id)   
        tag_cases = cases.filter(id__in=[item for item in filter_ids])

    # Staff only
    anon_cases = None
    if get.get("staff_choice") is not None:
        anon_cases = cases.filter(created_by__is_staff=True)

    #all tags
    tags = Tag.objects.filter()
    sexes = CaseStudy.SEX_CHOICES

    # find the intersections of the filters that were used
    filters = [key_cases, tag_cases, anon_cases]
    for each_filter in filters:
        if each_filter is not None:
            cases = cases.intersection(each_filter)

    # attach respective tags to the case studies
    for case in cases:
        case.tags = TagRelationship.objects.filter(case_study=case)

    c = {
        "tags": tags,
        "sexes": sexes,
        "get":get,

        "cases": cases,

        "key_words": keywords,
        "tag_choices": get.getlist('tag_choice'),
        "staff_choice": get.get("staff_choice")
    }

    return render(request,"search.html",c)




@login_required
def advsearch(request):
    get = request.GET
    cases = CaseStudy.objects.filter(is_submitted=True, is_deleted=False)

    # Keywords
    key_cases = None
    keywords = get.get("key_words")
    if keywords is not None and len(keywords) !=0: 
        key_cases = CaseStudy.objects.none()
        kw_list=keywords.split()
        for k in kw_list:
            keyword_cases = cases.filter(Q(description__icontains=k) | Q(height__icontains=k) |
                Q(weight__icontains=k) | Q(scr__icontains=k) | Q(age_type__icontains=k) |
                Q(age__icontains=k) | Q(answer_a__icontains=k) | Q(answer_b__icontains=k) |
                Q(answer_c__icontains=k) | Q(answer_d__icontains=k))
            key_cases = key_cases.union(keyword_cases)
    else:
        keywords = ''

    # Tags
    tag_cases = None
    tag_list=get.getlist('tag_choice')
    if len(tag_list) != 0:
        # tag_cases = CaseStudy.objects.none()
        filter_ids = []
        for case in cases:
            case_tags = TagRelationship.objects.filter(case_study=case)
            for tag in case_tags:
                if tag.tag.name in tag_list:
                    filter_ids.append(case.id)
        tag_cases = cases.filter(id__in=[item for item in filter_ids])

    # Medical Histories
    mhx_cases = None
    mhx_list = get.getlist('mhx_choice')
    if len(mhx_list) != 0:
        # mhx_cases = CaseStudy.objects.none()
        filter_ids = []
        for case in cases:
            case_mhxs = MedicalHistory.objects.filter(case_study=case)
            for mhx in case_mhxs:
                if mhx.body in mhx_list:
                    filter_ids.append(case.id)
        mhx_cases = cases.filter(id__in=[item for item in filter_ids])

    # Medicines
    medicine_cases = None
    medicine_list = get.getlist('medicine_choice')
    if len(medicine_list) != 0:
        # medicine_cases = CaseStudy.objects.none()
        filter_ids = []
        for case in cases:
            case_medicines = Medication.objects.filter(case_study=case)
            for medicine in case_medicines:
                if medicine.name in medicine_list:
                    filter_ids.append(case.id)
        medicine_cases = cases.filter(id__in=[item for item in filter_ids])

    # Others
    other_cases = None
    other_list = get.getlist('other_choice')
    if len(other_list) != 0:
        # other_cases = CaseStudy.objects.none()
        filter_ids = []
        for case in cases:
            case_others = Other.objects.filter(case_study=case)
            for other in case_others:
                if other.other_body in other_list:
                    filter_ids.append(case.id)
        other_cases = cases.filter(id__in=[item for item in filter_ids])

    
    # Date submitted
    date_cases = None
    start_date = get.get("before_date")
    if start_date is not None and start_date is not '':
        date_cases = cases.filter(date_submitted__gte=start_date)
    else:
        start_date = 0
    
    end_date = get.get("after_date")
    if end_date is not None and end_date is not '':
        # A day is added to make the selected end date inclusive
        end = datetime.strptime(end_date, "%Y-%m-%d")
        end_inclusive = end + timedelta(days=1) - timedelta(seconds=1)
        if start_date == 0: # if only end date selected
            date_cases = cases.filter(date_submitted__lte=end_inclusive)
        else: # both start and end dates selected
            date_cases = date_cases.filter(date_submitted__lte=end_inclusive)
    else:
        end_date = 0


    # Average score
    score_cases = None
    min_score = get.get("min_score")
    if min_score is not None and min_score is not '':
        # score_cases = cases.filter(score__gte=12*int(get.get("min_score")))
        min_score_ids = []
        for case in cases:
            if case.get_average_score() >= float(min_score):
                min_score_ids.append(case.id)
        score_cases = cases.filter(id__in=[item for item in min_score_ids])
    else:
        min_score=''

    max_score = get.get("max_score")
    if max_score is not None and max_score is not '':
        max_score_ids = []
        if min_score == '':
            for case in cases:
                if case.get_average_score() <= float(max_score):
                    max_score_ids.append(case.id)
            score_cases = cases.filter(id__in=[item for item in max_score_ids])
        else:
            for case in score_cases:
                if case.get_average_score() <= float(max_score):
                    max_score_ids.append(case.id)
            score_cases = score_cases.filter(id__in=[item for item in max_score_ids])
    else:
        max_score=''
    

    # Age
    age_cases = None
    min_age = get.get("min_age")
    if min_age is not None and min_age is not '':
        age_cases = cases.filter(age__gte=12*int(get.get("min_age")))
    else:
        min_age=''

    max_age = get.get("max_age")
    if max_age is not None and max_age is not '':
        if min_age == '':
            age_cases = cases.filter(age__lte=12*int(get.get("max_age")))
        else:
            age_cases = age_cases.filter(age__lte=12*int(get.get("max_age")))
    else:
        max_age=''


    # Sexes
    sex_cases = None
    sex_choices = get.getlist('sex_choice')
    if len(sex_choices) != 0:
        # sex_choices = sex_choices
        sex_cases = cases.filter(sex__in=[s for s in sex_choices])
    

    # Height
    height_cases = None
    min_height = get.get("min_height")
    if min_height is not None and min_height is not '':
        height_cases = cases.filter(height__gte=min_height)
    else:
        min_height=''

    max_height = get.get("max_height")
    if max_height is not None and max_height is not '':
        if min_height == '':
            height_cases = cases.filter(height__lte=max_height)
        else:
            height_cases = height_cases.filter(height__lte=max_height)
    else:
        max_height=''

    
    # Weight
    weight_cases = None
    min_weight = get.get("min_weight")
    if min_weight is not None and min_weight is not '':
        weight_cases = cases.filter(weight__gte=min_weight)
    else:
        min_weight=''

    max_weight = get.get("max_weight")
    if max_weight is not None and max_weight is not '':
        if min_weight == '':
            weight_cases = cases.filter(weight__lte=max_weight)
        else:
            weight_cases = weight_cases.filter(weight__lte=max_weight)
    else:
        max_weight=''

    
    # SCr
    scr_cases = None
    min_scr = get.get("min_scr")
    if min_scr is not None and min_scr is not '':
        scr_cases = cases.filter(scr__gte=min_scr)
    else:
        min_scr=''

    max_scr = get.get("max_scr")
    if max_scr is not None and max_scr is not '':
        if min_scr == '':
            scr_cases = cases.filter(scr__lte=max_scr)
        else:
            scr_cases = scr_cases.filter(scr__lte=max_scr)
    else:
        max_scr=''


    # Staff only
    anon_cases = None
    if get.get("staff_choice") is not None:
        anon_cases = cases.filter(created_by__is_staff=True)


    #all distinct tags, sexes, medications, medical histories
    tags = Tag.objects.filter()
    sexes = CaseStudy.SEX_CHOICES

    mhxes = MedicalHistory.objects.filter()
    mhxes_list = []
    for each in mhxes:
        mhxes_list.append(each.body)
    distinct_mhxes = set(mhxes_list)

    medicines = Medication.objects.filter()
    medicines_list = []
    for each in medicines:
        medicines_list.append(each.name)
    distinct_medicines = set(medicines_list)

    others = Other.objects.filter()
    others_list = []
    for each in others:
        others_list.append(each.body)
    distinct_others = set(others_list)

    # find the intersections of the filters that were used
    filters = [key_cases, tag_cases, mhx_cases, medicine_cases, other_cases, sex_cases,
                date_cases, score_cases, age_cases, height_cases, weight_cases, scr_cases]
    for each_filter in filters:
        if each_filter is not None:
            cases = cases.intersection(each_filter)

    # attach respective average score, total attempts, tags to the case studies
    for case in cases:
        case.average = case.get_average_score()
        case.attempts = len(Attempt.objects.filter(case_study=case))
        case.tags = TagRelationship.objects.filter(case_study=case)

    c = {
        "key_words": keywords,

        "tags": tags,
        "sexes": sexes,
        "mhxes": distinct_mhxes,
        "medicines": distinct_medicines,
        "others": distinct_others,
    
        "get": get,
        "cases": cases,

        "sex_choices": get.getlist('sex_choice'),
        "tag_choices": get.getlist('tag_choice'),
        "mhx_choices": get.getlist('mhx_choice'),
        "medicine_choices": get.getlist('medicine_choice'),
        "other_choices": get.getlist('other_choice'),

        "before_date": start_date,
        "after_date": end_date,
        "min_score": min_score,
        "max_score": max_score,
        "min_age": min_age,
        "max_age": max_age,
        "min_height": min_height,
        "max_height": max_height,
        "min_weight": min_weight,
        "max_weight": max_weight,
        "min_scr": min_scr,
        "max_scr": max_scr,
        "staff_choice": get.get("staff_choice"),
    }

    return render(request, "advsearch.html", c)
