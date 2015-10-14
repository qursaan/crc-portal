//
// storing toggle's status in localStorage
// NOTE that localStorage only stores strings, so true becomes "true"
//
var plugin_helper = {

    debug:false,

    ////////// use local storage to remember open/closed toggles
    store_toggle_status : function (domid,status) {
	var key='toggle.'+domid;
	if (plugin_helper.debug) messages.debug("storing toggle status " + status + " for " + domid + " key=" + key);
	$.localStorage.setItem(key,status);
    },
    // restore last status
    retrieve_last_toggle_status : function (domid) {
	var key='toggle.'+domid;
	// don't do anything if nothing stored
	var retrieved=$.localStorage.getItem(key);
	// set default to true
	if (retrieved==null) retrieved="true";
	if (plugin_helper.debug) messages.debug ("retrieved toggle status for " + domid + " (key=" + key + ") -> " + retrieved);
	return retrieved;
    },
    set_toggle_status : function (domid,status) {
	var plugindiv=$('#'+domid);
	var showbtn=$('#show-'+domid);
	var hidebtn=$('#hide-'+domid);
	if (status=="true")	{ plugindiv.slideDown(); hidebtn.show(); showbtn.hide(); }
	else			{ plugindiv.slideUp();   hidebtn.hide(); showbtn.show(); }
	plugin_helper.store_toggle_status(domid,status);
    },
    set_from_saved_toggle_status : function (domid) {
	var previous_status=plugin_helper.retrieve_last_toggle_status (domid);
	if (plugin_helper.debug) messages.debug("restoring initial status for domid " + domid + " -> " + previous_status);
	plugin_helper.set_toggle_status (domid,previous_status);
    },


    // triggered upon $(document).ready
    init_all_plugins : function() {
	// plugins marked as persistent start with all 3 parts turned off
	// let us first make sure the right parts are turned on 
	$('.persistent-toggle').each(function() {
	    var domid=this.id.replace('complete-','');
	    plugin_helper.set_from_saved_toggle_status(domid);
	});
	// program the hide buttons so they do the right thing
	$('.plugin-hide').each(function() {
	    $(this).click(function () { 
		var domid=this.id.replace('hide-','');
		plugin_helper.set_toggle_status(domid,"false");
	    })});
	// same for show buttons
	$('.plugin-show').each(function() {
	    $(this).click(function () { 
		var domid=this.id.replace('show-','');
		plugin_helper.set_toggle_status(domid,"true");
	    })});
	// arm tooltips
	$('.plugin-tooltip').each(function(){ $(this).tooltip({'selector':'','placement':'right'}); });
    },
} // global var plugin_helper

/* upon document completion, we locate all the hide and show areas, 
 * and configure their behaviour 
 */
$(document).ready(plugin_helper.init_all_plugins)

