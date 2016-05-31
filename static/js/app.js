/**
 * Created by evgeniy on 29.05.16.
 */

var app = angular.module('bookingApp', ['ui.router', 'ui.bootstrap', 'ui.bootstrap.datepicker'])
    .constant('templateURL', '/static/templates/')
    .constant('apiUrl', '/api/v1/')
    .controller('hotelsCtrl', function($scope, hotels) {
        $scope.hotels = hotels;
    })
    .controller("hotelCtrl", function ($scope, $uibModal, templateURL, hotel) {
        $scope.hotel = hotel;
        $scope.openReservationDialog = openReservationDialog;

        function openReservationDialog (room) {
            $uibModal.open({
                templateUrl: templateURL + "modal.reservation.html",
                controller: 'modalReservationCtrl',
                resolve: {
                    room: function () {
                        return room;
                    }
                }
            })
        }

    })
    .controller('modalReservationCtrl', function ($scope, $uibModalInstance) {
        $scope.startDate = new Date();
        $scope.endDate = new Date();

        $scope.optionsStartDate = {
            minDate: new Date(),
            format: "yyy-mm-dd"
        };

        $scope.optionsEndDate = {
            minDate: $scope.startDate
        }

    });

