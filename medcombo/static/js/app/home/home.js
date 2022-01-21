/*------------------------------
----------- home.js ------------
------------------------------*/

//Functions
$(function() {
    /*------------------------------
    ----------- Search -------------
    ------------------------------*/
    $("#search").keyup(function(){
        _this = this;
        // Show only matching TR, hide rest of them
        $.each($("#my_list #id-text"), function() {
            if($(this).text().toLowerCase().indexOf($(_this).val().toLowerCase()) === -1){
                $(this).hide();
            }
            else {
                $(this).show();
            }
        });
    });
    /*------------------------------
    ----------- ./Search -----------
    ------------------------------*/

    /*------------------------------
    ---------- addClass ------------
    ------------------------------*/
    $('#id_phone, #id_country, #id_city').addClass('form-control');
    /*------------------------------
    ---------- ./addClass ----------
    ------------------------------*/
});

/*------------------------------
--------- Profile Links --------
------------------------------*/
function my_link(my_url) {
	$(location).attr('href',my_url);
}
/*------------------------------
------- ./Profile Links --------
------------------------------*/

/*------------------------------
------ Adicional Scripts -------
------------------------------*/
$('#product-img').on('change', function(event) {
    var inputFile = event.currentTarget;
    if(inputFile.files[0].name.length <= 30) {
        $(inputFile).parent()
            .find('.custom-file-label')
            .html(inputFile.files[0].name.substring(0,25));
    }
    else {
        $(inputFile).parent()
            .find('.custom-file-label')
            .html(inputFile.files[0].name.substring(0,25)+'...');
    }
});

function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            $('#product-img-reload')
                .attr('src', e.target.result);
        };
        reader.readAsDataURL(input.files[0]);
    }
}
/*------------------------------
----- ./Adicional Scripts  -----
------------------------------*/