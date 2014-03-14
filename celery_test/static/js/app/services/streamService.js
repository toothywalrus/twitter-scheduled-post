'use strict';

angular.module('Posting').factory('streamService', function(Info) {
    var source = new EventSource('/stream/');

    source.addEventListener('saved', function(e) {
        var data = JSON.parse(e.data);
        console.log(e.data);
        Info.addToInfo(data.model_name, data.item);
    });

    source.addEventListener('deleted', function(e) {
        var data = JSON.parse(e.data);
        Info.removeFromInfo(data.model_name, data.item);
    });

    return {};
});