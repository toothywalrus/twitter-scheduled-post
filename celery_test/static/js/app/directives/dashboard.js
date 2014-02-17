'use strict';

window.angular.module('Posting').directive('dashboard', function(Restangular) {
    return {
        restrict: 'E',
        replace: true,
        transclude: true,
        templateUrl: 'dashboard.html',
        controller: function($scope) {
            $scope.$emit('info:start_load');
            Restangular.one('info').get().then(function(info) {
                $scope.info = info;
                $scope.$emit('info:stop_load', {});
            });
        }
    };
});