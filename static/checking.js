$(function() {
          $('a#test').bind('click', function() {
            $.getJSON('/checking',
                function(data) {
              //do nothing
            });
            return false;
          });
        });