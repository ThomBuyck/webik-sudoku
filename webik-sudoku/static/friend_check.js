// Ajax function to add friend to database
$(function() {
          $('a#test').bind('click', function() {
            $.getJSON('/friend_check',
                function(data) {
              //do nothing
            });
            return false;
          });
        });