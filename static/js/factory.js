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
    return {
        loadHotels: loadHotels,
        loadHotel: loadHotel
    }
});
