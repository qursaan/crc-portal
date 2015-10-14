// -*- js-indent-tab:2 -*-
/**
 * Description: display a query result in a slickgrid-powered table
 * Copyright (c) 2012-2013 UPMC Sorbonne Universite - INRIA
 * License: GPLv3
 */

/* 
 * WARNINGS
 *
 * This is very rough for now and not deemed working
 * 
 * WARNINGS
 */

/* ongoing adaptation to slickgrid 
   still missing are
. checkboxes really running properly
. ability to sort on columns (should be straightforward
  IIRC this got broken when moving to dataview, see dataview doc
. ability to sort on the checkboxes column 
  (e.g. have resources 'in' the slice show up first)
  not quite clear how to do this
. searching
. filtering
. style improvement
. rendering in the sliceview - does not use up all space, 
  this is different from the behaviour with simpleview
*/

(function($) {

    var debug=false;
    debug=true
    var debug_deep=false;
//    debug_deep=true;

    var QueryGrid = Plugin.extend({

        init: function(options, element) {
	    this.classname="querygrid";
            this._super(options, element);

            /* Member variables */
	    // in general we expect 2 queries here
	    // query_uuid refers to a single object (typically a slice)
	    // query_all_uuid refers to a list (typically resources or users)
	    // these can return in any order so we keep track of which has been received yet
            this.received_all_query = false;
            this.received_query = false;

//            // We need to remember the active filter for filtering
//            this.filters = Array(); 

            // an internal buffer for records that are 'in' and thus need to be checked 
            this.buffered_records_to_check = [];

            /* Events */
            this.elmt().on('show', this, this.on_show);

            var query = manifold.query_store.find_analyzed_query(this.options.query_uuid);
            this.object = query.object;

	    //// we need 2 different keys
	    // * canonical_key is the primary key as derived from metadata (typically: urn)
	    //   and is used to communicate about a given record with the other plugins
	    // * init_key is a key that both kinds of records 
	    //   (i.e. records returned by both queries) must have (typically: hrn or hostname)
	    //   in general query_all will return well populated records, but query
	    //   returns records with only the fields displayed on startup
	    var keys = manifold.metadata.get_key(this.object);
	    this.canonical_key = (keys && keys.length == 1) ? keys[0] : undefined;
	    // 
	    this.init_key = this.options.init_key;
	    // have init_key default to canonical_key
	    this.init_key = this.init_key || this.canonical_key;
	    // sanity check
	    if ( ! this.init_key ) messages.warning ("QueryGrid : cannot find init_key");
	    if ( ! this.canonical_key ) messages.warning ("QueryGrid : cannot find canonical_key");
	    if (debug) messages.debug("querygrid: canonical_key="+this.canonical_key+" init_key="+this.init_key);

            /* Setup query and record handlers */
            this.listen_query(options.query_uuid);
            this.listen_query(options.query_all_uuid, 'all');

            /* GUI setup and event binding */
            this.initialize_table();
        },

        /* PLUGIN EVENTS */

        on_show: function(e) {
            var self = e.data;
            self.redraw_table();
        }, // on_show

        /* GUI EVENTS */

        /* GUI MANIPULATION */

        initialize_table: function() {
	    // compute columns based on columns and hidden_columns
	    this.slick_columns = [];
	    var all_columns = this.options.columns; // .concat(this.options.hidden_columns)
	    // xxx would be helpful to support a column_renamings options arg
	    // for redefining some labels like 'network_hrn' that really are not meaningful
	    for (c in all_columns) {
		var column=all_columns[c];
		this.slick_columns.push ( {id:column, name:column, field:column, 
					   cssClass: "querygrid-column-"+column,
					   width:100, minWidth:40, });
	    }
	    var checkbox_selector = new Slick.CheckboxSelectColumn({
		cssClass: "slick-checkbox"
	    });
	    this.slick_columns.push(checkbox_selector.getColumnDefinition());

	    // xxx should be extensible from caller with this.options.slickgrid_options 
	    this.slick_options = {
		enableCellNavigation: false,
		enableColumnReorder: true,
		showHeaderRow: true,
		syncColumnCellResize: true,
	    };

	    this.slick_data = [];
	    this.slick_dataview = new Slick.Data.UnfoldDataView();
// capturing for debug
window.dv=this.slick_dataview;
	    var self=this;
	    this.slick_dataview.onRowCountChanged.subscribe ( function (e,args) {
		self.slick_grid.updateRowCount();
		self.slick_grid.autosizeColumns();
		self.slick_grid.render();
	    });
	  
	    
	    var selector="#grid-"+this.options.domid;
	    if (debug_deep) {
		messages.debug("slick grid selector is " + selector);
		for (c in this.slick_columns) {
		    var col=this.slick_columns[c];
		    var msg="";
		    for (k in col) msg = msg+" col["+k+"]="+col[k];
		    messages.debug("slick_column["+c+"]:"+msg);
		}
	    }

	    this.slick_grid = new Slick.Grid(selector, this.slick_dataview, this.slick_columns, this.slick_options);
//	    this.slick_grid.setSelectionModel (new Slick.RowSelectionModel ({selectActiveRow: false}));
	    this.slick_grid.setSelectionModel (new Slick.UnfoldSelectionModel({selectActiveRow: false}));
	    this.slick_grid.registerPlugin (checkbox_selector);
	    // autotooltips: for showing the full column name when ellipsed
	    var auto_tooltips = new Slick.AutoTooltips ({ enableForHeaderCells: true });
	    this.slick_grid.registerPlugin (auto_tooltips);
	    
	    this.columnpicker = new Slick.Controls.ColumnPicker (this.slick_columns, this.slick_grid, this.slick_options)

        }, // initialize_table

        new_record: function(record) {
	    this.slick_data.push(record);
        },

        clear_table: function() {
	    this.slick_data=[];
	  this.slick_dataview.setItems(this.slick_data,this.init_key,this.canonical_key);
        },

        redraw_table: function() {
	    this.slick_grid.autosizeColumns();
            this.slick_grid.render();
        },

        show_column: function(field) {
	    console.log ("querygrid.show_column not yet implemented with slickgrid - field="+field);
        },

        hide_column: function(field) {
	    console.log("querygrid.hide_column not implemented with slickgrid - field="+field);
        },

        /*************************** QUERY HANDLER ****************************/

        on_filter_added: function(filter) {
            this.filters.push(filter);
            this.redraw_table();
        },

        on_filter_removed: function(filter) {
            // Remove corresponding filters
            this.filters = $.grep(this.filters, function(x) {
                return x != filter;
            });
            this.redraw_table();
        },
        
        on_filter_clear: function() {
            this.redraw_table();
        },

        on_field_added: function(field) {
            this.show_column(field);
        },

        on_field_removed: function(field) {
            this.hide_column(field);
        },

        on_field_clear: function() {
            alert('QueryGrid::clear_fields() not implemented');
        },

        /* XXX TODO: make this generic a plugin has to subscribe to a set of Queries to avoid duplicated code ! */
        /*************************** ALL QUERY HANDLER ****************************/

        on_all_filter_added: function(filter) {
            // XXX
            this.redraw_table();
        },

        on_all_filter_removed: function(filter) {
            // XXX
            this.redraw_table();
        },
        
        on_all_filter_clear: function() {
            // XXX
            this.redraw_table();
        },

        on_all_field_added: function(field) {
            this.show_column(field);
        },

        on_all_field_removed: function(field) {
            this.hide_column(field);
        },

        on_all_field_clear: function() {
            alert('QueryGrid::clear_fields() not implemented');
        },


        /*************************** RECORD HANDLER ***************************/

        on_new_record: function(record) {
            if (this.received_all_query) {
        	// if the 'all' query has been dealt with already we may turn on the checkbox
                this._set_checkbox_from_record(record, true);
            } else {
        	// otherwise we need to remember that and do it later on
        	if (debug) messages.debug("Remembering record to check, "+this.init_key+'='+ record[this.init_key]);
                this.buffered_records_to_check.push(record);
            }
        },

        on_clear_records: function() {
        },

        // Could be the default in parent
        on_query_in_progress: function() {
            this.spin();
        },

        on_query_done: function() {
            this.received_query = true;
    	    // unspin once we have received both
            if (this.received_all_query && this.received_query) {
		this._init_checkboxes();
		this.unspin();
	    }
        },
        
        on_field_state_changed: function(data) {
            switch(data.request) {
                case FIELD_REQUEST_ADD:
                case FIELD_REQUEST_ADD_RESET:
                    this._set_checkbox_from_data(data.value, true);
                    break;
                case FIELD_REQUEST_REMOVE:
                case FIELD_REQUEST_REMOVE_RESET:
                    this._set_checkbox_from_data(data.value, false);
                    break;
                default:
                    break;
            }
        },

        /* XXX TODO: make this generic a plugin has to subscribe to a set of Queries to avoid duplicated code ! */
        // all
        on_all_field_state_changed: function(data) {
            switch(data.request) {
                case FIELD_REQUEST_ADD:
                case FIELD_REQUEST_ADD_RESET:
                    this._set_checkbox_from_data(data.value, true);
                    break;
                case FIELD_REQUEST_REMOVE:
                case FIELD_REQUEST_REMOVE_RESET:
                    this._set_checkbox_from_data(data.value, false);
                    break;
                default:
                    break;
            }
        },

        on_all_new_record: function(record) {
            this.new_record(record);
        },

        on_all_clear_records: function() {
            this.clear_table();

        },

        on_all_query_in_progress: function() {
            // XXX parent
            this.spin();
        }, // on_all_query_in_progress

        on_all_query_done: function() {
	    var start=new Date();
	    if (debug) messages.debug("1-shot initializing slickgrid content with " + this.slick_data.length + " lines");
	    // use this.init_key as the key for identifying rows
	  this.slick_dataview.setItems (this.slick_data, this.init_key,this.canonical_key);
	    var duration=new Date()-start;
	    if (debug) messages.debug("setItems " + duration + " ms");
	    if (debug_deep) {
		// show full contents of first row app
		for (k in this.slick_data[0]) messages.debug("slick_data[0]["+k+"]="+this.slick_data[0][k]);
	    }
	    
            var self = this;
	    // if we've already received the slice query, we have not been able to set 
	    // checkboxes on the fly at that time (dom not yet created)
            $.each(this.buffered_records_to_check, function(i, record) {
		if (debug) messages.debug ("delayed turning on checkbox " + i + " record= " + record);
                self._set_checkbox_from_record(record, true);
            });
	    this.buffered_records_to_check = [];

            this.received_all_query = true;
	    // unspin once we have received both
            if (this.received_all_query && this.received_query) {
		this._init_checkboxes();
		this.unspin();
	    }

        }, // on_all_query_done

        /************************** PRIVATE METHODS ***************************/

        _set_checkbox_from_record : function(record, checked) {
	    var init_id = record[this.init_key];
	    if (debug) messages.debug("querygrid.set_checkbox_from_record, init_id="+init_id);
	    var index = this.slick_dataview.getIdxById(init_id);
            this._set_checkbox_from_index (index,checked);
	},

        _set_checkbox_from_data : function (id, checked) {
	    if (debug) messages.debug("querygrid.set_checkbox_from_data, id="+id);
	    // this is a local addition to mainstream dataview
	    // it's kind if slow in this first implementation (no hashing)
	    // but we should not notice that much
	    var index = this.slick_dataview.getIdxByIdKey(id,this.canonical_key);
            this._set_checkbox_from_index (index,checked);
        },

        _set_checkbox_from_index : function (index, checked) {
	  if (index === undefined) { messages.warn("querygrid.set_checkbox - cannot find index"); return;}
            if (checked === undefined) checked = true;
	    var selectedRows=this.slick_grid.getSelectedRows();
	    if (checked) // add index in current list
		selectedRows=selectedRows.concat(index);
	    else // remove index from current list
		selectedRows=selectedRows.filter(function(idx) {return idx!=index;});
	    // set new selection
	    this.slick_grid.setSelectedRows(selectedRows);
	},

// initializing checkboxes
// have tried 2 approaches, but none seems to work as we need it
// issue summarized in here 
// http://stackoverflow.com/questions/20425193/slickgrid-selection-changed-callback-how-to-tell-between-manual-and-programmat
	// arm the click callback on checkboxes
	_init_checkboxes_manual : function () {
	    // xxx looks like checkboxes can only be the last column??
	    var checkbox_col = this.slick_grid.getColumns().length-1; // -1 +1 =0
	    console.log ("checkbox_col="+checkbox_col);
	    var self=this;
	    console.log ("HERE 1 with "+this.slick_dataview.getLength()+" sons");
	    for (var index=0; index < this.slick_dataview.getLength(); index++) {
		// retrieve key (i.e. hrn) for this line
		var key=this.slick_dataview.getItem(index)[this.key];
		// locate cell <div> for the checkbox
		var div=this.slick_grid.getCellNode(index,checkbox_col);
		if (index <=30) console.log("HERE2 div",div," index="+index+" col="+checkbox_col);
		// arm callback on single son of <div> that is the <input>
		$(div).children("input").each(function () {
		    if (index<=30) console.log("HERE 3, index="+index+" key="+key);
		    $(this).click(function() {self._checkbox_clicked(self,this,key);});
		});
	    }
	},

	// onSelectedRowsChanged will fire even when 
	_init_checkboxes : function () {
	    console.log("_init_checkboxes");
	    var grid=this.slick_grid;
	    this.slick_grid.onSelectedRowsChanged.subscribe(function(){
		row_ids = grid.getSelectedRows();
		console.log(row_ids);
	    });
	},

	// the callback for when user clicks 
        _checkbox_clicked: function(querygrid,input,key) {
            // XXX this.value = key of object to be added... what about multiple keys ?
	    if (debug) messages.debug("querygrid click handler checked=" + input.checked + " key=" + key);
            manifold.raise_event(querygrid.options.query_uuid, input.checked?SET_ADD:SET_REMOVED, key);
            //return false; // prevent checkbox to be checked, waiting response from manifold plugin api
            
        },

	// xxx from this and down, probably needs further tweaks for slickgrid

        _querygrid_filter: function(oSettings, aData, iDataIndex) {
            var ret = true;
            $.each (this.filters, function(index, filter) { 
                /* XXX How to manage checkbox ? */
                var key = filter[0]; 
                var op = filter[1];
                var value = filter[2];

                /* Determine index of key in the table columns */
                var col = $.map(oSettings.aoColumns, function(x, i) {if (x.sTitle == key) return i;})[0];

                /* Unknown key: no filtering */
                if (typeof(col) == 'undefined')
                    return;

                col_value=unfold.get_value(aData[col]);
                /* Test whether current filter is compatible with the column */
                if (op == '=' || op == '==') {
                    if ( col_value != value || col_value==null || col_value=="" || col_value=="n/a")
                        ret = false;
                }else if (op == '!=') {
                    if ( col_value == value || col_value==null || col_value=="" || col_value=="n/a")
                        ret = false;
                } else if(op=='<') {
                    if ( parseFloat(col_value) >= value || col_value==null || col_value=="" || col_value=="n/a")
                        ret = false;
                } else if(op=='>') {
                    if ( parseFloat(col_value) <= value || col_value==null || col_value=="" || col_value=="n/a")
                        ret = false;
                } else if(op=='<=' || op=='≤') {
                    if ( parseFloat(col_value) > value || col_value==null || col_value=="" || col_value=="n/a")
                        ret = false;
                } else if(op=='>=' || op=='≥') {
                    if ( parseFloat(col_value) < value || col_value==null || col_value=="" || col_value=="n/a")
                        ret = false;
                }else{
                    // How to break out of a loop ?
                    alert("filter not supported");
                    return false;
                }

            });
            return ret;
        },

        _selectAll: function() {
            // requires jQuery id
            var uuid=this.id.split("-");
            var oTable=$("#querygrid-"+uuid[1]).dataTable();
            // Function available in QueryGrid 1.9.x
            // Filter : displayed data only
            var filterData = oTable._('tr', {"filter":"applied"});   
            /* TODO: WARNING if too many nodes selected, use filters to reduce nuber of nodes */        
            if(filterData.length<=100){
                $.each(filterData, function(index, obj) {
                    var last=$(obj).last();
                    var key_value=unfold.get_value(last[0]);
                    if(typeof($(last[0]).attr('checked'))=="undefined"){
                        $.publish('selected', 'add/'+key_value);
                    }
                });
            }
        },

    });

    $.plugin('QueryGrid', QueryGrid);

})(jQuery);

