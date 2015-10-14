/* Buffered DOM updates */
var Buffer = Class.extend({

    init: function(callback, callback_this) {
        this._callback = callback;
        this._callback_this = callback_this;
        this._timerid  = null;
        this._num_elements = 0;
        this._elements = Array();

        this._interval = 1000;

        return this;
    },

    add: function(element)
    {
        this._elements.push(element);
        if (this._num_elements == 0) {
            this._timerid = setInterval(
                (function(self) {         //Self-executing func which takes 'this' as self
                    return function() {   //Return a function in the context of 'self'
                        messages.debug("running callback");
                        clearInterval(self._timerid);
                        self._callback.apply(self._callback_this);
                    }
                })(this),
                this._interval);
        }
        this._num_elements++;
    },

    get: function() {
        var elements = this._elements;
        this._elements = Array();
        this._num_elements = 0;
        return elements;
    },

});
