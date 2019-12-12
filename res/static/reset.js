$(document).ready(function(){

    $('.reset_profile_button').click(function(){
        $.ajax({url: "/reset_profile",  
            success: function(result) { 
                window.location.href= "/";    
            }
        }); 
    });

    $('.remove_rating_button').click(function(){
        var profileItem = $(this).parent();
        var stringId = profileItem.attr('id')

        var arr = stringId.split('_')

        var index = parseInt(arr[2]) - 1

        $.ajax({url: "/reset_rating?index=" + index,  
            success: function(result) { 
                window.location.href= "/";    
            }
        }); 

    });
});