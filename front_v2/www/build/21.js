webpackJsonp([21],{

/***/ 697:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
Object.defineProperty(__webpack_exports__, "__esModule", { value: true });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "AddUserPageModule", function() { return AddUserPageModule; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__(1);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1_ionic_angular__ = __webpack_require__(40);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__add_user__ = __webpack_require__(725);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3_ionic2_auto_complete__ = __webpack_require__(358);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_4_angular2_notifications__ = __webpack_require__(356);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_4_angular2_notifications___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_4_angular2_notifications__);
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};





var AddUserPageModule = (function () {
    function AddUserPageModule() {
    }
    AddUserPageModule = __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["NgModule"])({
            declarations: [
                __WEBPACK_IMPORTED_MODULE_2__add_user__["a" /* AddUserPage */],
            ],
            imports: [
                __WEBPACK_IMPORTED_MODULE_1_ionic_angular__["g" /* IonicPageModule */].forChild(__WEBPACK_IMPORTED_MODULE_2__add_user__["a" /* AddUserPage */]),
                __WEBPACK_IMPORTED_MODULE_3_ionic2_auto_complete__["a" /* AutoCompleteModule */],
                __WEBPACK_IMPORTED_MODULE_4_angular2_notifications__["SimpleNotificationsModule"].forRoot()
            ],
        })
    ], AddUserPageModule);
    return AddUserPageModule;
}());

//# sourceMappingURL=add-user.module.js.map

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

/***/ 725:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return AddUserPage; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__(1);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__components_pss_page_pss_page__ = __webpack_require__(718);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__providers_auto_complete_auto_complete__ = __webpack_require__(357);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3_ionic_angular__ = __webpack_require__(40);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_4__providers_event_auth_event_auth__ = __webpack_require__(155);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_5__providers_pss_api_pss_api__ = __webpack_require__(154);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_6_angular2_notifications__ = __webpack_require__(356);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_6_angular2_notifications___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_6_angular2_notifications__);
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
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};








/**
 * Generated class for the AddUserPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */
