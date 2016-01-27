// first application is for the 'validation' button in the topmenu
// if the subject query is non empty, then we turn on the subject button
// that is provided through button_domid

(function($){

    var debug=false;
//    debug=true

    var TopmenuValidation = Plugin.extend({

        init: function(options, element) {
	    this.classname="topmenuvalidation";
            this._super(options, element);
            this.listen_query(options.query_uuid);
	    this.triggered=false;
	},

        // Could be the default in parent
        on_query_in_progress: function() {
	    var presets = spin_presets();
	    presets.radius=5;
	    presets.length=4;
	    presets.lines=7;
	    presets.width=2;
            this.spin(presets);
        },

	// we have received at least one answer: we'll do something
	on_new_record: function (record) {
	    // we only need to act on the first record
	    if (this.triggered) return;
	    $('#'+this.options.button_domid).removeClass('disabled');
	    this.unspin();
	    this.triggered=true;
        },
	// for reference only, since there is nothing we need to do at this point
	on_query_done: function() {
	    if (!this.triggered) this.unspin();
	},
    });

    $.plugin('TopmenuValidation', TopmenuValidation);

})(jQuery);
