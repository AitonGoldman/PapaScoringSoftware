webpackJsonp([26],{

/***/ 154:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return PssApiProvider; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_common_http__ = __webpack_require__(54);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__angular_core__ = __webpack_require__(1);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2_rxjs_operators__ = __webpack_require__(217);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2_rxjs_operators___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_2_rxjs_operators__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3_rxjs_Observable__ = __webpack_require__(0);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3_rxjs_Observable___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_3_rxjs_Observable__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_4_rxjs_Subject__ = __webpack_require__(11);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_4_rxjs_Subject___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_4_rxjs_Subject__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_5_rxjs_observable_of__ = __webpack_require__(72);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_5_rxjs_observable_of___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_5_rxjs_observable_of__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_6_ionic_angular__ = __webpack_require__(40);
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};








/*
  Generated class for the PssApiProvider provider.

  See https://angular.io/guide/dependency-injection for more info on providers
  and Angular DI.
*/
var PssApiProvider = (function () {
    function PssApiProvider(http, loadingCtrl, toastCtrl) {
        this.http = http;
        this.loadingCtrl = loadingCtrl;
        this.toastCtrl = toastCtrl;
        this.basePssUrl = 'http://192.168.1.178:8000';
        //basePssUrl='http://0.0.0.0:8000'
        this.loading_instance = null;
        this.addTournamentMachine = this.generate_api_call('addTournamentMachine', this.basePssUrl + "/:arg/tournament_machine", 'post');
        this.addEventUsers = this.generate_api_call('addEventUsers', this.basePssUrl + "/:arg/event_user", 'post');
        this.addEventPlayers = this.generate_api_call('addEventPlayers', this.basePssUrl + "/:arg/player", 'post');
        this.createEvent = this.generate_api_call('createEvent', this.basePssUrl + "/event", 'post');
        this.createWizardEvent = this.generate_api_call('createWizardEvent', this.basePssUrl + "/wizard/event/tournament/tournament_machines", 'post');
        this.createWizardTournament = this.generate_api_call('createWizardTournament', this.basePssUrl + "/wizard/tournament/tournament_machines", 'post');
        this.createTournament = this.generate_api_call('createTournament', this.basePssUrl + "/:arg/tournament", 'post');
        this.editTournamentMachine = this.generate_api_call('editTournamentMachine', this.basePssUrl + "/:arg/tournament_machine", 'put');
        this.editTournament = this.generate_api_call('editTournament', this.basePssUrl + "/:arg/tournament", 'put');
        this.editEvent = this.generate_api_call('editEvent', this.basePssUrl + "/event", 'put');
        this.editEventUserRole = this.generate_api_call('editEventUser', this.basePssUrl + "/:arg/event_role_mapping", 'put');
        this.eventOwnerCreateRequest = this.generate_api_call('eventOwnerCreateRequest', this.basePssUrl + "/pss_user_request", 'post');
        this.eventOwnerCreateConfirm = this.generate_api_call('eventOwnerCreateConfirm', this.basePssUrl + "/pss_user_request_confirm/:arg", 'post');
        this.getAllEvents = this.generate_api_call('getAllEvents', this.basePssUrl + "/events", 'get');
        this.getAllPlayers = this.generate_api_call('getAllPlayers', this.basePssUrl + "/players", 'get');
        this.getEventPlayer = this.generate_api_call('getEventPlayer', this.basePssUrl + "/:arg/event_player/:arg", 'get');
        this.getEvent = this.generate_api_call('getEvent', this.basePssUrl + "/event/:arg", 'get');
        this.getIfpaRanking = this.generate_api_call('getIfpaRanking', this.basePssUrl + "/ifpa/:arg", 'get');
        this.getTournament = this.generate_api_call('getTournament', this.basePssUrl + "/:arg/tournament/:arg", 'get');
        this.getAllTournamentMachines = this.generate_api_call('getAllTournamentMachines', this.basePssUrl + "/:arg/:arg/tournament_machines/machines", 'get');
        this.getAllMachines = this.generate_api_call('getAllMachines', this.basePssUrl + "/machines", 'get');
        this.getAllUsers = this.generate_api_call('getAllUsers', this.basePssUrl + "/pss_users", 'get');
        this.getAllTournaments = this.generate_api_call('getAllTournaments', this.basePssUrl + "/:arg/tournaments", 'get');
        this.getAllEventsAndTournaments = this.generate_api_call('getAllEventsAndTournaments', this.basePssUrl + "/events/tournaments", 'get');
        this.loginEventOwner = this.generate_api_call('loginEventOwner', this.basePssUrl + "/auth/pss_user/login", 'post');
        this.loginUser = this.generate_api_call('loginUser', this.basePssUrl + "/auth/pss_event_user/login/:arg", 'post');
        this.loginPlayer = this.generate_api_call('loginPlayer', this.basePssUrl + "/auth/player/login/:arg", 'post');
        this.searchPlayers = this.generate_api_call('searchPlayers', this.basePssUrl + "/players/:arg", 'get');
        this.purchaseTicket = this.generate_api_call('purchaseTicket', this.basePssUrl + "/:arg/token", 'post');
        console.log('Hello PssApiProvider Provider');
    }
    PssApiProvider.prototype.makeHot = function (cold) {
        var subject = new __WEBPACK_IMPORTED_MODULE_4_rxjs_Subject__["Subject"]();
        cold.subscribe(subject);
        return new __WEBPACK_IMPORTED_MODULE_3_rxjs_Observable__["Observable"](function (observer) { return subject.subscribe(observer); });
    };
    PssApiProvider.prototype.generate_api_call = function (apiName, url, method) {
        var _this = this;
        return function () {
            var restOfArgs = [];
            for (var _i = 0; _i < arguments.length; _i++) {
                restOfArgs[_i] = arguments[_i];
            }
            console.log('trying a network op 1 ...');
            var localUrl = url;
            var postObject = null;
            if (method == "post" || method == "put") {
                postObject = restOfArgs.shift();
            }
            var localMatches = localUrl.match(/\:arg/g);
            if (restOfArgs != null && localMatches != null && localMatches.length != restOfArgs.length) {
                throw new Error("Oops - number of args in url and args given do not match");
            }
            _this.loading_instance = _this.loadingCtrl.create({
                content: 'Please wait...'
            });
            _this.loading_instance.present();
            while (localUrl.indexOf(':arg') >= 0) {
                var newUrl = localUrl.replace(":arg", restOfArgs.shift());
                localUrl = newUrl;
            }
            console.log('trying a network op 2...');
            var result_observable = _this.makeHot(_this.http.request(method, localUrl, { withCredentials: true,
                body: postObject }))
                .pipe(Object(__WEBPACK_IMPORTED_MODULE_2_rxjs_operators__["catchError"])(_this.handleError(apiName, null)));
            result_observable.subscribe(function () { _this.loading_instance.dismiss(); });
            return result_observable;
        };
    };
    PssApiProvider.prototype.handleError = function (operation, result) {
        var _this = this;
        if (operation === void 0) { operation = 'operation'; }
        var debouncer = false;
        return function (error) {
            console.log('trying a network op 3...');
            if (debouncer == false) {
                debouncer = true;
                console.log('error handling in progress...');
                console.error(error); // log to console instead
                var toast = _this.toastCtrl.create({
                    message: error.error.message,
                    duration: 99000,
                    position: 'top',
                    showCloseButton: true,
                    cssClass: "dangerToast"
                });
                toast.present();
            }
            // Let the app keep running by returning an empty result.
            return Object(__WEBPACK_IMPORTED_MODULE_5_rxjs_observable_of__["of"])(result);
        };
    };
    PssApiProvider = __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_1__angular_core__["Injectable"])(),
        __metadata("design:paramtypes", [__WEBPACK_IMPORTED_MODULE_0__angular_common_http__["a" /* HttpClient */], __WEBPACK_IMPORTED_MODULE_6_ionic_angular__["i" /* LoadingController */],
            __WEBPACK_IMPORTED_MODULE_6_ionic_angular__["n" /* ToastController */]])
    ], PssApiProvider);
    return PssApiProvider;
}());

