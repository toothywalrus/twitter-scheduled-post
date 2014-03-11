'use strict';

window.angular.module('Posting').directive('dashboard', function(Restangular) {
    return {
        restrict: 'E',
        replace: true,
        transclude: true,
        templateUrl: 'dashboard.html',
        controller: function($scope, Info) {
            $scope.$emit('info:start_load');
            Info.retrieve().then(function() {
                $scope.info = Info.getAll();
                $scope.$emit('info:stop_load', {});
            });
        }
    };
});