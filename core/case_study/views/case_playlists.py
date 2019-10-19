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


def create_new_playlist(request):
    tag_id = request.POST.get('tag_id', None)
    if tag_id:
        tag = get_object_or_404(Tag, pk=int(tag_id))
        case_list = list(
            CaseStudy.objects.filter(case_state=CaseStudy.STATE_PUBLIC, tagrelationship__tag=tag).values_list('id',
                                                                                                              flat=True))
        shuffle(case_list)
        case_string = ','.join(str(e) for e in case_list)
        Playlist.objects.create(owner=request.user, tag=tag, date_created=timezone.now(), case_list=case_string)
    else:
        tag = None
        case_list = list(CaseStudy.objects.filter(case_state=CaseStudy.STATE_PUBLIC).values_list('id', flat=True))
        shuffle(case_list)
        case_string = ','.join(str(e) for e in case_list)
        Playlist.objects.create(owner=request.user, tag=tag, date_created=timezone.now(), case_list=case_string)
    return JsonResponse({
        "success": True,
        "message": "Your playlist was successfully created!"
    })