//# sourceMappingURL=pss-api.js.map

/***/ }),

/***/ 155:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return EventAuthProvider; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_common_http__ = __webpack_require__(54);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__angular_core__ = __webpack_require__(1);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2_ngx_cookie__ = __webpack_require__(215);
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};



var roleToHomePageMap = {
    'eventowner': 'EventOwnerHomePage',
    'tournamentdirector': 'TournamentDirectorHomePage',
    'player': 'PlayerHomePage'
};
/*
  Generated class for the EventAuthProvider provider.

  See https://angular.io/guide/dependency-injection for more info on providers
  and Angular DI.
*/
var EventAuthProvider = (function () {
    function EventAuthProvider(http, _cookieService) {
        this.http = http;
        this._cookieService = _cookieService;
        this.userEventRoles = {};
        this.userLoggedInEvents = {};
        this.eventOwnerUserInfo = null;
        var userLoggedInEvents = _cookieService.getObject("userLoggedInEvents");
        var userEventRoles = _cookieService.getObject("userEventRoles");
        var eventOwnerUserInfo = _cookieService.getObject("eventOwnerUserInfo");
        console.log('Hello EventAuthProvider Provider');
        if (userLoggedInEvents != null) {
            this.userLoggedInEvents = userLoggedInEvents;
        }
        if (userEventRoles != null) {
            this.userEventRoles = userEventRoles;
        }
        if (eventOwnerUserInfo != null) {
            console.log(eventOwnerUserInfo);
            this.eventOwnerUserInfo = eventOwnerUserInfo;
        }
        else {
            console.log('not a event owner');
        }
    }
    EventAuthProvider.prototype.setEventUserLoggedIn = function (eventId, userInfo) {
        console.log('in setEventUserLoggedIn');
        if (eventId == null && userInfo.event_creator == true) {
            this.eventOwnerUserInfo = userInfo;
            this._cookieService.putObject("eventOwnerUserInfo", userInfo);
            return;
        }
        //this.userLoggedInEvents[eventId]=true;
        this.userLoggedInEvents[eventId] = userInfo;
        if (userInfo.player_id != null) {
            this.setEventRole(eventId, { event_role_name: 'player' });
        }
        if (userInfo.pss_user_id != null) {
            this.setEventRole(eventId, userInfo.roles[0]);
        }
        this._cookieService.putObject("userLoggedInEvents", this.userLoggedInEvents, { path: '/' });
        this._cookieService.putObject("userEventRoles", this.userEventRoles, { path: '/' });
        console.log('setEventUserLoggedIn debug...');
    };
    EventAuthProvider.prototype.isEventUserLoggedIn = function (eventId) {
        if (eventId in this.userLoggedInEvents) {
            return true; //this.userLoggedInEvents[eventId];
        }
        else {
            return null;
        }
    };
    EventAuthProvider.prototype.setEventRole = function (eventId, role) {
        if (eventId != null) {
            this.userEventRoles[eventId] = role;
        }
    };
    EventAuthProvider.prototype.getEventOwnerPssUserId = function () {
        if (this.eventOwnerUserInfo != null) {
            return this.eventOwnerUserInfo.pss_user_id;
        }
        else {
            return null;
        }
    };
    EventAuthProvider.prototype.getPssUserId = function (eventId) {
        if (this.userLoggedInEvents[eventId] != null) {
            return this.userLoggedInEvents[eventId].pss_user_id;
        }
        else {
            return null;
        }
    };
    EventAuthProvider.prototype.getRoleName = function (eventId) {
        if (this.eventOwnerUserInfo != null) {
            return "eventowner";
        }
        if (eventId in this.userEventRoles) {
            return this.userEventRoles[eventId].event_role_name;
        }
        else {
            return null;
        }
    };
    EventAuthProvider.prototype.getHomePage = function (eventId) {
        if (this.eventOwnerUserInfo != null) {
            return roleToHomePageMap['eventowner'];
        }
        if (this.userEventRoles[eventId]) {
            return roleToHomePageMap[this.userEventRoles[eventId].event_role_name];
        }
    };
    EventAuthProvider = __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_1__angular_core__["Injectable"])(),
        __metadata("design:paramtypes", [__WEBPACK_IMPORTED_MODULE_0__angular_common_http__["a" /* HttpClient */],
            __WEBPACK_IMPORTED_MODULE_2_ngx_cookie__["b" /* CookieService */]])
    ], EventAuthProvider);
    return EventAuthProvider;
}());

