/**
 * Created by evgeniy on 29.05.16.
 */

angular.module('bookingApp', ['ui.router'])
    .constant('templateURL', '/static/templates/partials/')
    .config(function($stateProvider, templateURL) {
        console.log(templateURL);
    //
    // Now set up the states
    $stateProvider
        .state('index', {
            url: '/',
            template: "<h1>Главная</h1>"
        })
        .state('hotels', {
            url: "/hotels/",
            template: "Отели"
        })
        .state('hotel_detail', {
            url: "/hotels/{id: int}/",
            template: "детализация отеля",
            controller: function ($scope) {
                $scope.items = ["A", "List", "Of", "Items"];
            }
        })
        .state('room', {
            url: "/room/{id: int}/",
            template: "Номер"
        })
        .state('cabinet', {
            url: "/cabinet",
            template: "Личный кабинет",
            controller: function ($scope) {
                $scope.things = ["A", "Set", "Of", "Things"];
            }
        });
});