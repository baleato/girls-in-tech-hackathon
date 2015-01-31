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
    console.log('[GET] alarm');
    res.send({
      alarm: getRealAlarmTimeMs()
    });
  })
  .post(function(req, res) {
    console.log('[POST] alarm', res.body);
    update(req, res);
  })
  .put(function(req, res) {
    console.log('[PUT] alarm', res.body);
    update(req, res);
  });

var bridge = require('./bridge');
// Sorry for all this intervals... hackathon time
var checking = false;
setInterval(
  function(){
    if(checking) return;

    checking = true;
    bridge.check(function(value){
      shouldGetUpEarly = value;
      checking = false;
    }, function(){
      checking = false;
    });
  }, 5000);

var switchingOn = false,
  isLigthOn = false;
setInterval(
  function(){
    console.log("alarm: ", new Date(getRealAlarmTimeMs()));
    if(getRealAlarmTimeMs() <= Date.now()){
      if(!switchingOn){
        switchingOn = true;
        bridge.turnLampOn(
          function(){
            ;
          },
          function(){
            switchingOn = false;
          });
      }
    }else{
      if(isLigthOn) {
        bridge.turnLampOff(
          // success
          function(){
            switchingOn = false;
            isLigthOn = false;

          },
          // error
          function(){

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