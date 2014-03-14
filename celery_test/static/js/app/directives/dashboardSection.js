'use strict';

window.angular.module('Posting').directive('dashboardSection', function(modelRelations) {
    var linker = function(scope, element, attrs) {
    };

    var ctrl = function($scope) {
        console.log($scope.type);
        $scope.childModel = modelRelations[$scope.type].child;
    };

    return {
        restrict: 'E',
        replace: true,
        transclude: true,
        templateUrl: 'dashboardSection.html',
        scope: {
            list: '=',
            type: '@'
        },
        link: linker,
        controller: ctrl
    };
});