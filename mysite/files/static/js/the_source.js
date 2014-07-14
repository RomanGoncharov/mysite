/**
 * Created by Romka on 10.02.14.
 */
function like_request(num){

    jQuery.ajax({
        type: 'get',
        url: 'like/'+num.toString()+'/',
        data: '',
        dataType: 'json',
        success:function(data){
            $('#counter'+num).animate({opacity: 0}, 'fast', function() {
                $(this)
                    .text(data.like)
                    .animate({opacity: 1},'fast');
            });
        }
    });

}