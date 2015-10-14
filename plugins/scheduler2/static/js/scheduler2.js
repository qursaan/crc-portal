/*
#
# Copyright (c) 2013 NITLab, University of Thessaly, CERTH, Greece
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
#
# This is a MySlice plugin for the NITOS Scheduler
# Nitos Scheduler v1
#
*/

/* some params */
var init_start_visible_index = 10;
var init_end_visible_index = 21;
var rsvrTblNm = "scheduler-reservation-table";
var SchedulerResources = [];
var schdlr_totalColums = 0;
var SetPerFun = null;
var Sched2 = null;
var Debug = true;
var schdlr_PartsInOneHour = 6;

(function ($) {
    var Scheduler2 = Plugin.extend({

        /** XXX to check
         * @brief Plugin constructor
         * @param options : an associative array of setting values
         * @param element : 
         * @return : a jQuery collection of objects on which the plugin is
         *     applied, which allows to maintain chainability of calls
         */
        init: function (options, element) {
            // Call the parent constructor, see FAQ when forgotten
            this._super(options, element);

            schdlr_totalColums = $("#scheduler-reservation-table th").length;

            //selection from table 
            $(window).keydown(function (evt) {
                if (evt.which == 17) { // ctrl
                    ctrlPressed = true;
                }
            }).keyup(function (evt) {
                if (evt.which == 17) { // ctrl
                    ctrlPressed = false;
                }
            });
            $("#" + rsvrTblNm).on('mousedown', 'td', rangeMouseDown).on('mouseup', 'td', rangeMouseUp).on('mousemove', 'td', rangeMouseMove);

            // Explain this will allow query events to be handled
            // What happens when we don't define some events ?
            // Some can be less efficient

            if (Debug) console.time("Listening_to_queries");
            /* Listening to queries */
            this.listen_query(options.query_uuid, 'all_ev');
            this.listen_query(options.query_all_resources_uuid, 'all_resources');
            this.listen_query(options.query_lease_uuid, 'lease');
            //this.listen_query(options.query_lease_uuid, 'lease');
            if (Debug) console.timeEnd("Listening_to_queries");

        },

        /* PLUGIN EVENTS */
        // on_show like in querytable


        /* GUI EVENTS */

        // a function to bind events here: click change
        // how to raise manifold events


        /* GUI MANIPULATION */

        // We advise you to write function to change behaviour of the GUI
        // Will use naming helpers to access content _inside_ the plugin
        // always refer to these functions in the remaining of the code

        show_hide_button: function () {
            // this.id, this.el, this.cl, this.elts
            // same output as a jquery selector with some guarantees
        },

        drawResources: function () {
            
            //if (Debug) this.debug('foo');
            if (Debug) console.time("each:SchedulerResources");

            //scheduler-reservation-table main table columns
            totalColums = $("#scheduler-reservation-table thead tr th").length;
            //var totalCell = [];
            //for (var i = 0; i < totalColums; i++) { totalCell.push("<td></td>"); }
            //var srt_body = [];
            var totalCell = "";
            for (var i = 0; i < totalColums; i++) totalCell +="<td></td>"; 
            var srt_body = "";

            $.each(SchedulerResources, function (i, group) {
                //var groupTR = $("#ShedulerNodes tbody").html('<tr><td class="no-image verticalIndex" rowspan="' + group.resources.length + '"><div class="verticalText">' + group.groupName + '</div></td><td id="schdlr_frstTD" class="info fixed"></td></tr>');
                var groupTR = $("#ShedulerNodes tbody").html('<tr><td class="no-image verticalIndex" rowspan="' + 30 + '"><div class="verticalText">' + group.groupName + '</div></td><td id="schdlr_frstTD" class="info fixed"></td></tr>');
                
                $.each(group.resources.slice(0,30), function (i, resource) {
                    if (i == 0) {
                        //$("#ShedulerNodes tbody tr:first").append('<td class="info fixed">' + resource.hostname + '</td>');
                        $(groupTR).find("#schdlr_frstTD").html(resource.hostname);
                        //$(srt_body).html("<tr>" + totalCell + "</tr>");
                    } else {
                        $(groupTR).find("tr:last").after('<tr><td class="info fixed">' + resource.hostname + '</td></tr>');
                        //$(srt_body).find("tr:last").after("<tr>" + totalCell + "</tr>");
                    }
                    srt_body += "<tr>" + totalCell + "</tr>";
                    //srt_body.push('<tr>'); srt_body = srt_body.concat(totalCell.concat()); srt_body.push('/<tr>');
                });
            });

            //$("#scheduler-reservation-table tbody").html(srt_body.join(""));
            $("#scheduler-reservation-table tbody").html(srt_body);

            if (Debug) console.timeEnd("each:SchedulerResources");
            

            $("#" + rsvrTblNm + " tbody tr").each(function (index) { $(this).attr("data-trindex", index); });

        },

        /* TEMPLATES */

        // see in the html template
        // How to load a template, use of mustache

        /* QUERY HANDLERS */
        loadWithDate: function () {
            // only convention, not strictly enforced at the moment
        },
        // How to make sure the plugin is not desynchronized
        // He should manifest its interest in filters, fields or records
        // functions triggered only if the proper listen is done

        /* all_ev QUERY HANDLERS Start */
        on_all_ev_clear_records: function (data) {
            //alert('all_ev clear_records');
        },
        on_all_ev_query_in_progress: function (data) {
           // alert('all_ev query_in_progress');
        },
        on_all_ev_new_record: function (data) {
            //alert('all_ev new_record');
        },
        on_all_ev_query_done: function (data) {
            //alert('all_ev query_done');
        },
        //another plugin has modified something, that requires you to update your display. 
        on_all_ev_field_state_changed: function (data) {
            //alert('all_ev query_done');
        },
        /* all_ev QUERY HANDLERS End */
        /* all_resources QUERY HANDLERS Start */
        on_all_resources_clear_records: function (data) {
            //data is empty on load
        },
        on_all_resources_query_in_progress: function (data) {
            //data is empty on load
        },
        on_all_resources_new_record: function (data) {
            var tmpGroup = lookup(SchedulerResources, 'groupName', data.type);
            if (tmpGroup == null) {
                tmpGroup = { groupName: data.type, resources: [] };
                SchedulerResources.push(tmpGroup);
                //if (data.type != "node")  alert('not all node');
            }
            tmpGroup.resources.push(data);
            //alert('new_record');
        },
        on_all_resources_query_done: function (data) {
            this.drawResources();
            //data is empty on load
            /* GUI setup and event binding */
            this._initUI();
            this._SetPeriodInPage(init_start_visible_index, init_end_visible_index);
            this.loadWithDate();
        },
        //another plugin has modified something, that requires you to update your display. 
        on_all_resources_field_state_changed: function (data) {
            //alert('all_resources query_done');
        },
        /* all_resources QUERY HANDLERS End */
        /* lease QUERY HANDLERS Start */
        on_lease_clear_records: function (data) { alert('clear_records'); },
        on_lease_query_in_progress: function (data) { alert('query_in_progress'); },
        on_lease_new_record: function (data) { alert('new_record'); },
        on_lease_query_done: function (data) { alert('query_done'); },
        //another plugin has modified something, that requires you to update your display. 
        on_lease_field_state_changed: function (data) { alert('query_done'); },
        /* lease QUERY HANDLERS End */


        // no prefix

        on_filter_added: function (filter) {

        },

        // ... be sure to list all events here

        /* RECORD HANDLERS */
        on_all_new_record: function (record) {
            //
            alert('on_all_new_record');
        },

        debug : function (log_txt) {
            if (typeof window.console != 'undefined') {
                console.debug(log_txt);
            }
        },

        /* INTERNAL FUNCTIONS */
        _initUI: function () {
            if (Debug) console.time("_initUI");
            //fix margins in tables
            mtNodesTbl = $("#" + rsvrTblNm + " tr:first").outerHeight() + 6;
            mtSchrollCon = $("#nodes").outerWidth();
            $("#nodes").css("margin-top", mtNodesTbl);
            $("#reservation-table-scroll-container").css("margin-left", mtSchrollCon);
            SetPerFun = this._SetPeriodInPage;
            //slider
            $("#time-range").slider({
                range: true,
                min: 0,
                max: 24,
                step: 0.5,
                values: [init_start_visible_index, init_end_visible_index],
                slide: function (event, ui) {
                    SetPerFun(ui.values[0], ui.values[1]);
                }
            });
            $("#DateToRes").datepicker({
                dateFormat: "yy-mm-dd",
                minDate: 0,
                numberOfMonths: 3
            }).change(function () {
                //Scheduler2.loadWithDate();
            }).click(function () {
                $("#ui-datepicker-div").css("z-index", 5);
            });
            //other stuff
            fixOddEvenClasses();
            $("#" + rsvrTblNm + " td:not([class])").addClass("free");
            if (Debug) console.timeEnd("_initUI");
        },
        _SetPeriodInPage: function (start, end) {
            if (Debug) console.time("_SetPeriodInPage");
            ClearTableSelection();
            $("#lbltime").html(GetTimeFromInt(start) + " - " + GetTimeFromInt(end));
            
            var start_visible_index = (start * schdlr_PartsInOneHour) + 1;
            var end_visible_index = (end * schdlr_PartsInOneHour);

            //hide - show
            for (i = 0; i < start_visible_index; i++) {
                $("#" + rsvrTblNm + " td:nth-child(" + i + "), #" + rsvrTblNm + " th:nth-child(" + i + ")").hide();
            }
            for (i = end_visible_index + 1; i <= schdlr_totalColums; i++) {
                $("#" + rsvrTblNm + " td:nth-child(" + i + "), #" + rsvrTblNm + " th:nth-child(" + i + ")").hide();
            }
            /*$("#" + rsvrTblNm + " td:not([class*='info']), #" + rsvrTblNm + " th:not([class*='fixed'])").hide();*/
            for (i = start_visible_index; i <= end_visible_index; i++) {
                $("#" + rsvrTblNm + " td:nth-child(" + i + "), #" + rsvrTblNm + " th:nth-child(" + i + ")").show();
            }

            if ($("#" + rsvrTblNm + " th:visible:first").width() > 105) {
                $("#" + rsvrTblNm + " th span").css("display", "inline")
            } else {
                $("#" + rsvrTblNm + " th span").css("display", "block");
            }
            mtNodesTbl = $("#" + rsvrTblNm + " tr:first").outerHeight() + 6;
            $("#nodes").css("margin-top", mtNodesTbl);
            //$("#scroll_container").width($("#Search").width() - $("#nodes").width());
            //$("#nodes th").height($("#tblReservation th:visible:first").height() - 2);
            if (Debug) console.timeEnd("_SetPeriodInPage");
        }
    });

    //Sched2 = new Scheduler2();

    /* Plugin registration */
    $.plugin('Scheduler2', Scheduler2);

    // TODO Here use cases for instanciating plugins in different ways like in the pastie.


})(jQuery);



