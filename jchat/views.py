# -*- encoding: UTF-8 -*-
'''
Chat application views, some are tests... some are not
@author: Federico Cáceres <fede.caceres@gmail.com>
'''
from datetime import datetime

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext
from django.contrib.auth.models import User
from models import Room, Message
from forms import CreateRoomForm
from django.core.urlresolvers import reverse

@login_required()
def main(request):
    form = CreateRoomForm()
    rooms = Room.objects.all()
    if request.method == 'POST':
        form = CreateRoomForm(data=request.POST)
        if form.is_valid():
            room = form.save()
            return HttpResponseRedirect(reverse("chat:room", args=[room.id]))
    return render_to_response('main_page_chat.html', RequestContext(request, {"rooms": rooms, 'form': form}))


@login_required
def room_view(request, id):
    try:
        room = Room.objects.get(id=id)
    except Room.DoesNotExist:
        raise Http404
    return render_to_response('room.html', RequestContext(request, {'room': room}))

@csrf_exempt
@login_required
def send(request):
    '''
    Expects the following POST parameters:
    chat_room_id
    message
    '''
    p = request.POST
    r = Room.objects.get(id=int(p['chat_room_id']))
    r.say(request.user, p['message'])
    return HttpResponse('')


@csrf_exempt
@login_required
def sync(request):
    '''Return last message id

    EXPECTS the following POST parameters:
    id
    '''
    if request.method != 'POST':
        raise Http404
    post = request.POST

    if not post.get('id', None):
        raise Http404

    r = Room.objects.get(id=post['id'])
    
    lmid = r.last_message_id()    
    
    return HttpResponse(jsonify({'last_message_id':lmid}))


@csrf_exempt
@login_required
def receive(request):
    '''
    Returned serialized data
    
    EXPECTS the following POST parameters:
    id
    offset
    
    This could be useful:
    @see: http://www.djangosnippets.org/snippets/622/
    '''
    if request.method != 'POST':
        raise Http404
    post = request.POST

    if not post.get('id', None) or not post.get('offset', None):
        raise Http404
    
    try:
        room_id = int(post['id'])
    except:
        raise Http404

    try:
        offset = int(post['offset'])
    except:
        offset = 0
    
    r = Room.objects.get(id=room_id)

    m = r.messages(offset)

    
    return HttpResponse(jsonify(m, ['id','author','message','timestamp','avatar', 'type']))

@csrf_exempt
@login_required
def join(request):
    '''
    Expects the following POST parameters:
    chat_room_id
    message
    '''
    p = request.POST
    r = Room.objects.get(id=int(p['chat_room_id']))
    r.join(request.user)
    return HttpResponse('')

@csrf_exempt
@login_required
def leave(request):
    '''
    Expects the following POST parameters:
    chat_room_id
    message
    '''
    p = request.POST
    r = Room.objects.get(id=int(p['chat_room_id']))
    r.leave(request.user)
    return HttpResponse('')

@csrf_exempt
@login_required
def test(request):
    '''Test the chat application'''

    u = User.objects.get(id=1) # always attach to first user id
    r = Room.objects.get_or_create(u)

    return render_to_response('chat/chat.html', {'js': ['/media/js/mg/chat.js'], 'chat_id': r.pk}, context_instance=RequestContext(request))


def jsonify(object, fields=None, to_dict=False):
    '''Simple convert model to json'''
    try:
        import json
    except:
        import django.utils.simplejson as json
 
    out = []
    if type(object) not in [dict,list,tuple] :
        for i in object:
            tmp = {}
            if fields:
                for field in fields:
                    if field == 'avatar':
                        tmp[field] = i.author.get_profile().get_avatar_url()
                        continue
                    tmp[field] = unicode(i.__getattribute__(field))
            else:
                for attr, value in i.__dict__.iteritems():
                    tmp[attr] = value
            out.append(tmp)
    else:
        out = object
    if to_dict:
        return out
    else:
        return json.dumps(out)
