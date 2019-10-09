'use strict';

angular.module('myApp.client', [])
.config(['$stateProvider',function ($stateProvider) {

    $stateProvider
        .state('root.book', {
              url: '/',
              views: {
                'container@': {
                    templateUrl: 'client/views/book.html',
                    controller: 'booksController'  
                }
              }

        });

}])
    .directive('googleplace', function() {
    return {
        require: 'ngModel',
        link: function(scope, element, attrs, model) {
            var options = {
                types: []
            };
            scope.gPlace = new google.maps.places.Autocomplete(element[0], options);

            google.maps.event.addListener(scope.gPlace, function() {
                scope.$apply(function() {
                    model.$setViewValue(element.val());
                });
            });
        }
    };
})
.controller('bookController', ['$scope','authFact',function ($scope, $state,reverseGeocode,authFact){

    function setMap(obj)
    {   
          
        reverseGeocode.geocodePosition(obj.lat, obj.lng, function(address){
          $scope.map = {control: {}, center: { latitude: obj.lat, longitude: obj.lng }, zoom: 10 };
          $scope.markerTemp = { id: 0, coords: { latitude: obj.lat, longitude : obj.lng }, window: {
            title: address,
            }
           }
          $scope.$apply();
        });
    }
    
    function setLocationMap()
    {  
      var options = {enableHighAccuracy: true};
      navigator.geolocation.getCurrentPosition(function(pos) {
          // pos = {coords:{latitude:31.4844394,longitude:74.2976333}};
          $scope.position = new google.maps.LatLng(pos.coords.latitude, pos.coords.longitude);
          var temp=JSON.stringify($scope.position);
          var obj=JSON.parse(temp);
          authFact.setLocation(temp);
          location = obj;
          setMap(obj);
        },
        function(error) {
          alert('Unable to get location: ' + error.message);
        }, options);
    }

    var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    var ws = new ReconnectingWebSocket(ws_scheme + '://127.0.0.1:8880'+ "/booking/"+authFact.randomString());
    
    $scope.options = {scrollwheel: false};
    
    $scope.getCurrentLocation=function () {
        $scope.map.zoom=15;
        $scope.marker=$scope.markerTemp;
        $scope.pickup=$scope.markerTemp.window.title;
    }
    
    $scope.disablePannel=function () {
        $scope.directions = {
        showList: false
        }
    }

    // ws.onopen = function()
    // {
    //   alert('opened');
    // };
        
    ws.onmessage = function (evt){ 
        var temp = evt.data;
        var obj=JSON.parse(temp);
        if(obj.action == 'quote'){
          var mark = { id: obj.location.uid, coords: { latitude: obj.location.lat, longitude : obj.location.lng }, window: {
            title: obj.quote,
            icon : 'https://cdn2.iconfinder.com/data/icons/location-map-simplicity/512/taxi-512.png'
            }
           }
          $scope.markers.push(mark);
          $scope.$apply();
        }
        else if(obj.action == 'location'){
          var arr = $scope.markers;
          for (var i=0; i< arr.length; i++){
            if(arr[i].id==obj.location.uid){
              arr[i].coords.latitude = obj.location.lat;
              arr[i].coords.longitude = obj.location.lng;
            }
          }
          $scope.markers = arr;
          $scope.$apply();
        }
    };
        
    ws.onclose = function()
    { 
        console.log("Connection is closed..."); 
    };


}]);