webpackJsonp([2],{

/***/ 703:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
Object.defineProperty(__webpack_exports__, "__esModule", { value: true });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "EventOwnerLoginPageModule", function() { return EventOwnerLoginPageModule; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__(1);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1_ionic_angular__ = __webpack_require__(40);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__event_owner_login__ = __webpack_require__(731);
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};



var EventOwnerLoginPageModule = (function () {
    function EventOwnerLoginPageModule() {
    }
    EventOwnerLoginPageModule = __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["NgModule"])({
            declarations: [
                __WEBPACK_IMPORTED_MODULE_2__event_owner_login__["a" /* EventOwnerLoginPage */],
            ],
            imports: [
                __WEBPACK_IMPORTED_MODULE_1_ionic_angular__["g" /* IonicPageModule */].forChild(__WEBPACK_IMPORTED_MODULE_2__event_owner_login__["a" /* EventOwnerLoginPage */]),
            ],
        })
    ], EventOwnerLoginPageModule);
    return EventOwnerLoginPageModule;
}());

//# sourceMappingURL=event-owner-login.module.js.map

/***/ }),

/***/ 718:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return PssPageComponent; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__(1);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1_ionic_angular__ = __webpack_require__(40);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__providers_event_auth_event_auth__ = __webpack_require__(155);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3__providers_pss_api_pss_api__ = __webpack_require__(154);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_4_angular2_notifications__ = __webpack_require__(356);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_4_angular2_notifications___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_4_angular2_notifications__);
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
 * Generated class for the TopNavComponent component.
 *
 * See https://angular.io/api/core/Component for more info on Angular
 * Components.
 */
