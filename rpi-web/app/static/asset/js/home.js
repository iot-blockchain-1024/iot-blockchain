$(document).ready(function() {
    $('#monitor-button').click(function() {
        window.location.href="iot.html";
    });
      $('.masthead')
        .visibility({
          once: false,
          onBottomPassed: function() {
            $('.fixed.menu').transition('fade in');
          },
          onBottomPassedReverse: function() {
            $('.fixed.menu').transition('fade out');
          }
        })
      ;
      $('.ui.sidebar')
        .sidebar('attach events', '.toc.item')
      ;
});