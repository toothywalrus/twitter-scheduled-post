'use strict';

window.angular.module('Posting').directive('listItem', function() {

    var ctrl = function($scope) {
        $scope.getTemplateName = function() {
            return $scope.type.toLowerCase() + '-item.html';
        };
    };

    return {
        restrict: 'E',
        template: '<div ng-include="getTemplateName()"></div>',
        scope: {
            item: '=',
            type: '@'
        },
        controller: ctrl
    };
});