// Ajax function to check the puzzle
$(function() {
          $('#Done').bind('click', function() {
            $.getJSON('/checking',
                function(data) {

            });
            return false;
          });
        });