var PssPageComponent = (function () {
    function PssPageComponent(eventAuth, navParams, navCtrl, appCtrl, pssApi, platform, notificationsService) {
        this.eventAuth = eventAuth;
        this.navParams = navParams;
        this.navCtrl = navCtrl;
        this.appCtrl = appCtrl;
        this.pssApi = pssApi;
        this.platform = platform;
        this.notificationsService = notificationsService;
        this.eventId = null;
        this.eventName = null;
        this.tournamentId = null;
        this.hideBackButton = false;
        this.eventId = navParams.get('eventId');
        this.eventName = navParams.get('eventName');
        console.log('Hello PssPageComponent Component');
        //        console.log(instance.constructor.name)
    }
    PssPageComponent.prototype.buildNavParams = function (params) {
        if (this.eventId != null && this.eventId != undefined) {
            params['eventId'] = this.eventId;
            params['eventName'] = this.eventName;
        }
        return params;
    };
    PssPageComponent.prototype.getHomePageString = function (eventId) {
        if (eventId == null) {
            eventId = this.eventId;
        }
        var role = this.eventAuth.getRoleName(eventId);
        console.log('in getHomePageString...');
        console.log(role);
        if (role == "tournamentdirector") {
            return 'TournamentDirectorHomePage';
        }
        if (role == "eventowner") {
            return 'EventOwnerHomePage';
        }
        if (role == null) {
            return 'HomePage';
        }
    };
    PssPageComponent.prototype.pushRootPage = function (page, params) {
        if (params === void 0) { params = {}; }
        this.appCtrl.getRootNav().push(page, params);
    };
    PssPageComponent.prototype.pushPageWithNoBackButton = function (pageName, navParams, tabIndex) {
        var _this = this;
        console.log('in push page with no back button...');
        if (tabIndex != null) {
            console.log(tabIndex);
            console.log('in push page with no back button...2');
            this.navCtrl.parent.getByIndex(tabIndex).setRoot(pageName, navParams, { animate: false });
            console.log('in push page with no back button...3');
            this.navCtrl.parent.select(tabIndex);
            console.log('in push page with no back button...4');
            return;
        }
        console.log('page name is ...' + pageName);
        this.navCtrl.getActive().willLeave.subscribe(function () {
            _this.navCtrl.last().showBackButton(false);
        });
        this.navCtrl.push(pageName, this.buildNavParams(navParams));
    };
    PssPageComponent.prototype.expand = function (item) {
        item.expanded = item.expanded == false ? true : false;
    };
    PssPageComponent.prototype.generateEditTournamentProcessor = function (message_string) {
        var _this = this;
        return function (result) {
            if (result == null) {
                return;
            }
            _this.notificationsService.success("Success", message_string, {
                timeOut: 0,
                position: ["top", "right"],
                theClass: 'poop'
            });
        };
    };
    PssPageComponent.prototype.onTournamentToggle = function (eventId, tournament) {
        tournament.active = tournament.active != true;
        var stringDescription = tournament.active != true ? "deactivated" : "activated";
        this.pssApi.editTournament(tournament, eventId)
            .subscribe(this.generateEditTournamentProcessor(tournament.tournament_name + " has been " + stringDescription));
    };
    PssPageComponent = __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["Component"])({
            selector: 'pss-page',template:/*ion-inline-start:"/Users/agoldma/git/github/TD/front_v2/src/components/pss-page/pss-page.html"*/'<!-- Generated template for the TopNavComponent component -->\n<div>\n  {{text}}\n</div>\n'/*ion-inline-end:"/Users/agoldma/git/github/TD/front_v2/src/components/pss-page/pss-page.html"*/
        }),
        __metadata("design:paramtypes", [typeof (_a = typeof __WEBPACK_IMPORTED_MODULE_2__providers_event_auth_event_auth__["a" /* EventAuthProvider */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_2__providers_event_auth_event_auth__["a" /* EventAuthProvider */]) === "function" && _a || Object, typeof (_b = typeof __WEBPACK_IMPORTED_MODULE_1_ionic_angular__["k" /* NavParams */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_1_ionic_angular__["k" /* NavParams */]) === "function" && _b || Object, typeof (_c = typeof __WEBPACK_IMPORTED_MODULE_1_ionic_angular__["j" /* NavController */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_1_ionic_angular__["j" /* NavController */]) === "function" && _c || Object, typeof (_d = typeof __WEBPACK_IMPORTED_MODULE_1_ionic_angular__["c" /* App */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_1_ionic_angular__["c" /* App */]) === "function" && _d || Object, typeof (_e = typeof __WEBPACK_IMPORTED_MODULE_3__providers_pss_api_pss_api__["a" /* PssApiProvider */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_3__providers_pss_api_pss_api__["a" /* PssApiProvider */]) === "function" && _e || Object, typeof (_f = typeof __WEBPACK_IMPORTED_MODULE_1_ionic_angular__["l" /* Platform */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_1_ionic_angular__["l" /* Platform */]) === "function" && _f || Object, typeof (_g = typeof __WEBPACK_IMPORTED_MODULE_4_angular2_notifications__["NotificationsService"] !== "undefined" && __WEBPACK_IMPORTED_MODULE_4_angular2_notifications__["NotificationsService"]) === "function" && _g || Object])
    ], PssPageComponent);
    return PssPageComponent;
    var _a, _b, _c, _d, _e, _f, _g;
}());

//# sourceMappingURL=pss-page.js.map

/***/ }),

/***/ 719:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return SuccessSummary; });
var SuccessSummary = (function () {
    function SuccessSummary(title, firstLine, secondLine) {
        this.title = title;
        this.firstLine = firstLine;
        this.secondLine = secondLine;
        //title:string = null;
        //firstLine:string = null;
        //secondLine:string = null;
        this.summaryTable = [];
    }
    SuccessSummary.prototype.setSummaryTable = function (table) {
        this.summaryTable = table;
    };
    SuccessSummary.prototype.getSummaryTable = function () {
        return this.summaryTable;
    };
    SuccessSummary.prototype.getTitle = function () {
        return this.title;
    };
    SuccessSummary.prototype.getFirstLine = function () {
        return this.firstLine;
    };
    SuccessSummary.prototype.getSecondLine = function () {
        return this.secondLine;
    };
    return SuccessSummary;
}());

//# sourceMappingURL=success-summary.js.map

/***/ }),

/***/ 720:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return SuccessButton; });
var SuccessButton = (function () {
    function SuccessButton(title, targetPage, params, targetTabIndex) {
        this.title = title;
        this.targetPage = targetPage;
        this.params = params;
        this.targetTabIndex = targetTabIndex;
    }
    SuccessButton.prototype.getTitle = function () {
        return this.title;
    };
    SuccessButton.prototype.getTargetPage = function () {
        return this.targetPage;
    };
    SuccessButton.prototype.getTargetTabIndex = function () {
        return this.targetTabIndex;
    };
    SuccessButton.prototype.getParams = function () {
        return this.params;
    };
    return SuccessButton;
}());

//# sourceMappingURL=SuccessButton.js.map

/***/ }),

