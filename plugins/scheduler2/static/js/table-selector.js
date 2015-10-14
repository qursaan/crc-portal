////version 3
var dragStart_td = 0;
var dragStart_tr = 0;
var dragEnd_td = 0;
var dragEnd_tr = 0;
//tmp gia ta loops & check gia to last state
var tmp_dragStart_td;
var tmp_dragStart_tr;
var tmp_dragEnd_td;
var tmp_dragEnd_tr;
var isDragging = false;
var ctrlPressed = false;
// try stop 
var continueExecuting = false;
var isExecuting = false;



function rangeMouseDown(e) {
    if (Debug) console.time("mouse:rangeMouseDown");
    if (isRightClick(e)) {
        return false;
    } else {
        dragStart_tr = $(this).parent().index();
        dragStart_td = $(this).index();
        dragEnd_tr = dragStart_tr;
        dragEnd_td = dragStart_td;
        //alert(dragStart_tr);
        //var allCells = $("#tblReservation td");
        //dragStart = allCells.index($(this));

        if ( $(this).hasClass("free"))
            $(this).addClass("selected_tmp");

        isDragging = true;
        //selectRange();

        if (typeof e.preventDefault != 'undefined') { e.preventDefault(); }
        document.documentElement.onselectstart = function () { return false; };
    }
    if (Debug) console.timeEnd("mouse:rangeMouseDown");
}

function rangeMouseUp(e) {
    if (Debug) console.time("mouse:rangeMouseUp");
    if (isRightClick(e)) {
        return false;
    } else {
        //var allCells = $("#tblReservation td");
        //dragEnd = allCells.index($(this));

        dragEnd_tr = $(this).parent().index();
        dragEnd_td = $(this).index();

        isDragging = false;
        selectRange(false);

        document.documentElement.onselectstart = function () { return true; };
    }
    if (Debug) console.timeEnd("mouse:rangeMouseUp");
}

function rangeMouseMove(e) {
    //if (Debug) console.time("mouse:rangeMouseMove");
    if (isDragging) {
        dragEnd_tr = $(this).parent().attr('data-trindex');
        dragEnd_td = $(this).attr('data-tdindex');

        //if (Debug) this.debug('foo');

        if ((dragEnd_tr != tmp_dragEnd_tr) || (dragEnd_td != tmp_dragEnd_td)) {
            //console.log(dragEnd_tr + " - " + tmp_dragEnd_tr);
            //console.log(dragEnd_td + " - " + tmp_dragEnd_td);
            //selectRange(true);
        }
    }
    //if (Debug) console.timeEnd("mouse:rangeMouseMove");
}

function selectRange(IsTemp) {
    if (Debug) console.time("mouse:---selectRange");

    if (!ctrlPressed)
        $("#" + rsvrTblNm + "  td:not([class='info'],[class='closed'])").removeClass('selected selected_tmp').addClass('free');

    tmp_dragStart_td = dragStart_td;
    tmp_dragStart_tr = dragStart_tr;
    tmp_dragEnd_td = dragEnd_td;
    tmp_dragEnd_tr = dragEnd_tr;

    if (tmp_dragStart_td > tmp_dragEnd_td) {
        var tmp = tmp_dragStart_td;
        tmp_dragStart_td = tmp_dragEnd_td;
        tmp_dragEnd_td = tmp;
    }

    if (tmp_dragStart_tr > tmp_dragEnd_tr) {
        var tmp = tmp_dragStart_tr;
        tmp_dragStart_tr = tmp_dragEnd_tr;
        tmp_dragEnd_tr = tmp;
    }

    //alert("tmp_dragStart_td:" + tmp_dragStart_td + "\n tmp_dragStart_tr:" + tmp_dragStart_tr + "\n tmp_dragEnd_td:" + tmp_dragEnd_td + "\n tmp_dragEnd_tr:" + tmp_dragEnd_tr);


    for (i = tmp_dragStart_tr; i <= tmp_dragEnd_tr; i++) {
        for (j = tmp_dragStart_td; j <= tmp_dragEnd_td; j++) {
            //alert("i:" + i + "j:" + j);
            var cell = $('#' + rsvrTblNm + '  tbody tr:eq(' + i + ') td:eq(' + j + ')');
            //$(cell)
            curClass = $(cell).attr("class");
            //alert(curClass);
            switch (curClass) {
                case "free_tmp":
                    $(cell).removeClass();
                    if (IsTemp)
                        $(cell).addClass("free_tmp");
                    else
                        $(cell).addClass("free");
                    break;
                case "free":
                    $(cell).removeClass();
                    if (IsTemp)
                        $(cell).addClass("selected_tmp");
                    else
                        $(cell).addClass("selected");
                    break;
                case "selected_tmp":
                    $(cell).removeClass();
                    if (IsTemp)
                        $(cell).addClass("selected_tmp");
                    else
                        $(cell).addClass("selected");
                    break;
                case "selected":
                    $(cell).removeClass();
                    if (IsTemp)
                        $(cell).addClass("free_tmp");
                    else
                        $(cell).addClass("free");
                    break;
                case "closed":
                    //do nothing
                    //alert("not allowed!");
                    break;
            }
        }
    }


    /*if (dragEnd + 1 < dragStart) { // reverse select
    //alert(1);
    $("#tblReservation td:not([class='info'])").slice(dragEnd, dragStart + 1).addClass('selected');
    } else {
    alert(dragStart + "-" + dragEnd);
    $("#tblReservation td:not([class='info'])").slice(dragStart, dragEnd).addClass('selected');
    }*/


    if (Debug) console.timeEnd("mouse:---selectRange");
}

function ClearTableSelection(){
    $('#' + rsvrTblNm + ' .selected').addClass("free").removeClass("selected");
}


