'use strict';

window.angular.module('Posting').factory('GlobalService', function () {
    var vars = {
        is_authenticated: false
    };

    return vars;
});

angular.module('Posting').constant('modelRelations', {
    tweet: {
        child: 'timedTweet',
        parent: null,
    },
    postTweetSet: {
        child: 'periodicTweet',
        parent: null,
        name: 'tweetset'
    },
    periodicTweet: {
        child: null,
        parent: 'postTweetSet'
    },
    timedTweet: {
        child: null,
        parent: 'tweet'
    }
});

angular.module('Posting').factory('Item', function(Restangular) {
    var Item = function(data) {
        angular.extend(this, data);
    };

    Item.prototype.create = function(itemType) {
        var item = this;
        var plural = itemType.toLowerCase() + 's';
        Restangular.all(plural).post(item).then(function(response) {
            item.id = response.id;
            return item;
        });
    };

    return Item;
});

angular.module('Posting').factory('Info', function(Restangular, modelRelations) {

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
        if (!parent) {
            info[resourceName(itemType)].push(item);
        }
        else {
            console.log(info[resourceName(parent)]);
            info[resourceName(parent)][resourceName(itemType)].push(item);
        }
    }

    var removeFromInfo = function(itemType, item) {
        var resource = resourceName(itemType);
        info[resource] = _.without(info[resource], item);
    };

    var add = function(itemType, item) {
        var resource = resourceName(itemType);
        Restangular.all(resource).post(item).then(function(response) {
            addToInfo(itemType, response);
            return response;
        });
    };

    var remove = function(itemType, item) {
        var resource = resourceName(itemType);
        console.log(item);
        Restangular.one(resource, item.id).remove().then(function() {
            removeFromInfo(itemType, item);
        });
    };

    return {
        retrieve: retrieve,
        getAll: getAll,
        add: add,
        remove: remove
    };
});