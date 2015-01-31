'use strict';

/**
 * @ngdoc function
 * @name angularApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the angularApp
 */
angular.module('angularApp')
  .controller('MainCtrl', function ($scope, AlarmService) {
    function updateServerTime(callback){
        AlarmService.get(function(serverTime){
            $scope.serverTime = serverTime;
            if(callback) callback();
        });
    }

    $scope.showServerTime = false;

    $scope.setAlarm = function(){
        AlarmService.set($scope.datetime,
            function(){
                $scope.status = "ok";
                updateServerTime(function(){
                    $scope.showServerTime = true;
                });
            })
    };

    var result = new Date();
    result.setMilliseconds(0);
    result.setSeconds(0);
    $scope.datetime = result;

    // Sorry, it's a hackathon you know
    (function uglyPolling(){
        setInterval(
            updateServerTime, 1000);
    })();
  });
