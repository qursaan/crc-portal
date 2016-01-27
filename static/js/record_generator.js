/* Buffered DOM updates */
var RecordGenerator = Class.extend({

    init: function(query, generators, number)
    {
        this._query      = query;
        this._generators = generators;
        this._number     = number;
    },

    random_int: function(options)
    {
        var default_options = {
            max: 1000
        }

        if (typeof options == 'object')
            options = $.extend(default_options, options);
        else
            options = default_options;

        return Math.floor(Math.random()*(options.max+1));
    },

    random_string: function()
    {
        var default_options = {
            possible: "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789",
            len:      this.random_int({max: 15})
        }

        if (typeof options == 'object')
            options = $.extend(default_options, options);
        else
            options = default_options;

        var text = "";

        for( var i=0; i < options.len; i++ )
            text += options.possible.charAt(Math.floor(Math.random() * options.possible.length));

        return text;

    },

    generate_record: function()
    {
        var self = this;
        var record = {};

        $.each(this._query.fields, function(i, field) {
            record[field] = self[self._generators[field]]();
        });

        // Publish records
        manifold.raise_record_event(self._query.query_uuid, NEW_RECORD, record);
        
    },

    run: function()
    {
        var record;
        manifold.raise_record_event(this._query.query_uuid, CLEAR_RECORDS);
        for (var i = 0; i < this._number; i++) {
            record = this.generate_record();
            /* XXX publish record */
        }
        manifold.raise_record_event(this._query.query_uuid, DONE);

    }
});
