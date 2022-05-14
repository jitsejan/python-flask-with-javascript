$( document ).ready(function() {
  function init() {}

  function getData() {
    var ticker = document.querySelector('input').value;
    console.log(ticker)
    $.post( "/postmethod", {
      ticker_name: ticker
    }, function (err, req, resp) {
      window.location.href = "/price_chart/"+resp["responseJSON"]["stock"]
      console.log(resp)
    })
  }

  $( "#tickerButton ").click(function() {
    getData();
  });

});