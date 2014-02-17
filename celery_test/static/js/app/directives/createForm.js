'use strict';

window.angular.module('Posting').directive('createForm', function(Restangular) {
    var getTemplateName = function(modelName) {
        return modelName.toLowerCase() + '.html';
    };

    var ctrl = function($scope, $modal) {
        $scope.open = function () {
            var modelName = $scope.modelName;
            var templateUrl = getTemplateName(modelName);
            var parentId = $scope.parentId;
            var parentType = $scope.parentType;
            var modalInstance = $modal.open({
                templateUrl: templateUrl,
                controller: function ($scope, $modalInstance) {
                    $scope[modelName] = {};
                    $scope[modelName][parentType] = parentId;
                    $scope.ok = function () {
                        $modalInstance.close($scope[modelName]);
                    };
                    $scope.cancel = function () {
                        $modalInstance.dismiss('cancel');
                    };
                }
            });

            modalInstance.result.then(function (result) {
                window.console.log(result);
                Restangular.all(modelName.toLowerCase() + 's').post(result).then(function (some) {
                    window.console.log(some);
                });
            });
        };
    };

    return {
        restrict: 'A',
        replace: true,
        template: '<button ng-click="open()">{[{modelName}]}</button>',
        scope: {
            modelName: '@',
            parentId: '=',
            parentType: '@'
        },
        controller: ctrl
    };
});