var express = require('express');
var bodyParser = require('body-parser');
var multer = require('multer');

var allowCrossDomain = function(req, res, next) {
    res.header('Access-Control-Allow-Origin', '*');
    res.header('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE');
    res.header('Access-Control-Allow-Headers', 'Content-Type');

    next();
}

var app = express();
app.use(bodyParser.json()); // for parsing application/json
app.use(bodyParser.urlencoded({ extended: true })); // for parsing application/x-www-form-urlencoded
app.use(allowCrossDomain);
app.use(multer()); // for parsing multipart/form-data


var alarm = new Date(2015, 1, 1, 8, 0, 0);
var shouldGetUpEarly = false;
var howMuchEarlyInMs = 1500000; // 25min

function getRealAlarmTimeMs(){
  return shouldGetUpEarly ? alarm.getTime() - howMuchEarlyInMs : alarm.getTime();
}

function update(req, res){
  var newValue = new Date(req.body.alarm);
  if(isNaN(newValue.getTime())){
    res.status(500);
    res.send({
      message: 'invalid date'
    });
  }else{
    alarm = newValue;
    res.send()
  }
}

app.route('/alarm')
  .get(function(req, res) {
    // console.log('[GET] alarm');
    res.send({
      alarm: getRealAlarmTimeMs()
    });
  })
  .post(function(req, res) {
    console.log('[POST] alarm', req.body);
    update(req, res);
  })
  .put(function(req, res) {
    console.log('[PUT] alarm', req.body);
    update(req, res);
  });

var bridge = require('./bridge');
// Sorry for all this intervals... hackathon time
var checking = false;

(function checkHumidity(){
    if(checking) return;

    checking = true;
    bridge.check(function(value){
      shouldGetUpEarly = value;
      checking = false;
      setTimeout(checkHumidity, 1000);
    }, function(){
      checking = false;
      setTimeout(checkHumidity, 1000);
    });
})();

var switchingOn = false,
  isLigthOn;
setInterval(
  function(){
    if(getRealAlarmTimeMs() <= Date.now()){
      if(!switchingOn){
        switchingOn = true;
        bridge.turnLampOn(
          function(){
            isLigthOn = true;
          },
          function(){
            switchingOn = false;
          });
      }
    }else{
      console.log("off..." + isLigthOn
        + "- "+ switchingOn);
      if(isLigthOn !== false) {
        bridge.turnLampOff(
          // success
          function(){
            switchingOn = false;
            isLigthOn = false;
          },
          // error
          function(){
            switchingOn = false;
            isLigthOn = true;
          });
      }
    }
  }, 5000);


// Start server on localhost:3000
var server = app.listen(3000, function () {

  var host = server.address().address;
  var port = server.address().port;

  console.log('App listening at http://%s:%s', host, port)
});