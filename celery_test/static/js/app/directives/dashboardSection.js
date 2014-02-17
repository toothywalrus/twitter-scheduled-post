'use strict';

window.angular.module('Posting').directive('dashboardSection', function() {
    var linker = function(scope, element, attrs) {
    };

    var ctrl = function($scope) {
    };

    return {
        restrict: 'E',
        replace: true,
        transclude: true,
        templateUrl: 'dashboardSection.html',
        scope: {
            list: '=',
            element: '@'
        },
        link: linker,
        controller: ctrl
    };
});