//# sourceMappingURL=event-auth.js.map

/***/ }),

/***/ 168:
/***/ (function(module, exports) {

function webpackEmptyAsyncContext(req) {
	// Here Promise.resolve().then() is used instead of new Promise() to prevent
	// uncatched exception popping up in devtools
	return Promise.resolve().then(function() {
		throw new Error("Cannot find module '" + req + "'.");
	});
}
webpackEmptyAsyncContext.keys = function() { return []; };
webpackEmptyAsyncContext.resolve = webpackEmptyAsyncContext;
module.exports = webpackEmptyAsyncContext;
webpackEmptyAsyncContext.id = 168;

/***/ }),

/***/ 212:
/***/ (function(module, exports, __webpack_require__) {

var map = {
	"../pages/add-player/add-player.module": [
		696,
		13
	],
	"../pages/create-event/create-event.module": [
		697,
		5
	],
	"../pages/create-tournament/create-tournament.module": [
		698,
		3
	],
	"../pages/edit-event/edit-event.module": [
		700,
		4
	],
	"../pages/edit-tournament/edit-tournament.module": [
		699,
		2
	],
	"../pages/event-owner-add-user/event-owner-add-user.module": [
		701,
		14
	],
	"../pages/event-owner-confirm/event-owner-confirm.module": [
		702,
		12
	],
	"../pages/event-owner-create-tournament/event-owner-create-tournament.module": [
		704,
		1
	],
	"../pages/event-owner-edit-tournament/event-owner-edit-tournament.module": [
		703,
		0
	],
	"../pages/event-owner-edit-user/event-owner-edit-user.module": [
		705,
		9
	],
	"../pages/event-owner-home/event-owner-home.module": [
		706,
		25
	],
	"../pages/event-owner-login/event-owner-login.module": [
		707,
		6
	],
	"../pages/event-owner-quick-links/event-owner-quick-links.module": [
		708,
		24
	],
	"../pages/event-owner-request/event-owner-request.module": [
		709,
		15
	],
	"../pages/event-owner-tabs/event-owner-tabs.module": [
		710,
		23
	],
	"../pages/event-owner-tournament-machines/event-owner-tournament-machines.module": [
		711,
		8
	],
	"../pages/event-select/event-select.module": [
		712,
		22
	],
	"../pages/home/home.module": [
		714,
		21
	],
	"../pages/login/login.module": [
		713,
		11
	],
	"../pages/quick-links/quick-links.module": [
		716,
		20
	],
	"../pages/results/results.module": [
		718,
		19
	],
	"../pages/success/success.module": [
		715,
		18
	],
	"../pages/tabs/tabs.module": [
		717,
		17
	],
	"../pages/ticket-purchase/ticket-purchase.module": [
		721,
		10
	],
	"../pages/tournament-director-home/tournament-director-home.module": [
		720,
		16
	],
	"../pages/tournament-machines/tournament-machines.module": [
		719,
		7
	]
};
function webpackAsyncContext(req) {
	var ids = map[req];
	if(!ids)
		return Promise.reject(new Error("Cannot find module '" + req + "'."));
	return __webpack_require__.e(ids[1]).then(function() {
		return __webpack_require__(ids[0]);
	});
};
webpackAsyncContext.keys = function webpackAsyncContextKeys() {
	return Object.keys(map);
};
webpackAsyncContext.id = 212;
module.exports = webpackAsyncContext;

/***/ }),

