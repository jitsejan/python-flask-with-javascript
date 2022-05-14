$( document ).ready(function() {

   function createCanvas(parent, width, height) {
    var canvas = document.getElementById("inputCanvas");
    canvas.context = canvas.getContext('2d');
    return canvas;
  }

  function init(container, width, height, fillColor) {
    var canvas = createCanvas(container, width, height);
    var ctx = canvas.context;
    ctx.fillCircle = function(x, y, radius, fillColor) {
      this.fillStyle = fillColor;
      this.beginPath();
      this.moveTo(x, y);
      this.arc(x, y, radius, 0, Math.PI * 2, false);
      this.fill();
    };
    ctx.clearTo = function(fillColor) {
      ctx.fillStyle = fillColor;
      ctx.fillRect(0, 0, width, height);
    };
    ctx.clearTo("#fff");

    canvas.onmousemove = function(e) {
      if (!canvas.isDrawing) {
        return;
      }
      var x = e.pageX - this.offsetLeft;
      var y = e.pageY - this.offsetTop;
      var radius = 10;
      var fillColor = 'rgb(102,153,255)';
      ctx.fillCircle(x, y, radius, fillColor);
    };
    canvas.onmousedown = function(e) {
      canvas.isDrawing = true;
    };
    canvas.onmouseup = function(e) {
      canvas.isDrawing = false;
    };
  }

  var container = document.getElementById('canvas');
  init(container, 200, 200, '#ddd');

  function clearCanvas() {
    var canvas = document.getElementById("inputCanvas");
    var ctx = canvas.getContext("2d");
        ctx.clearRect(0, 0, canvas.width, canvas.height);
  }

  function getData() {
    var canvas = document.getElementById("inputCanvas");
    var imageData = canvas.context.getImageData(0, 0, canvas.width, canvas.height);
    var data = imageData.data;
    var outputData = []
    for(var i = 0; i < data.length; i += 4) {
      var brightness = 0.34 * data[i] + 0.5 * data[i + 1] + 0.16 * data[i + 2];
      outputData.push(brightness);
    }
    $.post( "/postmethod", {
      canvas_data: JSON.stringify(outputData)
    }, function(err, req, resp){
      window.location.href = "/results/"+resp["responseJSON"]["unique_id"];  
      console.log(resp);
    });
  }

  function getPriceData() {
    var ticker = document.querySelector('input').value;
    console.log(ticker)
    $.post( "/postticker", {
      ticker_name: ticker
    }, function (err, req, resp) {
      window.location.href = "/price_chart/"+resp["responseJSON"]["stock"]
      console.log(resp)
    })
  }

  $( "#clearButton" ).click(function(){
    clearCanvas();
  });

  $( "#sendButton" ).click(function(){
    getData();
  });

  $( "#tickerButton ").click(function() {
    getPriceData();
  });

});