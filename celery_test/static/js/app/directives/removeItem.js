'use strict';

angular.module('Posting').directive('removeItem', function(Info) {
    return {
        restrict: 'A',
        link: function(scope, element, attrs) {
            element.bind('click', function(e) {
                Info.remove(scope.type, scope.item);
                return false;
            });
        }
    };
});