var PythonShell = require('python-shell');

function check(callback){
    PythonShell.run('predictor.py', function (err, data) {
      if (err) throw err;

      var value = parseInt(data[0], 10);
      console.log('>> Prediction: ', parseInt(data[0], 10));
      if(callback) callback(value);
    });
}

function checkHumidity(callback, errorCallback){
    PythonShell.run('checkHumidity.py', function (err, data) {
        if (err) {
            console.error('Error calling checkHumidity');
            if(errorCallback) errorCallback();
            return;
        }

        // sorry
        var value = parseInt(data[0], 10) > 5000 ? true : false;

        console.log('>> Prediction: ', parseFloat(data[0], 10));
        if(callback) callback(value);
    });
}

module.exports.check = checkHumidity;

function turnLampOn(callback, errorCallback){
    console.log('Turning lamp on...');
    PythonShell.run('turn_lamp_on.py', function (err, data) {
      if (err) {
        console.error('Error calling turnLampOn');
        if(errorCallback) errorCallback();
        return;
      }

      console.log('Lamp turning on finished!');
      if(callback) callback();
    });
}
module.exports.turnLampOn = turnLampOn;

function turnLampOff(callback, errorCallback){
    console.log('Turning lamp off...');
    PythonShell.run('turn_lamp_off.py', function (err, data) {
      if (err) {
        console.error('Error calling turnLampOff');
        if(errorCallback) errorCallback();
        return;
      }

      console.log('Lamp turning on finished!');
      if(callback) callback();
    });
}
module.exports.turnLampOff = turnLampOff;