/***/ 355:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return TitleServiceProvider; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_common_http__ = __webpack_require__(54);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__angular_core__ = __webpack_require__(1);
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};


/*
  Generated class for the TitleServiceProvider provider.

  See https://angular.io/guide/dependency-injection for more info on providers
  and Angular DI.
*/
var TitleServiceProvider = (function () {
    function TitleServiceProvider(http) {
        this.http = http;
        this.title = undefined;
        console.log('Hello TitleServiceProvider Provider');
        this.title = 'aiton';
    }
    TitleServiceProvider.prototype.setTitle = function (newTitle) {
        this.title = newTitle;
    };
    TitleServiceProvider.prototype.getTitle = function () {
        return this.title;
    };
    TitleServiceProvider = __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_1__angular_core__["Injectable"])(),
        __metadata("design:paramtypes", [__WEBPACK_IMPORTED_MODULE_0__angular_common_http__["a" /* HttpClient */]])
    ], TitleServiceProvider);
    return TitleServiceProvider;
}());

//# sourceMappingURL=title-service.js.map

/***/ }),

/***/ 358:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return AutoCompleteProvider; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_common_http__ = __webpack_require__(54);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__angular_core__ = __webpack_require__(1);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__providers_pss_api_pss_api__ = __webpack_require__(154);
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};



/*
  Generated class for the AutoCompleteProvider provider.

  See https://angular.io/guide/dependency-injection for more info on providers
  and Angular DI.
*/
var AutoCompleteProvider = (function () {
    function AutoCompleteProvider(http, pssApi) {
        this.http = http;
        this.pssApi = pssApi;
        this.labelAttribute = "machine_name";
        this.formValueAttribute = "";
        this.players = null;
        this.url = null;
        console.log('Hello AutoCompleteProvider Provider');
    }
    AutoCompleteProvider.prototype.setMachines = function (machines) {
        //this.machines=machines;        
        this.items = machines;
        this.itemFieldToMatch = 'machine_name';
        this.labelAttribute = "machine_name";
    };
    AutoCompleteProvider.prototype.addUsers = function (user) {
        this.items.push(user);
    };
    AutoCompleteProvider.prototype.setUsers = function (users) {
        this.items = users;
        this.itemFieldToMatch = 'full_user_name';
        this.labelAttribute = "full_user_name";
    };
    AutoCompleteProvider.prototype.setEndpoint = function (typeOfEndpoint) {
        if (typeOfEndpoint == "allPlayers") {
        }
    };
    AutoCompleteProvider.prototype.setPlayerSearchType = function (typeOfSearch, observable) {
        var url = "";
        if (typeOfSearch == "allPlayers") {
            url = "http://192.168.1.178:8000/players/";
        }
        this.itemFieldToMatch = 'player_full_name';
        this.labelAttribute = "player_full_name";
        this.url = url;
        this.loadingObservable = observable;
    };
    AutoCompleteProvider.prototype.setPlayers = function (allPlayers) {
        var _this = this;
        if (allPlayers == true) {
            this.pssApi.getAllPlayers()
                .subscribe(function (result) { _this.players = result.data; _this.items = _this.players; });
        }
    };
    AutoCompleteProvider.prototype.getResults = function (name) {
        var _this = this;
        if (this.url != null) {
            console.log('in getResults...');
            return this.http.get(this.url + name)['map'](function (result) { return result.data; })['do'](function (input) { _this.loadingObservable(input); });
            //return this.pssApi.searchPlayers(name)
        }
        var regex = new RegExp(name.toLowerCase());
        return this.items.filter(function (item) {
            var matches = item[_this.itemFieldToMatch].toLowerCase().match(regex);
            return (matches != null && matches.length > 0);
        });
    };
    AutoCompleteProvider = __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_1__angular_core__["Injectable"])(),
        __metadata("design:paramtypes", [__WEBPACK_IMPORTED_MODULE_0__angular_common_http__["a" /* HttpClient */], __WEBPACK_IMPORTED_MODULE_2__providers_pss_api_pss_api__["a" /* PssApiProvider */]])
    ], AutoCompleteProvider);
    return AutoCompleteProvider;
}());

