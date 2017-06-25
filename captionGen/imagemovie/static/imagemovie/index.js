
var file;
$(document).ready( function() {
    $(document).on('change', '.btn-file :file', function() {
    var input = $(this),
        label = input.val().replace(/\\/g, '/').replace(/.*\//, '');
    input.trigger('fileselect', [label]);
    });

    $('.btn-file :file').on('fileselect', function(event, label) {

        var input = $(this).parents('.input-group').find(':text'),
            log = label;

        if( input.length ) {
            input.val(log);
        } else {
            if( log ) alert(log);
        }

    });
    function readURL(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();

            reader.onload = function (e) {
                $('#img-upload').attr('src', e.target.result);
            }

            reader.readAsDataURL(input.files[0]);
        }
    }

    $("#imgInp").change(function(){
         $( "#img" ).children().hide();
        $( "#caption" ).children().hide();
        readURL(this);


    });
});

$(function () {
  /* 1. OPEN THE FILE EXPLORER WINDOW */
//  $(".btn-file").click(function () {
//    $("#imgInp").click();
//  });

  /* 2. INITIALIZE THE FILE UPLOAD COMPONENT */
  $("#imgInp").fileupload({
    dataType: 'json',
    done: function (e, data) {  /* 3. PROCESS THE RESPONSE FROM THE SERVER */
      if (data.result.is_valid) {
//        alert(data.result.caption);
//          $( "#caption" ).children().hide();
         $.each(data.result.caption, function(index, data){
               $('#caption').append('<p style="margin-top:15px;color:gray;font-size:16px"> <i class="glyphicon glyphicon-forward"></i> " '+ data + ' " </p>');
            });
//         $( "#img" ).children().hide();

         $('#img').append("<img class='img-responsive' src='"+data.result.url+"'/>");


//            alert(data.result.caption);
//          $('#img').append("<a href='" + data.result.url + "'>" + data.result.name + "</a>");
      }



    }
  });

});