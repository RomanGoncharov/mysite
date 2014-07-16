var chat_room_id = undefined;
var last_received = 0;

/**
 * Initialize chat:
 * - Set the room id
 * - Generate the html elements (chat box, forms & inputs, etc)
 * - Sync with server
 * @param chat_room_id the id of the chatroom
 * @param html_el_id the id of the html element where the chat html should be placed
 * @return
 */
function init_chat(chat_id, html_el_id) {
	chat_room_id = chat_id;
	layout_and_bind(html_el_id);
	sync_messages();
}

var img_dir = "{{STATIC_URL}}/img/";

/**
 * Asks the server which was the last message sent to the room, and stores it's id.
 * This is used so that when joining the user does not request the full list of
 * messages, just the ones sent after he logged in. 
 * @return
 */
function sync_messages() {
    $.ajax({
        type: 'POST',
        data: {id:window.chat_room_id},
        url:'/chat/sync/',
		dataType: 'json',
		success: function (json) {
        	last_received = json.last_message_id;
		}        
    });
	
	setTimeout("get_messages()", 2000);
}

/**
 * Generate the Chat box's HTML and bind the ajax events
 * @param target_div_id the id of the html element where the chat will be placed 
 */
function layout_and_bind(html_el_id) {
		// layout stuff

		
		// event stuff
    	$("#chat-form").submit( function () {
            var $inputs = $(this).find('input');
            var values = {};
            
            $inputs.each(function(i,el) { 
            	values[el.name] = $(el).val();
            });
			values['chat_room_id'] = window.chat_room_id;
        	
        	$.ajax({
                data: values,
                dataType: 'json',
                type: 'post',
                url: '/chat/send/'
            });
            $('#chat-form .message').val('');
            return false;
	});
};

/**
 * Gets the list of messages from the server and appends the messages to the chatbox
 */
function get_messages() {
    $.ajax({
        type: 'POST',
        data: {id:window.chat_room_id, offset: window.last_received},
        url:'/chat/receive/',
		dataType: 'json',
		success: function (json) {
			var scroll = false;
		
			// first check if we are at the bottom of the div, if we are, we shall scroll once the content is added
			var $containter = $("#chat-messages-container");
			if ($containter.scrollTop() == $containter.attr("scrollHeight") - $containter.height())
				scroll = true;

			// add messages
			$.each(json, function(i,m){
                var avatar = '<img src="'+ m.avatar+'" width="32" height="32">'
				if (m.type == 's')
					$('#chat-messages').append('<div class="system">'+ replace_emoticons(m.message));
				else if (m.type == 'm')
                    $('#chat-messages').append(
                                '<div class="media">'+
                                   '<a class="pull-left" href="#">'+
                                        '<img class="media-object" src="'+m.avatar+'" width="32" height="32">' +
                                   '</a>'+
                                    '<div class="media-body ">'+
                                        '<div class="media-heading author">' + m.author +'</div>'+
                                        replace_emoticons(m.message)+
                                '</div></div>');
//					$('#chat-messages').append('<div class="message">'+ avatar +'<div class="author">'+m.author+'</div>'+replace_emoticons(m.message) + '</div><div class="timestamp">'+ m.timestamp+'</div>');
				else if (m.type == 'j') 	
					$('#chat-messages').append('<div class="join">' +m.author+' has joined</div>');
				else if (m.type == 'l') 	
					$('#chat-messages').append('<div class="leave">'+m.author+' has left</div>');
					
				last_received = m.id;
			})
			
			// scroll to bottom
			if (scroll)
				$("#chat-messages-container").animate({ scrollTop: $("#chat-messages-container").attr("scrollHeight") }, 500);
		}        
    });
    
    // wait for next
    setTimeout("get_messages()", 2000);
}

/**
 * Tells the chat app that we are joining
 */
function chat_join() {
	jQuery.ajax({
		async: false,
        type: 'POST',
        data: {chat_room_id:window.chat_room_id},
        url:'/chat/join/',
        dataType: "json"
    });
}

/**
 * Tells the chat app that we are leaving
 */
function chat_leave() {
	$.ajax({
		async: false,
        type: 'POST',
        data: {chat_room_id:window.chat_room_id},
        url:'/chat/leave/'
    });
}

// attach join and leave events
$(window).load(function(){chat_join()});
$(window).unload(function(){chat_leave()});

// emoticons
var emoticons = {                 
	'>:D' : 'emoticon_evilgrin.png',
	':D' : 'emoticon_grin.png',
	'=D' : 'emoticon_happy.png',
	':\\)' : 'emoticon_smile.png',
	':O' : 'emoticon_surprised.png',
	':P' : 'emoticon_tongue.png',
	':\\(' : 'emoticon_unhappy.png',
	':3' : 'emoticon_waii.png',
	';\\)' : 'emoticon_wink.png',
	'\\(ball\\)' : 'sport_soccer.png'
}

/**
 * Regular expression maddness!!!
 * Replace the above strings for their img counterpart
 */
function replace_emoticons(text) {
	$.each(emoticons, function(char, img) {
		re = new RegExp(char,'g');
		// replace the following at will
		text = text.replace(re, '<img src="'+img_dir+img+'" />');
	});
	return text;
}