//# sourceMappingURL=auto-complete.js.map

/***/ }),

/***/ 360:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return CustomComponentsModule; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__(1);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__custom_header_custom_header__ = __webpack_require__(400);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2_ionic_angular__ = __webpack_require__(40);
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};



var CustomComponentsModule = (function () {
    function CustomComponentsModule() {
    }
    CustomComponentsModule = __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["NgModule"])({
            declarations: [__WEBPACK_IMPORTED_MODULE_1__custom_header_custom_header__["a" /* CustomHeaderComponent */]],
            imports: [__WEBPACK_IMPORTED_MODULE_2_ionic_angular__["f" /* IonicModule */]],
            exports: [__WEBPACK_IMPORTED_MODULE_1__custom_header_custom_header__["a" /* CustomHeaderComponent */]]
        })
    ], CustomComponentsModule);
    return CustomComponentsModule;
}());

//# sourceMappingURL=custom-components.module.js.map

/***/ }),

/***/ 361:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return ExpandableModule; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__(1);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1_ionic_angular__ = __webpack_require__(40);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__expandable__ = __webpack_require__(672);
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};



var ExpandableModule = (function () {
    function ExpandableModule() {
    }
    ExpandableModule = __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["NgModule"])({
            imports: [__WEBPACK_IMPORTED_MODULE_1_ionic_angular__["g" /* IonicPageModule */].forChild(__WEBPACK_IMPORTED_MODULE_2__expandable__["a" /* ExpandableComponent */])],
            declarations: [__WEBPACK_IMPORTED_MODULE_2__expandable__["a" /* ExpandableComponent */]],
            exports: [__WEBPACK_IMPORTED_MODULE_2__expandable__["a" /* ExpandableComponent */]]
        })
    ], ExpandableModule);
    return ExpandableModule;
}());

//# sourceMappingURL=expandable.module.js.map

/***/ }),

/***/ 362:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
Object.defineProperty(__webpack_exports__, "__esModule", { value: true });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_platform_browser_dynamic__ = __webpack_require__(363);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__app_module__ = __webpack_require__(367);


Object(__WEBPACK_IMPORTED_MODULE_0__angular_platform_browser_dynamic__["a" /* platformBrowserDynamic */])().bootstrapModule(__WEBPACK_IMPORTED_MODULE_1__app_module__["a" /* AppModule */]);
//# sourceMappingURL=main.js.map

/***/ }),

/***/ 367:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return AppModule; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_platform_browser__ = __webpack_require__(31);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__angular_core__ = __webpack_require__(1);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2_ionic_angular__ = __webpack_require__(40);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3__ionic_native_splash_screen__ = __webpack_require__(351);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_4__ionic_native_status_bar__ = __webpack_require__(354);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_5__angular_common_http__ = __webpack_require__(54);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_6__app_component__ = __webpack_require__(693);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_7__providers_title_service_title_service__ = __webpack_require__(355);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_8__providers_event_auth_event_auth__ = __webpack_require__(155);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_9__providers_pss_api_pss_api__ = __webpack_require__(154);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_10__angular_forms__ = __webpack_require__(21);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_11_ionic2_auto_complete__ = __webpack_require__(359);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_12__providers_auto_complete_auto_complete__ = __webpack_require__(358);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_13__components_expandable_expandable_module__ = __webpack_require__(361);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_14__angular_platform_browser_animations__ = __webpack_require__(694);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_15_angular2_notifications__ = __webpack_require__(356);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_15_angular2_notifications___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_15_angular2_notifications__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_16_angular2_image_upload__ = __webpack_require__(357);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_17_ngx_cookie__ = __webpack_require__(215);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_18__components_custom_components_module__ = __webpack_require__(360);
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};



















