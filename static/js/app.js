/**
 * Created by evgeniy on 29.05.16.
 */

var app = angular.module('bookingApp', ['ui.router'])
    .constant('templateURL', '/static/templates/')
    .constant('apiUrl', '/api/v1/')
    .controller('hotelsCtrl', function($scope, hotels) {
        $scope.hotels = hotels;
    })
    .controller("hotelCtrl", function ($scope, hotel) {
        $scope.hotel = hotel;
    });

