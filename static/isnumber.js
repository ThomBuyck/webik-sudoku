document.getElementById("explicit-block-txt").onkeypress = function(e) {
    var chr = String.fromCharCode(e.which);
    if (!("<>\"".indexOf(chr) >= 0))
        return false;
};