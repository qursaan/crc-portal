/**
 * Description: display simple lists like slices or testbeds
 * Copyright (c) 2012 UPMC Sorbonne Universite - INRIA
 * License: GPLv3
 */

(function($){

    var debug=false;
    debug=true

    var SimpleList = Plugin.extend ({

	init: function (options, element) {
	    this.classname = options.classname;
	    this._super (options, element);
	    this.buffered_records = [];
        this.listen_query(options.query_uuid);
        /* Optional parameter warning_msg */
        if(options.warning_msg != "unknown-setting-warning_msg"){
            this.warning_msg = options.warning_msg;
        }else{
            this.warning_msg = "No Result";
        }
	}, 

        on_query_in_progress: function() {
	    messages.debug("on_query_in_progress");
            this.spin(true);
        },

        on_query_done: function() {
	        this._display_table();
            this.unspin();
            console.log("query simple list done");
            console.log(this);
            console.log(this.buffered_records);
        },
        
        on_new_record: function(record) {
	    this.buffered_records.push(record);
        },

    /* Private methods */

	_display_table: function() {
	    var self=this;
        var $plugindiv = this.elmt();
        var options = this.options;
        // locate the <table> element; with datatables in the way,
        // this might not be a direct son of the div-plugin
        var $table = $plugindiv.find("table."+this.classname).first();
        // also we may or may not have a header
        var $tbody = $table.find("tbody."+this.classname).first();
        var use_datatables = $table.hasClass("with-datatables");
	    var rows=self.buffered_records;
	    self.buffered_records=[];
        if (debug){
		    messages.debug($plugindiv.attr('id') + " udt= " + use_datatables + " rows="+rows.length);
	    }
        // check if rows contains results related to the object key
        object_key = this.options.key.split('.');
        if (rows.length == 0 || rows[0][object_key[0]].length == 0) {
    		if (use_datatables){
                this._datatables_set_message ($table, $tbody, unfold.warning(self.warning_msg));
	    	}else{
        	    this._regular_set_message ($table, $tbody, unfold.warning(self.warning_msg));
            }
		    return;
        }

        if (typeof rows[0].error != 'undefined') {
		    var error="ERROR: " + rows[0].error;
		    if (use_datatables){
                this._datatables_set_message ($table, $tbody, unfold.error(error));
		    }else{
        	    this._regular_set_message ($table, $tbody, unfold.error(error));
            }
		    return;
        }

	    if (use_datatables){
		    this._datatables_update_table($table, $tbody, rows, options.key);
	    }else{
  		    this._regular_update_table($table, $tbody, rows, options.key, this.classname);
        }
	},

	_regular_set_message: function ($table, $tbody, message) {
	    $tbody.html("<tr><td>"+message+"</td></tr>");
	},

	_regular_update_table: function ($table, $tbody, rows, key, classname) {
            if (debug)
		messages.debug('regular_update_table ' + rows.length + " rows" + 
			       " key=" + key + " classname=" + this.classname);
	    var self=this;
	    var html=$.map(rows, function (row) {
		var value = row;
		$.each(key.split('.'), function(i, k) {
                    if ($.isArray(value)) {
			value = $.map(value, function(val, i) { return val[k]});
                    } else {
			value = value[k];
                    }
		});
		if ($.isArray(value)) {
                    return $.map(value, function(val, i) { 
			return self._html_row ( self._cell (key, val), this.classname); 
		    });
		} else {
                    return self._html_row ( self._cell (key, value), this.classname);
		}
            }).join();
    	    $tbody.html(html);
	},
    
	_datatables_set_message: function ($table, $tbody, message) {
            $table.dataTable().fnClearTable();
            $table.dataTable().fnAddData( [ message ] );
            $table.dataTable().fnDraw();
	},

	_datatables_update_table: function ($table, $tbody, rows, key) {
	    if (debug) messages.debug('datatables_update_table ' + rows.length + " rows");
	    $table.dataTable().fnClearTable();
	    // the lambda here returns a [[]] because $.map is kind of broken; as per the doc:
	    // The function can return any value to add to the array. 
	    // A returned array will be flattened into the resulting array.
	    // this is wrong indeed so let's work around that
	    var self=this;
	    $table.dataTable().fnAddData( $.map(rows, function (row) { return [[ self._cell (key,row[key]) ]] }) );
	    $table.dataTable().fnDraw();
	},
    
	_html_row: function (cell, classname) { 
            return "<tr><td class='"+classname+"'>"+cell+"</td></tr>"; 
	},
    
	// hard-wire a separate presentation depending on the key being used....
	_cell: function (key, value) {
            if (key == 'slice.slice_hrn') {
		return "<i class='icon-play-circle'></i><a href='/portal/slice/" + value + "'>" + value + "</a>";
            } else if (key == 'platform') {
		return "<i class='icon-play-circle'></i><a href='/portal/platform/" + value + "'>" + value + "</a>";
            } else {
		return value;
            }
	},
    });

    $.plugin('SimpleList', SimpleList);

})( jQuery );
