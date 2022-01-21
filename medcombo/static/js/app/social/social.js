/*------------------------------
---------- social.js -----------
------------------------------*/

//Functions
$(function() {
    /*------------------------------
    ----------- Search -------------
    ------------------------------*/
    $("#search-user").keyup(function () {
        var url = $("#url_id").attr("data-contact-url");
        var user = $('#search-user').val();
        $.ajax({                      
            url: url,                    
            data: {
                'user': user       
            },
            success: function (data) {   
				$("#list_chat_url").html(data);
			}
        });
    });
    /*------------------------------
    ----------- ./Search -----------
    ------------------------------*/

    /*------------------------------
    --------- Select List ----------
    ------------------------------*/
    $('#list_chat_url li').click(function(){
        var selected = $(this).hasClass("chat_highlight");
        $("#list_chat_url li").removeClass("chat_highlight");
        if(!selected) $(this).addClass("chat_highlight");
    });
    /*------------------------------
    --------- ./Select List --------
    ------------------------------*/
});