var AppModule = (function () {
    function AppModule() {
    }
    AppModule = __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_1__angular_core__["NgModule"])({
            declarations: [
                __WEBPACK_IMPORTED_MODULE_6__app_component__["a" /* MyApp */]
            ],
            imports: [
                __WEBPACK_IMPORTED_MODULE_0__angular_platform_browser__["BrowserModule"],
                __WEBPACK_IMPORTED_MODULE_2_ionic_angular__["f" /* IonicModule */].forRoot(__WEBPACK_IMPORTED_MODULE_6__app_component__["a" /* MyApp */], {}, {
                    links: [
                        { loadChildren: '../pages/add-player/add-player.module#AddPlayerPageModule', name: 'AddPlayerPage', segment: 'AddPlyer/:eventId', priority: 'low', defaultHistory: [] },
                        { loadChildren: '../pages/create-event/create-event.module#CreateEventPageModule', name: 'CreateEventPage', segment: 'CreateEventPage/:actionType/:wizardMode', priority: 'low', defaultHistory: [] },
                        { loadChildren: '../pages/create-tournament/create-tournament.module#CreateTournamentPageModule', name: 'CreateTournamentPage', segment: 'CreateTournament/:eventId/:actionType', priority: 'low', defaultHistory: [] },
                        { loadChildren: '../pages/edit-tournament/edit-tournament.module#EditTournamentPageModule', name: 'EditTournamentPage', segment: 'EditTournament/:eventId/:tournamentId/:actionType', priority: 'low', defaultHistory: [] },
                        { loadChildren: '../pages/edit-event/edit-event.module#EditEventPageModule', name: 'EditEventPage', segment: 'EditEventPage/:actionType/:eventId', priority: 'low', defaultHistory: [] },
                        { loadChildren: '../pages/event-owner-add-user/event-owner-add-user.module#EventOwnerAddUserPageModule', name: 'EventOwnerAddUserPage', segment: 'EventOwnerAddUser/:eventId', priority: 'low', defaultHistory: [] },
                        { loadChildren: '../pages/event-owner-confirm/event-owner-confirm.module#EventOwnerConfirmPageModule', name: 'EventOwnerConfirmPage', segment: 'EventOwnerConfirm/:itsdangerousstring', priority: 'low', defaultHistory: [] },
                        { loadChildren: '../pages/event-owner-edit-tournament/event-owner-edit-tournament.module#EventOwnerEditTournamentPageModule', name: 'EventOwnerEditTournamentPage', segment: 'EventOwnerEditTournament/:eventId/:tournamentId/:actionType', priority: 'low', defaultHistory: [] },
                        { loadChildren: '../pages/event-owner-create-tournament/event-owner-create-tournament.module#EventOwnerCreateTournamentPageModule', name: 'EventOwnerCreateTournamentPage', segment: 'EventOwnerCreateTournament/:eventId/:actionType/:wizardMode', priority: 'low', defaultHistory: [] },
                        { loadChildren: '../pages/event-owner-edit-user/event-owner-edit-user.module#EventOwnerEditUserPageModule', name: 'EventOwnerEditUserPage', segment: 'EventOwnerEditUser/:eventId', priority: 'low', defaultHistory: [] },
                        { loadChildren: '../pages/event-owner-home/event-owner-home.module#EventOwnerHomePageModule', name: 'EventOwnerHomePage', segment: 'event-owner-home', priority: 'low', defaultHistory: [] },
                        { loadChildren: '../pages/event-owner-login/event-owner-login.module#EventOwnerLoginPageModule', name: 'EventOwnerLoginPage', segment: 'event-owner-login', priority: 'low', defaultHistory: [] },
                        { loadChildren: '../pages/event-owner-quick-links/event-owner-quick-links.module#EventOwnerQuickLinksPageModule', name: 'EventOwnerQuickLinksPage', segment: 'event-owner-quick-links', priority: 'low', defaultHistory: [] },
                        { loadChildren: '../pages/event-owner-request/event-owner-request.module#EventOwnerRequestPageModule', name: 'EventOwnerRequestPage', segment: 'event-owner-request', priority: 'low', defaultHistory: [] },
                        { loadChildren: '../pages/event-owner-tabs/event-owner-tabs.module#EventOwnerTabsPageModule', name: 'EventOwnerTabsPage', segment: 'event-owner-tabs', priority: 'low', defaultHistory: [] },
                        { loadChildren: '../pages/event-owner-tournament-machines/event-owner-tournament-machines.module#EventOwnerTournamentMachinesPageModule', name: 'EventOwnerTournamentMachinesPage', segment: 'EventOwnerTournamentMachines/:eventId/:tournamentId', priority: 'low', defaultHistory: [] },
                        { loadChildren: '../pages/event-select/event-select.module#EventSelectPageModule', name: 'EventSelectPage', segment: 'event-select', priority: 'low', defaultHistory: [] },
                        { loadChildren: '../pages/login/login.module#LoginPageModule', name: 'LoginPage', segment: 'login/:eventId', priority: 'low', defaultHistory: [] },
                        { loadChildren: '../pages/home/home.module#HomePageModule', name: 'HomePage', segment: 'HomePage/:eventId', priority: 'low', defaultHistory: [] },
                        { loadChildren: '../pages/success/success.module#SuccessPageModule', name: 'SuccessPage', segment: 'Success/:eventId', priority: 'low', defaultHistory: [] },
                        { loadChildren: '../pages/quick-links/quick-links.module#QuickLinksPageModule', name: 'QuickLinksPage', segment: 'quick-links', priority: 'low', defaultHistory: [] },
                        { loadChildren: '../pages/tabs/tabs.module#TabsPageModule', name: 'TabsPage', segment: 'tabs', priority: 'low', defaultHistory: [] },
                        { loadChildren: '../pages/results/results.module#ResultsPageModule', name: 'ResultsPage', segment: 'results', priority: 'low', defaultHistory: [] },
                        { loadChildren: '../pages/tournament-machines/tournament-machines.module#TournamentMachinesPageModule', name: 'TournamentMachinesPage', segment: 'TournamentMachines/:eventId/:tournamentId', priority: 'low', defaultHistory: [] },
                        { loadChildren: '../pages/tournament-director-home/tournament-director-home.module#TournamentDirectorHomePageModule', name: 'TournamentDirectorHomePage', segment: 'TournamentDirectorHomePage/:eventId', priority: 'low', defaultHistory: [] },
                        { loadChildren: '../pages/ticket-purchase/ticket-purchase.module#TicketPurchasePageModule', name: 'TicketPurchasePage', segment: 'TicketPurchasePage/:eventId', priority: 'low', defaultHistory: [] }
                    ]
                }),
                __WEBPACK_IMPORTED_MODULE_5__angular_common_http__["b" /* HttpClientModule */],
                __WEBPACK_IMPORTED_MODULE_10__angular_forms__["a" /* FormsModule */],
                __WEBPACK_IMPORTED_MODULE_11_ionic2_auto_complete__["a" /* AutoCompleteModule */],
                __WEBPACK_IMPORTED_MODULE_13__components_expandable_expandable_module__["a" /* ExpandableModule */],
                __WEBPACK_IMPORTED_MODULE_14__angular_platform_browser_animations__["a" /* BrowserAnimationsModule */],
                __WEBPACK_IMPORTED_MODULE_15_angular2_notifications__["SimpleNotificationsModule"].forRoot(),
                __WEBPACK_IMPORTED_MODULE_16_angular2_image_upload__["a" /* ImageUploadModule */].forRoot(),
                __WEBPACK_IMPORTED_MODULE_17_ngx_cookie__["a" /* CookieModule */].forRoot(),
                __WEBPACK_IMPORTED_MODULE_18__components_custom_components_module__["a" /* CustomComponentsModule */]
            ],
            bootstrap: [__WEBPACK_IMPORTED_MODULE_2_ionic_angular__["d" /* IonicApp */]],
            entryComponents: [
                __WEBPACK_IMPORTED_MODULE_6__app_component__["a" /* MyApp */]
            ],
            providers: [
                __WEBPACK_IMPORTED_MODULE_4__ionic_native_status_bar__["a" /* StatusBar */],
                __WEBPACK_IMPORTED_MODULE_3__ionic_native_splash_screen__["a" /* SplashScreen */],
                { provide: __WEBPACK_IMPORTED_MODULE_1__angular_core__["ErrorHandler"], useClass: __WEBPACK_IMPORTED_MODULE_2_ionic_angular__["e" /* IonicErrorHandler */] },
                __WEBPACK_IMPORTED_MODULE_7__providers_title_service_title_service__["a" /* TitleServiceProvider */],
                __WEBPACK_IMPORTED_MODULE_8__providers_event_auth_event_auth__["a" /* EventAuthProvider */],
                __WEBPACK_IMPORTED_MODULE_9__providers_pss_api_pss_api__["a" /* PssApiProvider */],
                __WEBPACK_IMPORTED_MODULE_12__providers_auto_complete_auto_complete__["a" /* AutoCompleteProvider */]
            ]
        })
    ], AppModule);
    return AppModule;
}());

