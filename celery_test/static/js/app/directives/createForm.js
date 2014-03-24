'use strict';

window.angular.module('Posting').directive('createForm', function(Restangular, Info) {
    var getTemplateName = function(modelName) {
        return modelName.toLowerCase() + '_form.html';
    };

    var ctrl = function($scope, $modal) {

        function getModelName() {
            return (!$scope.item) ? $scope.type : Info.getChild($scope.type);
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
                        var parentName = Info.getParent(modelName);
                        var parentId = getParentId();
                        if (parentName) {
                            $scope[modelName][parentName] = parentId;
                        }
                    }

                    $scope[modelName] = {};
                    Info.retrieve().then(function(resp) {
                        $scope.info = resp;
                    });
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
                console.log(result);
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