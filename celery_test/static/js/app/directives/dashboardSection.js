'use strict';

window.angular.module('Posting').directive('dashboardSection', function(Info) {
    var linker = function(scope, element, attrs) {
    };

    var ctrl = function($scope) {
        Info.getResourceByType($scope.type).then(function(resp) {
            $scope.list = resp;
        });
    };

    return {
        restrict: 'E',
        replace: true,
        transclude: true,
        templateUrl: 'dashboardSection.html',
        scope: {
            type: '@'
        },
        link: linker,
        controller: ctrl
    };
});