//# sourceMappingURL=app.module.js.map

/***/ }),

/***/ 400:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return CustomHeaderComponent; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__(1);
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
/**
 * Generated class for the CustomHeaderComponent component.
 *
 * See https://angular.io/api/core/Component for more info on Angular
 * Components.
 */

var CustomHeaderComponent = (function () {
    function CustomHeaderComponent() {
    }
    CustomHeaderComponent.prototype.goGoCustomHeader = function () {
    };
    __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["Input"])(),
        __metadata("design:type", Object)
    ], CustomHeaderComponent.prototype, "homePage", void 0);
    __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["Input"])(),
        __metadata("design:type", Object)
    ], CustomHeaderComponent.prototype, "eventId", void 0);
    CustomHeaderComponent = __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["Component"])({
            selector: 'custom-headers',template:/*ion-inline-start:"/Users/agoldma/git/github/TD/front_v2/src/components/custom-header/custom-header.html"*/'<ion-navbar>\n  <ion-buttons end hideWhen=\'mobile\'>\n    <button icon-only ion-button [navPush]="homePage" [navParams]="{eventId:eventId}" >{{homePage}}</button>\n  </ion-buttons>\n</ion-navbar>\n\n'/*ion-inline-end:"/Users/agoldma/git/github/TD/front_v2/src/components/custom-header/custom-header.html"*/
        })
    ], CustomHeaderComponent);
    return CustomHeaderComponent;
}());

