$(function() {
          $('a#test').bind('click', function() {
            $.getJSON('/multiplayer_checking',
                function(data) {
              //do nothing
            });
            return false;
          });
        });