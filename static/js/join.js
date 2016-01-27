jQuery(document).ready(function(){

    jQuery("#joinForm").validate({
        rules: {
          pi_password: {
                required: true
          },
          confirmpassword: {
                required: true, equalTo: "#password"
          },
          root_authorithy_hrn: {
              required: true
          },
          site_name: {
              required: true
          },
          site_login_base: {
              required: true
          },
          site_abbreviated_name: {
              required: true
          },
          site_url: {
              required: true
          },
          site_latitude: {
              required: true
          },
          site_longitude: {
              required: true
          },
          pi_first_name: {
              required: true
          },
          pi_last_name: {
              required: true
          },
          pi_title: {
              required: true
          },
          pi_phone: {
              required: true
          },
          pi_email: {
              required: true
          },
/*
          address_line1: {
              required: true
          },

          address_line2: {
              required: true
          },
          address_line3: {
              required: true
          },

          address_city: {
              required: true
          },
          address_postalcode: {
              required: true
          },
          address_state: {
              required: true
          },

          address_country: {
              required: true
          },
*/
        }
    });
 });