//# sourceMappingURL=custom-header.js.map

/***/ }),

/***/ 672:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return ExpandableComponent; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__(1);
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};

var ExpandableComponent = (function () {
    function ExpandableComponent(renderer) {
        this.renderer = renderer;
    }
    ExpandableComponent.prototype.ngAfterViewInit = function () {
        this.renderer.setElementStyle(this.expandWrapper.nativeElement, 'height', this.expandHeight + 'px');
    };
    __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["ViewChild"])('expandWrapper', { read: __WEBPACK_IMPORTED_MODULE_0__angular_core__["ElementRef"] }),
        __metadata("design:type", Object)
    ], ExpandableComponent.prototype, "expandWrapper", void 0);
    __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["Input"])('expanded'),
        __metadata("design:type", Object)
    ], ExpandableComponent.prototype, "expanded", void 0);
    __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["Input"])('expandHeight'),
        __metadata("design:type", Object)
    ], ExpandableComponent.prototype, "expandHeight", void 0);
    ExpandableComponent = __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["Component"])({
            selector: 'expandable',template:/*ion-inline-start:"/Users/agoldma/git/github/TD/front_v2/src/components/expandable/expandable.html"*/'<div #expandWrapper class=\'expand-wrapper\' [class.collapsed]="!expanded">\n    <ng-content></ng-content>\n</div>\n'/*ion-inline-end:"/Users/agoldma/git/github/TD/front_v2/src/components/expandable/expandable.html"*/
        }),
        __metadata("design:paramtypes", [__WEBPACK_IMPORTED_MODULE_0__angular_core__["Renderer"]])
    ], ExpandableComponent);
    return ExpandableComponent;
}());

//# sourceMappingURL=expandable.js.map

/***/ }),

/***/ 693:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return MyApp; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__(1);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1_ionic_angular__ = __webpack_require__(40);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__ionic_native_status_bar__ = __webpack_require__(354);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3__ionic_native_splash_screen__ = __webpack_require__(351);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_4__providers_title_service_title_service__ = __webpack_require__(355);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_5__providers_event_auth_event_auth__ = __webpack_require__(155);
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};






var MyApp = (function () {
    function MyApp(platform, statusBar, splashScreen, titleService, eventAuth) {
        this.titleService = titleService;
        this.eventAuth = eventAuth;
        platform.ready().then(function () {
            // Okay, so the platform is ready and our plugins are available.
            // Here you can do any higher level native things you might need.
            statusBar.styleDefault();
            splashScreen.hide();
        });
    }
    MyApp = __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["Component"])({template:/*ion-inline-start:"/Users/agoldma/git/github/TD/front_v2/src/app/app.html"*/'<ion-menu [content]="content">\n  <ion-header>\n    <ion-toolbar>\n      <ion-title>Menu</ion-title>\n    </ion-toolbar>\n  </ion-header>\n \n  <ion-content>\n    <ion-list>\n      <button ion-item menuClose>\n        hi there\n      </button>\n    </ion-list>\n  </ion-content>\n</ion-menu>\n<!-- main navigation -->\n<!--\n<ion-header hideWhen="mobile">\n  <ion-navbar>\n    <ion-title>Pss</ion-title>\n    <ion-buttons end>\n      <button icon-only ion-button [navPush]="\'LoginPage\'" [navParams]="getEventIdName()" >Login</button>\n      <button icon-only ion-button>Results</button>\n      <button icon-only ion-button>Queues</button>\n      <button *ngIf="eventAuth.getRoleName(eventId)" icon-only ion-button (click)="menuNav(getRolePage())">{{eventAuth.getRoleName(eventId)}}</button>\n    </ion-buttons>\n  </ion-navbar>\n</ion-header>\n-->\n\n<ion-nav [root]="\'EventSelectPage\'" [rootParams]="{eventId:eventId,eventName:eventName}" #content swipeBackEnabled="false">\n</ion-nav>\n'/*ion-inline-end:"/Users/agoldma/git/github/TD/front_v2/src/app/app.html"*/
        }),
        __metadata("design:paramtypes", [__WEBPACK_IMPORTED_MODULE_1_ionic_angular__["l" /* Platform */], __WEBPACK_IMPORTED_MODULE_2__ionic_native_status_bar__["a" /* StatusBar */],
            __WEBPACK_IMPORTED_MODULE_3__ionic_native_splash_screen__["a" /* SplashScreen */], __WEBPACK_IMPORTED_MODULE_4__providers_title_service_title_service__["a" /* TitleServiceProvider */],
            __WEBPACK_IMPORTED_MODULE_5__providers_event_auth_event_auth__["a" /* EventAuthProvider */]])
    ], MyApp);
    return MyApp;
}());

//# sourceMappingURL=app.component.js.map

/***/ })

},[362]);
//# sourceMappingURL=main.js.map