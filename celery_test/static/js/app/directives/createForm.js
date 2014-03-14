'use strict';

window.angular.module('Posting').directive('createForm', function(Restangular, modelRelations, Info) {
    var getTemplateName = function(modelName) {
        return modelName.toLowerCase() + '.html';
    };

    var ctrl = function($scope, $modal) {

        function getModelName() {
            return (!$scope.item) ? $scope.type : modelRelations[$scope.type].child;
        }

        function getParentId() {
            return ($scope.item) ? $scope.item.id : null;
        }

        $scope.open = function () {
            var modelName = getModelName();
            var templateUrl = getTemplateName(modelName);

            var modalInstance = $modal.open({
                templateUrl: templateUrl,
                controller: function($scope, $modalInstance, Info) {

                    function setParentId() {
                        var parentName = modelRelations.getParent(modelName);
                        var parentId = getParentId();
                        if (parentName) {
                            $scope[modelName][parentName] = parentId;
                        }
                    }

                    $scope[modelName] = {};
                    $scope.info = Info.getAll();
                    setParentId();
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
        controller: ctrl,
        link: linker
    };
});