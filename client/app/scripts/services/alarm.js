'use strict';

angular.module('angularApp')
.factory('AlarmService', ['$http', function($http) {
    var server = 'http://localhost:3000',
        resourceName = 'alarm';

    return {
        get: function(success, error){
            $http.get(server + '/' + resourceName).
              success(function(data, status, headers, config) {
                console.log("Success");
                if(success) success(new Date(data.alarm));
              }).
              error(function(data, status, headers, config) {
                console.error("Error");
                if(error) error(data);
              });
        },

        set: function(alarmDate, success, error){
            $http.post(server + '/' + resourceName, {
                    alarm: alarmDate.getTime()
                }).
              success(function(data, status, headers, config) {
                console.log("Success");
                if(success) success();
              }).
              error(function(data, status, headers, config) {
                console.error("Error");
                if(error) error(data);
              });
        }
    };
}]);