var AddUserPage = (function (_super) {
    __extends(AddUserPage, _super);
    function AddUserPage(autoCompleteProvider, eventAuth, navParams, navCtrl, appCtrl, pssApi, platform, actionSheetCtrl, notificationsService) {
        var _this = _super.call(this, eventAuth, navParams, navCtrl, appCtrl, pssApi, platform, notificationsService) || this;
        _this.autoCompleteProvider = autoCompleteProvider;
        _this.eventAuth = eventAuth;
        _this.navParams = navParams;
        _this.navCtrl = navCtrl;
        _this.appCtrl = appCtrl;
        _this.pssApi = pssApi;
        _this.platform = platform;
        _this.actionSheetCtrl = actionSheetCtrl;
        _this.notificationsService = notificationsService;
        _this.existingUserFound = true;
        _this.selectedUser = {};
        _this.newUserName = null;
        _this.roles = [];
        _this.selectedRole = null;
        return _this;
    }
    AddUserPage.prototype.generateGetAllUsersProcessor = function () {
        var _this = this;
        return function (result) {
            if (result == null) {
                return;
            }
            _this.users = result.data;
            _this.autoCompleteProvider.setUsers(result.data);
            _this.roles = result.roles;
        };
    };
    AddUserPage.prototype.generateAddEventUsersProcessor = function (user_full_name, role_name) {
        var _this = this;
        return function (result) {
            if (result == null) {
                return;
            }
            var user_already_exists = _this.users.filter(function (user) {
                return user.pss_user_id == result.data.pss_user_id;
            }).length;
            if (user_already_exists == 0) {
                _this.users.push(result.data[0]);
            }
            var message_string = user_full_name + " is a " + role_name + " in the event.";
            _this.notificationsService.success("Success", message_string, {
                timeOut: 0,
                position: ["top", "right"],
                theClass: 'poop'
            });
            //toast here
        };
    };
    AddUserPage.prototype.ionViewWillLoad = function () {
        console.log('ionViewDidLoad EventOwnerAddUserPage');
        this.pssApi.getAllUsers()
            .subscribe(this.generateGetAllUsersProcessor());
    };
    AddUserPage.prototype.onInput = function (event) {
        if (this.searchbar.suggestions.length == 0) {
            this.existingUserFound = false;
            this.newUserName = event;
        }
        else {
            this.existingUserFound = true;
        }
        console.log(this.selectedUser);
    };
    AddUserPage.prototype.doesEventRolesMatchEvent = function (eventId, roles) {
        return roles.filter(function (role) { return Number(eventId) == role.event_id; }).length > 0;
    };
    AddUserPage.prototype.onSelect = function (event) {
        console.log('in onselect...');
        console.log(this.eventId);
        if (this.doesEventRolesMatchEvent(this.eventId, this.selectedUser.event_roles)) {
            this.existingUserFound = true;
            var message_string = this.selectedUser.full_user_name + " is already registered for this event.";
            this.notificationsService.warn("Warning", message_string, {
                timeOut: 0,
                position: ["top", "right"],
                theClass: 'poop'
            });
            return;
        }
        //FIXME : need to add new user to list of users searched
        if (!this.doesEventRolesMatchEvent(this.eventId, this.selectedUser.event_roles)) {
            this.existingUserFound = true;
            this.pssApi.addEventUsers({ event_users: [this.selectedUser],
                event_role_ids: [this.selectedRole.event_role_id] }, this.eventId)
                .subscribe(this.generateAddEventUsersProcessor(this.selectedUser.full_user_name, this.selectedRole.event_role_name));
            return;
        }
        this.existingUserFound = true;
    };
    AddUserPage.prototype.onFocus = function () {
        this.selectedUser = {};
        this.existingUserFound = true;
    };
    AddUserPage.prototype.onSubmit = function (name_string) {
        this.existingUserFound = true;
        this.pssApi.addEventUsers({ event_users: [this.parseOutFirstLastNames(name_string)], event_role_ids: [this.selectedRole.event_role_id] }, this.eventId)
            .subscribe(this.generateAddEventUsersProcessor(name_string, this.selectedRole.event_role_name));
    };
    AddUserPage.prototype.parseOutFirstLastNames = function (name_string) {
        var name_elements = name_string.split(" ");
        return {
            first_name: name_elements[0],
            last_name: name_elements[1],
            username: name_elements[0] + name_elements[1]
        };
    };
    __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["ViewChild"])('searchbar'),
        __metadata("design:type", Object)
    ], AddUserPage.prototype, "searchbar", void 0);
    __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["ViewChild"])('myForm'),
        __metadata("design:type", Object)
    ], AddUserPage.prototype, "myForm", void 0);
    AddUserPage = __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["Component"])({
            selector: 'page-add-user',template:/*ion-inline-start:"/Users/agoldma/git/github/TD/front_v2/src/components/add-user/add-user.html"*/'<ion-header>\n  <ion-navbar>\n    <ion-title></ion-title>\n    <ion-buttons end hideWhen="mobile">\n      <button icon-only ion-button [navPush]="\'EventSelectPage\'">Switch Events</button>    \n      <button icon-only ion-button [navPush]="destPageAfterSuccess" [navParams]=\'buildNavParams({})\'>Home</button>    \n    </ion-buttons>\n  </ion-navbar>\n</ion-header>\n<simple-notifications  [options]="{position:[\'top\',\'right\']}"></simple-notifications>\n<ion-content padding>\n  <form #myForm="ngForm">\n    <ion-item>\n    <ion-label>Role</ion-label>\n    <ion-select name="myeventrole" [(ngModel)]="selectedRole" required>\n      <ion-option *ngFor="let role of roles" [value]="role">{{role.event_role_name}}</ion-option>\n    </ion-select>\n    </ion-item>\n    <ion-item>\n    </ion-item>\n    <ion-auto-complete name="myautocomplete" [(ngModel)]="selectedUser" (ionAutoInput)="onInput($event)" (autoFocus)="onFocus()" (itemSelected)="onSelect($event)" #searchbar [dataProvider]="autoCompleteProvider"></ion-auto-complete>\n  </form>\n\n  <div *ngIf=\'existingUserFound==false\' text-center padding>        \n    The system does not know about {{newUserName}}.  Click the button below to register them for the event.\n    <br>\n    <button [disabled]=\'!myForm.valid\' ion-button margin (click)="onSubmit(newUserName)">Register User</button>\n    \n  </div>\n  \n</ion-content>\n'/*ion-inline-end:"/Users/agoldma/git/github/TD/front_v2/src/components/add-user/add-user.html"*/,
        }),
        __metadata("design:paramtypes", [__WEBPACK_IMPORTED_MODULE_2__providers_auto_complete_auto_complete__["a" /* AutoCompleteProvider */],
            __WEBPACK_IMPORTED_MODULE_4__providers_event_auth_event_auth__["a" /* EventAuthProvider */],
            __WEBPACK_IMPORTED_MODULE_3_ionic_angular__["k" /* NavParams */],
            __WEBPACK_IMPORTED_MODULE_3_ionic_angular__["j" /* NavController */],
            __WEBPACK_IMPORTED_MODULE_3_ionic_angular__["c" /* App */],
            __WEBPACK_IMPORTED_MODULE_5__providers_pss_api_pss_api__["a" /* PssApiProvider */],
            __WEBPACK_IMPORTED_MODULE_3_ionic_angular__["l" /* Platform */],
            __WEBPACK_IMPORTED_MODULE_3_ionic_angular__["a" /* ActionSheetController */],
            __WEBPACK_IMPORTED_MODULE_6_angular2_notifications__["NotificationsService"]])
    ], AddUserPage);
    return AddUserPage;
}(__WEBPACK_IMPORTED_MODULE_1__components_pss_page_pss_page__["a" /* PssPageComponent */]));

//# sourceMappingURL=add-user.js.map

/***/ })

});
//# sourceMappingURL=21.js.map