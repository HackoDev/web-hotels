/**
 * Created by evgeniy on 29.05.16.
 */

var app = angular.module('bookingApp', ['ui.router', 'ui.bootstrap', 'ui.bootstrap.datepicker'])
    .constant('templateURL', '/static/templates/')
    .constant('apiUrl', '/api/v1/')
    .controller('hotelsCtrl', function($scope, $state, $stateParams, hotels, countries, cities) {
        $scope.hotels = hotels;
        $scope.countries = countries;
        $scope.cities = cities;
        $scope.positions = [2, 3, 4, 5];
        $scope.searchParams = angular.copy($stateParams);
        $scope.search = search;

        /**
         * @description
         *
         * Поиск отелей по введенным данным в форме
         * Вызывается при клике на кнопку поиск
         *
         */
        function search () {
            $state.go("hotels", $scope.searchParams);
        }
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
    .controller('modalReservationCtrl', function ($scope, $uibModalInstance, apiFactory , room) {
        $scope.room = room;
        $scope.startDate = new Date();
        $scope.endDate = new Date();

        $scope.optionsStartDate = {
            minDate: new Date(),
            format: "yyy-mm-dd"
        };

        $scope.optionsEndDate = {
            minDate: $scope.startDate
        };

        $scope.setReservation = setReservation;

        /**
         * @description
         *
         * Бронирование номера
         */
        function setReservation() {
            var endDateStr = [$scope.startDate.getFullYear(), $scope.startDate.getMonth() + 1, $scope.startDate.getDate()].join("-"),
                startDateStr = [$scope.endDate.getFullYear(), $scope.endDate.getMonth() + 1, $scope.endDate.getDate()].join("-");
            var sendData = {
                first_name: $scope.first_name,
                last_name: $scope.last_name,
                middle_name: $scope.middle_name,
                start_date_time: startDateStr,
                end_date_time: endDateStr
            }
            apiFactory.setReservation(room.id, sendData)
                .then(function() {
                    alert("Номер успешно забронирован");
                    $uibModalInstance.close("cancel");
                });
        }
    });

