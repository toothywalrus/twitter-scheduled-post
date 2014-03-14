angular.module('Posting').factory('Info', function(Restangular, modelRelations, $rootScope) {

    var info = {};

    var retrieve = function() {
        return Restangular.one('info').get().then(function(response) {
            return info = response;
        });
    };

    var getAll = function() {
        return info;
    }

    var resourceName = function(modelName) {
        return modelName.toLowerCase() + 's';
    }

    var addToInfo = function(itemType, item) {
        var parent = modelRelations[itemType].parent;
        $rootScope.$apply(function() {
            if (!parent) {
               info[resourceName(itemType)].push(item);
            } else {
                var parentItem = _.findWhere(info[resourceName(parent)], {id: item.parent});
                parentItem[resourceName(itemType)].push(item);
            }
        });
    };

    var removeFromInfo = function(itemType, item) {
        var resource = resourceName(itemType);
        $rootScope.$apply(function() {
            var elem =_.findWhere(info[resource], {id: item.id});
            info[resource] = _.without(info[resource], elem);
        });
    };

    var add = function(itemType, item) {
        var resource = resourceName(itemType);
        Restangular.all(resource).post(item).then(function(response) {
            //addToInfo(itemType, response);
            return response;
        });
    };

    var remove = function(itemType, item) {
        var resource = resourceName(itemType);
        Restangular.one(resource, item.id).remove().then(function() {
            //removeFromInfo(itemType, item);
        });
    };

    return {
        retrieve: retrieve,
        getAll: getAll,
        add: add,
        remove: remove,
        addToInfo: addToInfo,
        removeFromInfo: removeFromInfo
    };
});