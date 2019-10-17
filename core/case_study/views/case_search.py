from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponseRedirect, JsonResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from datetime import datetime, timedelta

from ..forms import CaseStudyForm, CaseStudyTagForm, MedicalHistoryForm, MedicationForm, OtherForm  # , CaseTagForm
from ..models import Tag, TagRelationship, CaseStudy, MedicalHistory, Medication, Attempt, Comment, Other, Question

from django.db.models import Q

@login_required
def search(request):
    get = request.GET
    cases = CaseStudy.objects.filter(case_state=CaseStudy.STATE_PUBLIC)

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
    tag_list = get.getlist('tag_choice')
    if len(tag_list) != 0:
        filter_ids = []
        for case in cases:
            case_tags = TagRelationship.objects.filter(case_study=case)
            case_tags_list = []
            for tag in case_tags:
                case_tags_list.append(tag.tag.name)
            if(set(tag_list).issubset(set(case_tags_list))):
                filter_ids.append(case.id)
        tag_cases = cases.filter(id__in=[item for item in filter_ids])

    # Staff only
    anon_cases = None
    if get.get("staff_choice") is not None:
        anon_cases = cases.filter(created_by__is_staff=True)

    # all tags
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
        "get": get,

        "cases": cases,

        "key_words": keywords,
        "tag_choices": get.getlist('tag_choice'),
        "staff_choice": get.get("staff_choice")
    }

    return render(request,"search.html",c)


@login_required
def advsearch(request):
    get = request.GET
    cases = CaseStudy.objects.filter(case_state=CaseStudy.STATE_PUBLIC)

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
        filter_ids = []
        for case in cases:
            case_tags = TagRelationship.objects.filter(case_study=case)
            case_tags_list = []
            for tag in case_tags:
                case_tags_list.append(tag.tag.name)
            if(set(tag_list).issubset(set(case_tags_list))):
                filter_ids.append(case.id)
        tag_cases = cases.filter(id__in=[item for item in filter_ids])

    # Medical Histories
    mhx_cases = None
    mhx_list = get.getlist('mhx_choice')
    if len(mhx_list) != 0:
        filter_ids = []
        for case in cases:
            case_mhxs = MedicalHistory.objects.filter(case_study=case)
            case_mhxs_list = []
            for mhx in case_mhxs:
                case_mhxs_list.append(mhx.body)
            if(set(mhx_list).issubset(set(case_mhxs_list))):
                filter_ids.append(case.id)
        mhx_cases = cases.filter(id__in=[item for item in filter_ids])

    # Medicines
    medicine_cases = None
    medicine_list = get.getlist('medicine_choice')
    if len(medicine_list) != 0:
        filter_ids = []
        for case in cases:
            case_medicines = Medication.objects.filter(case_study=case)
            case_medicines_list = []
            for medicine in case_medicines:
                case_medicines_list.append(medicine.name)
                # if medicine.name in medicine_list:
            if(set(medicine_list).issubset(set(case_medicines_list))):
                filter_ids.append(case.id)
        medicine_cases = cases.filter(id__in=[item for item in filter_ids])

    # Others
    other_cases = None
    other_list = get.getlist('other_choice')
    if len(other_list) != 0:
        filter_ids = []
        for case in cases:
            case_others = Other.objects.filter(case_study=case)
            case_others_list = []
            for other in case_others:
                case_others_list.append(other.other_body)
            if(set(other_list).issubset(set(case_others_list))):
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
        if sex_choices[0] == 'Male':
            sex_cases = cases.filter(sex='M')
        elif sex_choices[0] == 'Female':
            sex_cases = cases.filter(sex='F')
        elif sex_choices[0] == 'Both':
            sex_cases = cases

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
        max_scr = ''

    # Questions
    question_cases = None
    question_list=get.getlist('question_choice')
    if len(question_list) != 0:
        filter_ids = []
        for case in cases:
            question = case.question.body
            if question in question_list:
                filter_ids.append(case.id)
        question_cases = cases.filter(id__in=[item for item in filter_ids])

    # Staff only
    anon_cases = None
    if get.get("staff_choice") is not None:
        anon_cases = cases.filter(created_by__is_staff=True)

    tags = Tag.objects.filter()
    sexes = ['Both', 'Male', 'Female']

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
        others_list.append(each.other_body)
    distinct_others = set(others_list)

    questions = Question.objects.filter()
    questions_list = []
    for each in questions:
        questions_list.append(each.body)
    distinct_questions = set(questions_list)

    # find the intersections of the filters that were used
    filters = [key_cases, tag_cases, mhx_cases, medicine_cases, other_cases, sex_cases, date_cases,
               score_cases, age_cases, height_cases, weight_cases, scr_cases, question_cases, anon_cases]
    for each_filter in filters:
        if each_filter is not None:
            cases = cases.intersection(each_filter)

    # attach respective average score, total attempts, tags to the case studies
    for case in cases:
        case.average = case.get_average_score()
        if case.average is None: # no attempts made
            case.average = 0
        elif case.average % 1 == 0: # average is a whole number
            case.average = int(case.average)
        case.attempts = len(Attempt.objects.filter(case_study=case))
        case.tags = TagRelationship.objects.filter(case_study=case)

    c = {
        "key_words": keywords,

        "tags": tags,
        "sexes": sexes,
        "mhxes": distinct_mhxes,
        "medicines": distinct_medicines,
        "others": distinct_others,
        "questions": distinct_questions,

        "get": get,
        "cases": cases,

        "sex_choices": get.getlist('sex_choice'),
        "tag_choices": get.getlist('tag_choice'),
        "mhx_choices": get.getlist('mhx_choice'),
        "medicine_choices": get.getlist('medicine_choice'),
        "other_choices": get.getlist('other_choice'),
        "question_choices": get.getlist('question_choice'),

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
