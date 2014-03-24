'use strict';

window.angular.module('Posting').directive('listItem', function(Info, $rootScope) {

    var ctrl = function($scope) {
        $scope.getTemplateName = function() {
            return $scope.type.toLowerCase() + '-item.html';
        };

        if (Info.getChild($scope.type)) {
            $rootScope.$watch('info_change', function() {
                Info.getChildren($scope.type, $scope.item.id).then(function(resp) {
                    $scope.children = resp;
                });
            });
        }

        var forList = Info.getForeignList($scope.type);
        if (forList) {
            $scope.foreign = {};
            window.angular.forEach(forList, function(val) {
                Info.getItemById(val, $scope.item[val]).then(function(resp) {
                    $scope.foreign[val] = resp;
                });
            });
        }

        $scope.info = $rootScope.info;
    };

    return {
        restrict: 'E',
        template: '<div ng-include="getTemplateName()"></div>',
        scope: {
            item: '=',
            type: '@'
        },
        controller: ctrl,
    };
});