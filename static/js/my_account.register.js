/*$(document).ready(function(){
    $("#registrationForm").validate({
        rules: {
          password: { 
                required: true
          }, 
          confirmpassword: { 
                required: true, equalTo: "#password"
          }
        }
    });
    // upload button
    $("#key-policy").change(function(){
        if(this.value=="upload"){
            jQuery("#upload_key").show();
        }else{
            jQuery("#upload_key").hide();
        }
    });
 });*/

$(document).ready(function() {
    $('#super_group').hide();
    $('#usertype').change(function() {
        if ($(this).val() == "3") {
            $('#super_group').show();
        } else {
            $('#super_group').hide();
        }
    });
    $(function () {
        if ($('#usertype').val() == "3") {
            $('#super_group').show();
        } else {
            $('#super_group').hide();
        }
        $('#usertype').val() == "-1";
    });

    $("#registrationForm").validate({
        rules: {
            password: {
                required: true,
                minlength: 5
            },
            confirmpassword: {
                required: true, minlength: 5, equalTo: "#password"
            }
        },
        messages: {
            password: {
                required: "Please provide a password",
                minlength: "Your password must be at least 5 characters long"
            },
            confirmpassword: {
                required: "Please provide a password",
                minlength: "Your password must be at least 5 characters long",
                equalTo: "Please enter the same password as above"
            }
        }
    });
});



