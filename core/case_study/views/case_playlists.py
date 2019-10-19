from random import shuffle

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from ..forms import PlaylistTagForm
from ..models import Tag, Playlist, CaseStudy


@login_required
def playlist_landing(request):
    playlists = Playlist.objects.filter(owner=request.user).order_by("-date_created")
    form = PlaylistTagForm()
    c = {
        "playlists": playlists,
        "form": form
    }
    return render(request, "playlist_landing.html", c)


@login_required
def create_new_playlist(request):
    tag_id = request.POST.get('tag_id', None)
    if tag_id:
        tag = get_object_or_404(Tag, pk=int(tag_id))
        case_list = list(
            CaseStudy.objects.filter(case_state=CaseStudy.STATE_PUBLIC, tagrelationship__tag=tag).values_list('id',
                                                                                                              flat=True))
        if len(case_list) > 1:
            shuffle(case_list)
            case_string = ','.join(str(e) for e in case_list)
            new_playlist = Playlist.objects.create(owner=request.user, tag=tag, date_created=timezone.now(), case_list=case_string)
    else:
        tag = None
        case_list = list(CaseStudy.objects.filter(case_state=CaseStudy.STATE_PUBLIC).values_list('id', flat=True))
        if len(case_list) > 1:
            shuffle(case_list)
            case_string = ','.join(str(e) for e in case_list)
            new_playlist = Playlist.objects.create(owner=request.user, tag=tag, date_created=timezone.now(), case_list=case_string)
    if case_list:
        return JsonResponse({
            "success": True,
            "message": "Your playlist was successfully created!"
        })
    return JsonResponse({
        "success": False,
        "message": "An error has occurred. This is likely due to there being no cases for the specified tag. Please try again."
    })


@login_required
def refresh_playlist(request):
    playlist_id = request.POST.get('playlist_id', None)
    playlist = get_object_or_404(Playlist, pk=int(playlist_id))
    if playlist.tag:
        case_list = list(
            CaseStudy.objects.filter(case_state=CaseStudy.STATE_PUBLIC, tagrelationship__tag=playlist.tag).values_list('id',
                                                                                                              flat=True))
        if len(case_list) > 1:
            shuffle(case_list)
            case_string = ','.join(str(e) for e in case_list)
            playlist.case_list = case_string
            playlist.current_position = 0
            playlist.save()
    else:
        case_list = list(CaseStudy.objects.filter(case_state=CaseStudy.STATE_PUBLIC).values_list('id', flat=True))
        if len(case_list) > 1:
            shuffle(case_list)
            case_string = ','.join(str(e) for e in case_list)
            playlist.case_list = case_string
            playlist.current_position = 0
            playlist.save()
    if playlist.case_list:
        return JsonResponse({
            "success": True,
            "message": "Your playlist was successfully refreshed!"
        })
    return JsonResponse({
        "success": False,
        "message": "There are not enough cases to create a playlist for this tag."
    })


@login_required
def delete_playlist(request):
    playlist_id = request.POST.get('playlist_id', None)
    playlist = get_object_or_404(Playlist, pk=int(playlist_id))
    playlist.delete()
    success = True if not playlist.id else False
    return JsonResponse({'success': success})