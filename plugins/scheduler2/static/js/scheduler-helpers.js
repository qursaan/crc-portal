function lookup(array, prop, value) {
    for (var i = 0, len = array.length; i < len; i++)
        if (array[i][prop] === value) return array[i];
}

function GetTimeFromInt(intTime) {
    var has30 = intTime % 1;
    var CurInt = parseInt(intTime / 1);
    if (CurInt < 10)
        CurInt = "0" + CurInt;

    if (has30 == 0) {
        return CurInt + ":00";
    } else {
        return CurInt + ":30";
    }
}

function fixOddEvenClasses() {
    $('#' + rsvrTblNm + ' tbody tr').removeClass();
    $('#' + rsvrTblNm + ' tbody tr:visible:even').addClass('even');
    $('#' + rsvrTblNm + ' tbody tr:visible:odd').addClass('odd');
}

function isRightClick(e) {
    if (e.which) {
        return (e.which == 3);
    } else if (e.button) {
        return (e.button == 2);
    }
    return false;
}
