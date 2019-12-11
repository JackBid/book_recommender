$(document).ready(function(){

    $('.reset_profile_button').click(function(){
        $.ajax({url: "/reset_profile",  
            success: function(result) { 
                window.location.href= "/";    
            }
        }); 
    });

});