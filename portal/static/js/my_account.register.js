/* 
# Jquery for password matching and Affiliation list

Authors:
  Mohammed Yasin Rahman <mohammed-yasin.rahman@lip6.fr>
Copyright 2013, UPMC Sorbonne Universités / LIP6

*/
jQuery(document).ready(function(){
    
    jQuery("#registrationForm").validate({
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
    jQuery("#key-policy").change(function(){
        if(this.value=="upload"){
            jQuery("#upload_key").show();
        }else{
            jQuery("#upload_key").hide();
        }
    });
 });

jQuery(function() {
    var availableTags = [
      "iMinds",
      "IT Innovation",
      "UPMC",
      "Fraunhofer",
      "TUB",
      "UEDIN",
      "INRIA",
      "NICTA",
      "ATOS",
      "UTH",
      "NTUA",
      "UNIVBRIS",
      "i2CAT",
      "EUR",
      "DANTE Limited",
      "UC",
      "NIA"
    ];
    jQuery( "#aff_list" ).autocomplete({
      source: availableTags
    });
  });

