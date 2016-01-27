/**
 * Description: display a query result in a Google map
 * Copyright (c) 2012-2013 UPMC Sorbonne Universite - INRIA
 * License: GPLv3
 */

/* BUGS:
 * - infowindow is not properly reopened when the maps does not have the focus
 */

(function($){

    // events that happen in the once-per-view range
    var debug=false;
    debug=true;

    // this now should be obsolete, rather use plugin_debug in plugin.js
    // more on a on-per-record basis
    var debug_deep=false;
    // debug_deep=true;

    var GoogleMap = Plugin.extend({

        init: function(options, element) {
	    this.classname="googlemap";
            this._super(options, element);

            /* Member variables */
            // query status
            this.received_all = false;
            this.received_set = false;
            this.in_set_backlog = [];

            // we keep a couple of global hashes
	    // lat_lon --> { marker, <ul> }
	    // id --> { <li>, <input> }
	    this.by_lat_lon = {};
	    // locating checkboxes by DOM selectors might be abstruse, as we cannot safely assume 
	    // all the items will belong under the toplevel <div>
	    this.by_id = {};
	    this.by_init_id = {};

            /* Events */
	    // xx somehow non of these triggers at all for now
            this.elmt().on('show', this, this.on_show);
            this.elmt().on('shown.bs.tab', this, this.on_show);
            this.elmt().on('resize', this, this.on_resize);

            var query = manifold.query_store.find_analyzed_query(this.options.query_uuid);
            this.object = query.object;

	    // see querytable.js for an explanation
	    var keys = manifold.metadata.get_key(this.object);
	    this.canonical_key = (keys && keys.length == 1) ? keys[0] : undefined;
	    // 
	    this.init_key = this.options.init_key;
	    // have init_key default to canonical_key
	    this.init_key = this.init_key || this.canonical_key;
	    // sanity check
	    if ( ! this.init_key ) messages.warning ("QueryTable : cannot find init_key");
	    if ( ! this.canonical_key ) messages.warning ("QueryTable : cannot find canonical_key");
	    if (debug) messages.debug("googlemap: canonical_key="+this.canonical_key+" init_key="+this.init_key);

            //// Setup query and record handlers 
	    // this query is the one about the slice itself 
	    // event related to this query will trigger callbacks like on_new_record
            this.listen_query(options.query_uuid);
	    // this one is the complete list of resources
	    // and will be bound to callbacks like on_all_new_record
            this.listen_query(options.query_all_uuid, 'all');

            /* GUI setup and event binding */
            this.initialize_map();
        }, // init

        /* PLUGIN EVENTS */

        on_show: function(e) {
	    if (debug) messages.debug("googlemap.on_show");
            var googlemap = e.data;
            google.maps.event.trigger(googlemap.map, 'resize');
        }, 
	// dummy to see if this triggers at all
        on_resize: function(e) {
	    if (debug) messages.debug("googlemap.on_resize ...");
        }, 

        /* GUI EVENTS */

        /* GUI MANIPULATION */

        initialize_map: function() {
            this.markerCluster = null;
            //create empty LatLngBounds object in order to automatically center the map on the displayed objects
            this.bounds = new google.maps.LatLngBounds();
            var center = new google.maps.LatLng(this.options.latitude, this.options.longitude);
            var myOptions = {
                zoom: this.options.zoom,
                center: center,
		        scrollwheel: false,
                mapTypeId: google.maps.MapTypeId.ROADMAP,
            }
	    
            var domid = this.options.plugin_uuid + '--' + 'googlemap';
	    var elmt = document.getElementById(domid);
            this.map = new google.maps.Map(elmt, myOptions);
            this.infowindow = new google.maps.InfoWindow();
        }, // initialize_map

	// return { marker: gmap_marker, ul : <ul DOM> }
	create_marker_struct: function (object,lat,lon) {
	    // the DOM fragment
	    var dom = $("<p>").addClass("geo").append(object+"(s)");
	    var ul = $("<ul>").addClass("geo");
	    dom.append(ul);
	    // add a gmap marker to the mix
	    var marker = new google.maps.Marker({
		position: new google.maps.LatLng(lat, lon),
                title: object,
		// gmap can deal with a DOM element but not a jquery object
                content: dom.get(0),
        }); 
        //extend the bounds to include each marker's position
        this.bounds.extend(marker.position);
	    return {marker:marker, ul:ul};
	},

	// given an input <ul> element, this method inserts a <li> with embedded checkbox 
	// for displaying/selecting the resource corresponding to the input record
	// returns the created <input> element for further checkbox manipulation
	create_record_checkbox: function (record,ul,checked) {
	    var checkbox = $("<input>", {type:'checkbox', checked:checked, class:'geo'});
	    var id=record[this.canonical_key];
	    var init_id=record[this.init_key];
	    // xxx use init_key to find out label - or should we explicitly accept an incoming label_key ?
	    var label=init_id;
	    ul.append($("<li>").addClass("geo").append(checkbox).
		      append($("<span>").addClass("geo").append(label)));
	    // hash by id and by init_id 
	    this.by_id[id]=checkbox;
            this.by_init_id[init_id] = checkbox;
	    //
	    // the callback for when a user clicks
	    // NOTE: this will *not* be called for changes done by program
	    var self=this;
	    checkbox.change( function (e) {
		manifold.raise_event (self.options.query_uuid, this.checked ? SET_ADD : SET_REMOVED, id);
	    });
	    return checkbox;
	},
	    
	warning: function (record,message) {
	    try {messages.warning (message+" -- "+this.key+"="+record[this.key]); }
	    catch (err) {messages.warning (message); }
	},
	    
	// retrieve DOM checkbox and make sure it is checked/unchecked
	set_checkbox_from_record: function(record, checked) {
	    var init_id=record[this.init_key];
	    var checkbox = this.by_init_id [ init_id ];
	    if (checkbox) checkbox.prop('checked',checked);
	    else this.warning(record, "googlemap.set_checkbox_from_record - not found "+init_id);
	}, 

	set_checkbox_from_data: function(id, checked) {
	    var checkbox = this.by_id [ id ];
	    if (checkbox) checkbox.prop('checked',checked);
	    else messages.warning("googlemap.set_checkbox_from_data - id not found "+id);
	}, 

	// this record is *in* the slice
        new_record: function(record) {
	    if (debug_deep) messages.debug ("googlemap.new_record");
            if (!(record['latitude'])) return false;
	    
            // get the coordinates
            var latitude=unfold.get_value(record['latitude']);
            var longitude=unfold.get_value(record['longitude']);
            var lat_lon = latitude + longitude;

    	    // check if we've seen anything at that place already
    	    // xxx might make sense to allow for some fuzziness, 
    	    // i.e. consider 2 places equal if not further away than 300m or so...
    	    var marker_s = this.by_lat_lon [lat_lon];
    	    if ( marker_s == null ) {
        	marker_s = this.create_marker_struct (this.object, latitude, longitude);
        	this.by_lat_lon [ lat_lon ] = marker_s;
        	this.arm_marker(marker_s.marker, this.map);
	    }
	    
    	    // now add a line for this resource in the marker
    	    // xxx should compute checked here ?
    	    // this is where the checkbox will be appended
    	    var ul=marker_s.ul;
    	    var checkbox = this.create_record_checkbox (record, ul, false);
        }, // new_record

        arm_marker: function(marker, map) {
	    if (debug_deep) messages.debug ("arm_marker content="+marker.content);
            var googlemap = this;
            google.maps.event.addListener(marker, 'click', function () {
                googlemap.infowindow.close();
                googlemap.infowindow.setContent(marker.content);
                googlemap.infowindow.open(map, marker);
            });
        }, // arm_marker

        /*************************** QUERY HANDLER ****************************/

        /*************************** RECORD HANDLER ***************************/
        on_new_record: function(record) {
	    if (debug_deep) messages.debug("googlemap.on_new_record");
            if (this.received_all)
                // update checkbox for record
                this.set_checkbox_from_record(record, true);
            else
                // store for later update of checkboxes
                this.in_set_backlog.push(record);
        },

        on_clear_records: function(record) {
	    if (debug_deep) messages.debug("googlemap.on_clear_records");
        },

        // Could be the default in parent
        on_query_in_progress: function() {
	    if (debug) messages.debug("googlemap.on_query_in_progress (spinning)");
            this.spin();
        },

        on_query_done: function() {
	        if (debug) messages.debug("googlemap.on_query_done");	    
            if (this.received_all) {
                this.unspin();
	        }
            this.received_set = true;
        },

        on_field_state_changed: function(data) {
	    if (debug_deep) messages.debug("googlemap.on_field_state_changed");	    
            switch(data.request) {
            case FIELD_REQUEST_ADD:
            case FIELD_REQUEST_ADD_RESET:
                this.set_checkbox_from_data(data.value, true);
                break;
            case FIELD_REQUEST_REMOVE:
            case FIELD_REQUEST_REMOVE_RESET:
                this.set_checkbox_from_data(data.value, false);
                break;
            default:
                break;
            }
        },


        // all : this 

        on_all_new_record: function(record) {
	    if (debug_deep) messages.debug("googlemap.on_all_new_record");
            this.new_record(record);
        },

        on_all_clear_records: function() {
	    if (debug) messages.debug("googlemap.on_all_clear_records");	    
        },

        on_all_query_in_progress: function() {
	    if (debug) messages.debug("googlemap.on_all_query_in_progress (spinning)");
            // XXX parent
            this.spin();
        },

        on_all_query_done: function() {
	    if (debug) messages.debug("googlemap.on_all_query_done");

            // MarkerClusterer
            var markers = [];
            $.each(this.by_lat_lon, function (k, s) { markers.push(s.marker); });
            this.markerCluster = new MarkerClusterer(this.map, markers, {zoomOnClick: false});
            google.maps.event.addListener(this.markerCluster, "clusterclick", function (cluster) {
                var cluster_markers = cluster.getMarkers();
                var bounds  = new google.maps.LatLngBounds();
                $.each(cluster_markers, function(i, marker){
                    bounds.extend(marker.getPosition()); 
                });
                //map.setCenter(bounds.getCenter(), map.getBoundsZoomLevel(bounds));
                this.map.fitBounds(bounds);
            });
            //now fit the map to the bounds
            this.map.fitBounds(this.bounds);
            // Fix the zoom of fitBounds function, it's too close when there is only 1 marker
            if(markers.length==1){
                this.map.setZoom(this.map.getZoom()-4);
            }
            var googlemap = this;
            if (this.received_set) {
                /* ... and check the ones specified in the resource list */
                $.each(this.in_set_backlog, function(i, record) {
                    googlemap.set_checkbox_from_record(record, true);
                });
		// reset 
		googlemap.in_set_backlog = [];
                this.unspin();
            }
            this.received_all = true;

        } // on_all_query_done
    });
        /************************** PRIVATE METHODS ***************************/

    $.plugin('GoogleMap', GoogleMap);

})(jQuery);