/***/ 723:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return LoginPage; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__(1);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__components_pss_page_pss_page__ = __webpack_require__(718);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__classes_success_summary__ = __webpack_require__(719);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3__classes_SuccessButton__ = __webpack_require__(720);
var __extends = (this && this.__extends) || (function () {
    var extendStatics = Object.setPrototypeOf ||
        ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
        function (d, b) { for (var p in b) if (b.hasOwnProperty(p)) d[p] = b[p]; };
    return function (d, b) {
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};




/**
 * Generated class for the LoginPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */
var LoginPage = (function (_super) {
    __extends(LoginPage, _super);
    function LoginPage() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.loginInfo = { 'username': null, 'password': null, 'player_id_for_event': null, 'player_pin': null };
        _this.loginType = 'player';
        return _this;
    }
    LoginPage.prototype.generateLoginUserProcessor = function (successButton) {
        var _this = this;
        return function (result) {
            if (result == null) {
                return;
            }
            console.log('in generateLoginUserProcessor');
            console.log(result);
            _this.eventAuth.setEventUserLoggedIn(_this.eventId, result.data);
            var name = null;
            if (result.data.full_user_name != null) {
                name = result.data.full_user_name;
            }
            if (result.data.player_full_name != null) {
                name = result.data.player_full_name;
            }
            var successSummary = new __WEBPACK_IMPORTED_MODULE_2__classes_success_summary__["a" /* SuccessSummary */](name + ' has logged in.', null, null);
            var targetPage = null;
            var targetTabIndex = null;
            if (_this.platform.is('mobile')) {
                console.log('going mobile');
                targetTabIndex = 0;
            }
            if (successButton == null) {
                targetPage = _this.getHomePageString();
                successButton = new __WEBPACK_IMPORTED_MODULE_3__classes_SuccessButton__["a" /* SuccessButton */]('Go Home', targetPage, _this.buildNavParams({}), targetTabIndex);
            }
            //            this.appCtrl.getRootNav().push("SuccessPage",
            _this.navCtrl.push("SuccessPage", _this.buildNavParams({ 'successSummary': successSummary,
                'successButtons': [successButton] }));
        };
    };
    LoginPage.prototype.loginUser = function () {
        this.pssApi.loginUser(this.loginInfo, this.eventId)
            .subscribe(this.generateLoginUserProcessor());
    };
    LoginPage.prototype.loginPlayer = function () {
        this.pssApi.loginPlayer(this.loginInfo, this.eventId)
            .subscribe(this.generateLoginUserProcessor());
    };
    LoginPage.prototype.loginEventOwner = function () {
        var targetTabIndex = null;
        if (this.platform.is('mobile')) {
            console.log('going mobile');
            targetTabIndex = 0;
        }
        var successButton = new __WEBPACK_IMPORTED_MODULE_3__classes_SuccessButton__["a" /* SuccessButton */]('Go Home', 'EventOwnerHomePage', this.buildNavParams({}), targetTabIndex);
        this.pssApi.loginEventOwner(this.loginInfo)
            .subscribe(this.generateLoginUserProcessor(successButton));
    };
    LoginPage.prototype.ionViewWillLoad = function () {
        console.log('ionViewDidLoad LoginPage');
        //this.eventAuth.setEventRole(1,{'roleName':'deskworker'});      
    };
    LoginPage = __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["Component"])({
            selector: 'page-login',template:/*ion-inline-start:"/Users/agoldma/git/github/TD/front_v2/src/pages/login/login.html"*/'<!--\n    Generated template for the LoginPage page.\n\n    See http://ionicframework.com/docs/components/#navigation for more info on\n    Ionic pages and navigation.\n  -->\n\n<ion-header>\n  <ion-navbar>\n    <ion-title>\n      Login\n    </ion-title>\n  </ion-navbar>\n</ion-header>\n<ion-content padding>\n  <div>\n  <ion-segment [(ngModel)]="loginType">\n    <ion-segment-button value="player">\n      <ion-icon item-start name="person"></ion-icon> Tournament Player\n    </ion-segment-button>\n    <ion-segment-button value="official">\n            <ion-icon item-start name="clipboard"></ion-icon> Tournament Official\n    </ion-segment-button>\n  </ion-segment>\n  </div>\n  <ng-container [ngSwitch]="loginType">\n    <form #loginForm="ngForm" *ngSwitchCase="\'official\'">\n      <ion-item>\n        <ion-label floating>Username</ion-label>\n        <ion-input type="text" required\n                   [(ngModel)]="loginInfo.username" name="username"></ion-input>\n      </ion-item>\n      <ion-item>\n        <ion-label floating>Password</ion-label>\n        <ion-input type="text" required\n                   [(ngModel)]="loginInfo.password" name="password"></ion-input>\n      </ion-item>\n      <ion-item no-lines>\n        <button [disabled]=\'!loginForm.valid\' ion-button default (click)="loginUser()">Login </button>\n      </ion-item>\n    </form>\n    <form #playerLoginForm="ngForm" *ngSwitchCase="\'player\'">\n      <ion-item>\n        <ion-label floating>Player Number</ion-label>\n        <ion-input type="number" required\n                   [(ngModel)]="loginInfo.player_id_for_event" name="player_id_for_event"></ion-input>\n      </ion-item>\n      <ion-item>\n        <ion-label floating>Pin</ion-label>\n        <ion-input type="text" required\n                   [(ngModel)]="loginInfo.player_pin" name="player_pin"></ion-input>\n      </ion-item>\n      <ion-item no-lines>\n        <button [disabled]=\'!playerLoginForm.valid\' ion-button default (click)="loginPlayer()">Login </button>\n      </ion-item>\n    </form>\n    \n  </ng-container>\n<!--  <ng-container *ngIf=\'loginType=="player"\'>\n  </ng-container>-->\n  \n</ion-content>\n'/*ion-inline-end:"/Users/agoldma/git/github/TD/front_v2/src/pages/login/login.html"*/,
        })
    ], LoginPage);
    return LoginPage;
}(__WEBPACK_IMPORTED_MODULE_1__components_pss_page_pss_page__["a" /* PssPageComponent */]));

