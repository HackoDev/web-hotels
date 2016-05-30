/**
 * Created by evgeniy on 30.05.16.
 */
app
    .config(function($stateProvider, templateURL) {
        console.log(templateURL);
        //
        // Now set up the states
        $stateProvider
            .state('index', {
                url: '/',
                templateUrl: templateURL
            })
            .state('hotels', {
                url: "/hotels/?:page&:title&city&country",
                templateUrl: templateURL + "hotels.html",
                controller: 'hotelsCtrl',
                resolve: {
                    hotels: function ($stateParams, apiFactory) {
                        return apiFactory.loadHotels($stateParams);
                    }
                }
            })
            .state('hotel_details', {
                url: "/hotels/{id: int}/",
                templateUrl: templateURL + "hotel.details.html",
                controller: "hotelCtrl",
                resolve: {
                    hotel: function ($stateParams, apiFactory) {
                        return apiFactory.loadHotel($stateParams.id);
                    }
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