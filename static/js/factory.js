/**
 * Created by evgeniy on 30.05.16.
 */
app.factory('apiFactory', function($rootScope, $http, $q, apiUrl) {

    /**
     * @description
     *
     * Загрузка списка отелей
     *
     * @param params Object Параметры поиска (page, title and etc.)
     * @returns {*} Promise
     */
    function loadHotels (params) {
        var deferred = $q.defer();
        $http.get(apiUrl + 'hotels/?' + angular.element.param(params))
            .success(function (hotelsData) {
                deferred.resolve(hotelsData);
            })
            .error(function (errorData, headers, status) {
                deferred.reject({data: errorData, headers: headers, code: status});
            });
        return deferred.promise;

    }

    /**
     * @description
     *
     * Загрузка стран для поиска
     *
     * @returns {*} Promise
     */
    function loadCountries () {
        var deferred = $q.defer();
        $http.get(apiUrl + 'countries/?formart=json')
            .success(function (countries) {
                deferred.resolve(countries);
            })
            .error(function (errorData, headers, status) {
                deferred.reject({data: errorData, headers: headers, code: status});
            });
        return deferred.promise;
    }

    /**
     * @description
     *
     * Загрузка городов для поиска
     *
     * @returns {*} Promise
     */
    function loadCities () {
        var deferred = $q.defer();
        $http.get(apiUrl + 'cities/?formart=json')
            .success(function (countries) {
                deferred.resolve(countries);
            })
            .error(function (errorData, headers, status) {
                deferred.reject({data: errorData, headers: headers, code: status});
            });
        return deferred.promise;
    }

    /**
     * @description
     *
     * Загрузка данных об отеле
     *
     * @param hotelId int Идентификатор отеля
     * @returns {*} Promise
     */

    function loadHotel (hotelId) {
        var deferred = $q.defer();
        $http.get(apiUrl + 'hotels/' + hotelId + "/")
            .success(function (hotelsData) {
                deferred.resolve(hotelsData);
            })
            .error(function (errorData, headers, status) {
                deferred.reject({data: errorData, headers: headers, code: status});
            });
        return deferred.promise;
    }


    /**
     * @description
     *
     * Бронирование отеля
     *
     * @param roomId int Идентификатор номера
     * @param sendData {Object} Данные для бронирования
     * @returns {*} Promise
     */

    function setReservation (roomId, sendData) {
        var deferred = $q.defer();
        $http.post(apiUrl + 'rooms/' + roomId + "/", sendData)
            .success(function (hotelsData) {
                deferred.resolve(hotelsData);
            })
            .error(function (errorData, headers, status) {
                deferred.reject({data: errorData, headers: headers, code: status});
            });
        return deferred.promise;

    }
    return {
        loadHotels: loadHotels,
        loadCountries: loadCountries,
        loadCities: loadCities,
        loadHotel: loadHotel,
        setReservation: setReservation
    }
});
