var PythonShell = require('python-shell');

function check(callback){
    PythonShell.run('predictor.py', function (err, data) {
      if (err) throw err;

      var value = parseInt(data[0], 10);
      console.log('>> Prediction: ', parseInt(data[0], 10));
      if(callback) callback(value);
    });
}
module.exports.check = check;

function turnLampOn(callback){
    console.log('Turning lamp on...');
    PythonShell.run('turn_lamp_on.py', function (err, data) {
      if (err) throw err;

      console.log('Lamp turning on finished!');
      if(callback) callback();
    });
}
module.exports.turnLampOn = turnLampOn;

function turnLampOff(callback){
    console.log('Turning lamp on...');
    PythonShell.run('turn_lamp_off.py', function (err, data) {
      if (err) throw err;

      console.log('Lamp turning on finished!');
      if(callback) callback();
    });
}
module.exports.turnLampOff = turnLampOff;