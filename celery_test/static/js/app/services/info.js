'use strict';

angular.module('Posting').factory('Info', function(Restangular, modelRelations, $rootScope) {

    var info = {};

    function retrieve() {
        return Restangular.one('info').get().then(function(response) {
            return info = response;
        });
    }

    function getAll() {
        return info;
    }

    function resourceName (modelName) {
        return modelName.toLowerCase() + 's';
    }

    function addToInfo(itemType, item) {
        var parent = modelRelations[itemType].parent;
        $rootScope.$apply(function() {
            if (!parent) {
               info[resourceName(itemType)].push(item);
            } else {
                var parentItem = _.findWhere(info[resourceName(parent)], {id: item.parent});
                parentItem[resourceName(itemType)].push(item);
            }
        });
    }

    function removeFromInfo(itemType, item) {

        function getList() {
            var parent = modelRelations[itemType].parent;

            if (!parent) {
                return info[resourceName(itemType)];
            } else {
                var mainList = info[resourceName(parent)];
                var elem = _.findWhere(mainList, {id: item.parent});
                var childList = elem[resourceName(itemType)];
                return childList;
            }
        }

        function getElem(list) {
            return _.findWhere(list, {id: item.id});
        }

        $rootScope.$apply(function() {
            var list = getList();
            var elem = getElem(list);
            var index = _.indexOf(list, elem);
            list.splice(index, 1);
        });
    }

/*    function changeInfoItem(itemType, item) {
        var elem = 
    }*/

    function add(itemType, item) {
        var resource = resourceName(itemType);
        Restangular.all(resource).post(item).then(function(response) {
            return response;
        });
    }

    function remove(itemType, item) {
        var resource = resourceName(itemType);
        Restangular.one(resource, item.id).remove();
    }

    return {
        retrieve: retrieve,
        getAll: getAll,
        add: add,
        remove: remove,
        addToInfo: addToInfo,
        removeFromInfo: removeFromInfo
    };
});