// Ionic Starter App

// angular.module is a global place for creating, registering and retrieving Angular modules
// 'starter' is the name of this angular module example (also set in a <body> attribute in index.html)
// the 2nd parameter is an array of 'requires'
// 'starter.controllers' is found in controllers.js
angular.module('pss', ['ionic', 'ngAnimate','resource_wrapper','credentials','app','ngCookies'])
    .run(function($ionicPlatform) {
        $ionicPlatform.ready(function() {
            // Hide the accessory bar by default (remove this to show the accessory bar above the keyboard
            // for form inputs)
            if (window.cordova && window.cordova.plugins.Keyboard) {
                cordova.plugins.Keyboard.hideKeyboardAccessoryBar(true);
                cordova.plugins.Keyboard.disableScroll(true);
            }
            if (window.StatusBar) {
                // org.apache.cordova.statusbar required
                StatusBar.styleDefault();
            }
        });
    })
    .config(function($stateProvider, $urlRouterProvider,$ionicConfigProvider) {
        $ionicConfigProvider.views.transition('none');
        $ionicConfigProvider.backButton.text('');
        $ionicConfigProvider.backButton.icon('ion-arrow-left-c');
        $ionicConfigProvider.backButton.previousTitleText(false);
        $ionicConfigProvider.views.maxCache(0);
        $ionicConfigProvider.templates.maxPrefetch(0);
    });
