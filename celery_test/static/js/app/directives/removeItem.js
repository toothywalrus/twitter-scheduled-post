'use strict';

window.angular.module('Posting').directive('removeItem', function(Info) {
    return {
        restrict: 'A',
        link: function(scope, element) {
            element.bind('click', function() {
                Info.remove(scope.type, scope.item);
                return false;
            });
        }
    };
});