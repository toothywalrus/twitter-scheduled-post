'use strict';

window.angular.module('Posting').directive('createForm', function(Restangular, modelRelations, Info) {
    var getTemplateName = function(modelName) {
        return modelName.toLowerCase() + '.html';
    };
    var ctrl = function($scope, $modal) {
        $scope.open = function () {
            var modelName = $scope.type;
            var templateUrl = getTemplateName(modelName);
            var parentType = modelRelations[modelName].parent;
            parentType = (parentType) ? (modelRelations[parentType].name || parentType) : (null);

            $scope.modalInstance = $modal.open({
                templateUrl: templateUrl,
                controller: function($scope, $modalInstance, Info) {
                    $scope[modelName] = {};
                    $scope.info = Info.getAll();
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

            /*modalInstance.result.then(function(result) {
                Info.add(modelName, result);
            });*/
        };
    };

    var linker = function(scope, element, attrs, listItemCtrl) {
        element.bind('click', function() {
            scope.open();
            scope.modalInstance.result.then(function(result) {
                Info.add(scope.type, result);
            });
            console.log(scope);
        });
    };
    
    return {
        restrict: 'EA',
        //require: '^listItem',
        /*scope: {
            modelName: '@',
        },*/
        controller: ctrl,
        link: linker
    };
});