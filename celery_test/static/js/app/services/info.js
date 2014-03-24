'use strict';

window.angular.module('Posting').factory('Info', function(Restangular, $rootScope, $q, _) {

    var info;

    var promise = Restangular.one('info').get();
    var deferred = $q.defer();

    var tree = {
        tweet: {
            child: 'timedTweet',
            parent: null,
        },
        postTweetSet: {
            child: 'periodicTweet',
            parent: null,
            name: 'posttweetset',
            foreign: ['interval']
        },
        periodicTweet: {
            child: null,
            parent: 'postTweetSet',
            foreign: ['tweet']
        },
        timedTweet: {
            child: null,
            parent: 'tweet',
            foreign: ['twitteruser']
        },
        interval: {
            child: null,
            parent: null
        },
        twitteruser: {
            child: null,
            parent: null
        }
    };

    function getResourceName(modelName) {
        return modelName.toLowerCase() + 's';
    }

    function getAllResources() {
        var names = [];
        for (var name in tree)
            names.push(getResourceName(name));
        return names;
    }

    function getChildResources() {
        var names = [];
        for (var name in tree) {
            if (tree[name].parent)
                names.push(getResourceName(name));
        }
        return names;
    }

    function getName(modelName) {
        return tree[modelName].name || modelName;
    }

    function getParent(modelName) {
        var pt = tree[modelName].parent;
        pt = (pt) ? (getName(pt)) : (null);
        return pt;
    }

    function getChild(modelName) {
        return tree[modelName].child;
    }

    function getForeignList(modelName) {
        return (tree[modelName].foreign) ? (tree[modelName].foreign) : null;
    }

    function retrieve() {
        if (info === undefined) {
            promise.then(function(response) {
                deferred.resolve(response);
                info = response;
                return info;
            });
        } else {
            deferred.resolve(info);
        }

        return deferred.promise;
    }

    function getResourceByType(type) {
        return retrieve().then(function(resp) {
            return resp[getResourceName(type)];
        });
    }

    function getItemById(type, id) {
        return getResourceByType(type).then(function(resp) {
            return _.findWhere(resp, {id: id});
        });
    }

    function getChildren(type, id) {
        var child = getChild(type);
        if (!child)
            return;
        return getResourceByType(child).then(function(resp) {
            var dict = {};
            dict[getName(type)] = id;
            return _.where(resp, dict);
        });
    }

    function getParentItem(type, item) {
        var parent = getParent(type);
        return getResourceByType(parent).then(function(resp) {
            return _.findWhere(resp, {id: item[parent]});
        });
    }

    function getForeignResource(type, id) {
        return getResourceByType(type).then(function(resp) {
            return _.findWhere(resp, {id: id});
        });
    }

    function addToInfo(itemType, item) {
        return getResourceByType(itemType).then(function(resp) {
            resp.push(item);
            return resp;
        });
    }

    function removeFromInfo(itemType, item) {
        return getResourceByType(itemType).then(function(resp) {
            var elem = _.findWhere(resp, {id: item.id});
            var index = _.indexOf(resp, elem);
            resp.splice(index, 1);
        });
    }

    function changeItem(itemType, item) {
        return getResourceByType(itemType).then(function(resp) {
            var elem = _.findWhere(resp, {id: item.id});
            var index = _.indexOf(resp, elem);
            resp[index] = item;
        });
    }


    function add(itemType, item) {
        var resource = getResourceName(itemType);
        var promise = Restangular.all(resource).post(item);
        return promise.then(function(resp) {
            return resp;
        });
    }

    function remove(itemType, item) {
        var resource = getResourceName(itemType);
        return Restangular.one(resource, item.id).remove();
    }

    return {
        retrieve: retrieve,
        add: add,
        remove: remove,
        addToInfo: addToInfo,
        removeFromInfo: removeFromInfo,
        changeItem: changeItem,
        getResourceName: getResourceName,
        getResourceByType: getResourceByType,
        getForeignList: getForeignList,
        getChildren: getChildren,
        getParentItem: getParentItem,
        getItemById: getItemById,
        getForeignResource: getForeignResource,
        getParent: getParent,
        getChild: getChild,
        getName: getName,
        getAllResources: getAllResources,
        getChildResources: getChildResources
    };
});