'use strict';

window.angular.module('Posting').directive('deleteBtn', function() {
    return {
        restrict: 'A',
        replace: true,
        template: '<button class="btn btn-xs" ng-click="delete()">Delete</button>',
        scope: {
            count: '='
        },
        controller: function($scope) {
            $scope.delete = function() {
                window.alert('Hello ');
            };
        }
    };
});