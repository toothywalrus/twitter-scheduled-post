'use strict';

angular.module('Posting').factory('streamService', function(Info) {
    var source = new EventSource('/stream/');

    /*function addEvent(name) {
        source.addEventListener(name, function(e) {
            listener(e, function)
        });
    }

    function listener(e) {
        var data = JSON.parse(e.data);
    }*/

    source.addEventListener('saved', function(e) {
        var data = JSON.parse(e.data);
        Info.addToInfo(data.model_name, data.item);
    });

    source.addEventListener('deleted', function(e) {
        var data = JSON.parse(e.data);
        console.log('deleted');
        Info.removeFromInfo(data.model_name, data.item);
    });

    source.addEventListener('changed', function(e) {
        var data = JSON.parse(e.data);
        console.log('changed');
        console.log(e.data);
    });

    return {

    };
});