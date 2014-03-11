'use strict';

window.angular.module('Posting').directive('createForm', function(Restangular, modelRelations) {
    var getTemplateName = function(modelName) {
        return modelName.toLowerCase() + '.html';
    };
    var ctrl = function($scope, $modal, Info) {
        $scope.open = function () {
            var modelName = $scope.modelName;
            var templateUrl = getTemplateName(modelName);
            var parentId = $scope.parentId;
            var parentType = modelRelations[modelName].parent;
            parentType = (parentType) ? (modelRelations[parentType].name || parentType) : (null);

            var modalInstance = $modal.open({
                templateUrl: templateUrl,
                controller: function($scope, $modalInstance) {
                    $scope[modelName] = {};
                    if (parentType) { 
                        $scope[modelName][parentType] = parentId;
                    }
                    $scope.ok = function () {
                        $modalInstance.close($scope[modelName]);
                    };
                    $scope.cancel = function () {
                        $modalInstance.dismiss('cancel');
                    };
                }
            });
            modalInstance.result.then(function(result) {
                Info.add(modelName, result);
            });
        };
    };
    var linker = function(scope, element, attrs) {
        element.bind('click', function() {
            scope.open();
        });
    };
    return {
        restrict: 'EA',
        replace: true,
        scope: {
            modelName: '@',
            parentId: '@'
        },
        controller: ctrl,
        link: linker
    };
});