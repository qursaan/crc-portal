// storing tabs active component in localStorage
//
// based on plugin-helper.js, extended to store the domid of an active tab
//

(function($){

    var tabs_helper = {

	debug:false,

	////////// use local storage to remember the active son
	// xxx this is a bit fragile in that we assume the elements that need to have the 'active' class
	// are direct sons of the .persistent-active elements
	// it would be simple to overcome this weakness by requiring the template to set
	// .persistent-active-item on these elements active-able instead 
	store_active_domid : function (domid,active_domid) {
	    var key='active.'+domid;
	    if (tabs_helper.debug) messages.debug("storing for domid " + domid + " (key=" + key + ") active_domid=" + active_domid);
	    $.localStorage.setItem(key,active_domid);
	},
	// restore last status
	retrieve_last_active_domid : function (domid) {
	    var key='active.'+domid;
	    // don't do anything if nothing stored
	    var retrieved=$.localStorage.getItem(key);
	    // set default to undefined
	    if (retrieved==null) retrieved=undefined;
	    if (tabs_helper.debug) messages.debug ("retrieved active status for " + domid + " (key=" + key + ") -> " + retrieved);
	    return retrieved;
	},
	// tabs_helper.set_active_domid("tabs-resources","tab-resources-list")
	set_active_domid : function (domid,active_domid) {
	    if ( ! active_domid ) return;
	    if (tabs_helper.debug) messages.debug ("setting active for " + domid + " to active_domid=" + active_domid);
	    // build something like "#uldomid a[href='#active_domid']"
	    var selector="#"+domid+" a[href='#"+active_domid+"']";
	    $(selector).tab('show');
	},
	set_from_saved_active_domid : function (domid) {
	    var active_domid=tabs_helper.retrieve_last_active_domid (domid);
	    if (tabs_helper.debug) messages.debug("restoring active domid for domid " + domid + " -> " + active_domid);
	    tabs_helper.set_active_domid (domid,active_domid);
	},

	init_all_tabs : function () {
	    ////////// active
	    $('.persistent-active').each(function() {
		var domid=this.id;
		tabs_helper.set_from_saved_active_domid(domid);
	    });
	    // on all the children of the persistent-active element
	    $('.persistent-active>*').on('shown.bs.tab', function (e) {
		var active_domid=e.target;
		// at this point we have something like 
		// http://localhost:8080/portal/slice/ple.inria.f14#tab-resources-list
		active_domid=active_domid.hash.replace("#","");
		// find out the domid, which is for the nearest ancestor with class
		// persistent-active
		var domid=$(e.target).closest(".persistent-active").attr('id');
		tabs_helper.store_active_domid(domid,active_domid);
	    });
            // In Bootstrap 3, the tab receives 'shown.bs.tab' instead of 'shown'
            // see: http://bootply.com/bootstrap-3-migration-guide
	    // we just forward this event to the actual plugin in the tab
	    // 
            $('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
		// find the plugin object inside the tab content referenced by the current tabs
		$('.plugin', $($(e.target).attr('href'))).trigger('shown.bs.tab');
		$('.plugin', $($(e.target).attr('href'))).trigger('show');
            });
	},

    } // var tabs_helper

    $(tabs_helper.init_all_tabs);

})( jQuery );
