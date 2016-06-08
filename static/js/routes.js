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
                url: "/hotels/?:{page: int}&:title&:{city: int}&{position: int}&{country: int}&{min_price: int}&{max_price: int}",
                templateUrl: templateURL + "hotels.html",
                controller: 'hotelsCtrl',
                resolve: {
                    hotels: function ($stateParams, apiFactory) {
                        return apiFactory.loadHotels($stateParams);
                    },
                    countries: function (apiFactory) {
                        return apiFactory.loadCountries();
                    },
                    cities: function (apiFactory) {
                        return apiFactory.loadCities();
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
                templateUrl: templateURL + "cabinet.stats.html"
            })
            .state('cabinet', {
                url: "/cabinet",
                templateUrl: templateURL + "cabinet.stats.html",
                controller: function ($scope) {
                    $scope.things = ["A", "Set", "Of", "Things"];
                }
            });
    });