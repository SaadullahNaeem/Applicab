'use strict';

// Declare app level module which depends on views, and components
angular.module('myApp', [
  'ui.router', 'ngResource','ngCookies','firebase','uiGmapgoogle-maps','AngularReverseGeocode',
  'myApp.driver','myApp.client',
])
.constant('SOCKET_URL', '://blooming-wildwood-98566.herokuapp.com')
.constant('APP_URL', 'https://blooming-wildwood-98566.herokuapp.com/zkjih3y3bi3u9dbjnnn9no8hyughvbv2j8jh7d7/api/')
.config(['$locationProvider', '$urlRouterProvider', function($locationProvider, $urlRouterProvider) {  
  var config = {
        apiKey: "AIzaSyCtOj-6gZR2odhayz7eZLw3QpgCk_x7tXE",
        authDomain: "applicab-7255d.firebaseapp.com",
        databaseURL: "https://applicab-7255d.firebaseio.com",
        projectId: "applicab-7255d",
        storageBucket: "applicab-7255d.appspot.com",
        messagingSenderId: "246452028918"
  };
  firebase.initializeApp(config);
  
  $urlRouterProvider.otherwise("/");
  $locationProvider.html5Mode(true);

}]);