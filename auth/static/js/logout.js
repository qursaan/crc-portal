/* retrieve username from the button that is clicked, the one named 'logout' 
   and that is expected to have the 'username' attribute */
function logout () {
    var username=$(this).data('username');
    var msg="Are you sure you want to logout as " + username + " ?";
    /* redirect to /logout, see urls.py */
    if (confirm(msg)) window.location="/logout/";
}
/* attach this function to the logout button */
$(document).ready(function() { $('#logout').click(logout); })