//# sourceMappingURL=login.js.map

/***/ }),

/***/ 731:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return EventOwnerLoginPage; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__(1);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__login_login__ = __webpack_require__(723);
var __extends = (this && this.__extends) || (function () {
    var extendStatics = Object.setPrototypeOf ||
        ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
        function (d, b) { for (var p in b) if (b.hasOwnProperty(p)) d[p] = b[p]; };
    return function (d, b) {
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};


/**
 * Generated class for the EventOwnerLoginPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */
var EventOwnerLoginPage = (function (_super) {
    __extends(EventOwnerLoginPage, _super);
    function EventOwnerLoginPage() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    EventOwnerLoginPage.prototype.ionViewDidLoad = function () {
        console.log('ionViewDidLoad EventOwnerLoginPage');
    };
    EventOwnerLoginPage = __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["Component"])({
            selector: 'page-event-owner-login',template:/*ion-inline-start:"/Users/agoldma/git/github/TD/front_v2/src/pages/event-owner-login/event-owner-login.html"*/'<!--\n  Generated template for the EventOwnerLoginPage page.\n\n  See http://ionicframework.com/docs/components/#navigation for more info on\n  Ionic pages and navigation.\n-->\n<!--\n  Generated template for the LoginPage page.\n\n  See http://ionicframework.com/docs/components/#navigation for more info on\n  Ionic pages and navigation.\n-->\n\n<ion-header>\n  <ion-navbar>\n    <ion-title>\n      Login\n    </ion-title>\n  </ion-navbar>\n</ion-header>\n<ion-content padding>\n<form #loginForm="ngForm">\n  <ion-item>\n  <ion-label floating>Username</ion-label>\n  <ion-input type="text" required\n         [(ngModel)]="loginInfo.username" name="username"></ion-input>\n</ion-item>\n<ion-item>\n  <ion-label floating>Password</ion-label>\n  <ion-input type="text" required\n         [(ngModel)]="loginInfo.password" name="password"></ion-input>\n</ion-item>\n<ion-item no-lines>\n  <button [disabled]=\'!loginForm.valid\' ion-button default (click)="loginEventOwner()">Login </button>\n</ion-item>\n</form>\n\n<ion-item no-lines text-center>\n  OR\n</ion-item>\n<ion-item no-lines text-center>\n  If you want to create an account, follow <a href="/#/event-owner-request">this link.</a>\n</ion-item>\n\n\n</ion-content>\n'/*ion-inline-end:"/Users/agoldma/git/github/TD/front_v2/src/pages/event-owner-login/event-owner-login.html"*/,
        })
    ], EventOwnerLoginPage);
    return EventOwnerLoginPage;
}(__WEBPACK_IMPORTED_MODULE_1__login_login__["a" /* LoginPage */]));

//# sourceMappingURL=event-owner-login.js.map

/***/ })

});
//# sourceMappingURL=2.js.map