'use strict';

window.angular.module('Posting').directive('dashboardSection', function(modelRelations) {
    var linker = function(scope, element, attrs) {
    };

    var ctrl = function($scope) {
        $scope.childModel = modelRelations[$scope.element].child;
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