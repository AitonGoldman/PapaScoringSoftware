webpackJsonp([14],{

/***/ 685:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
Object.defineProperty(__webpack_exports__, "__esModule", { value: true });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "EventOwnerHomePageModule", function() { return EventOwnerHomePageModule; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__(1);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1_ionic_angular__ = __webpack_require__(43);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__event_owner_home__ = __webpack_require__(709);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3__components_expandable_expandable_module__ = __webpack_require__(351);
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};




var EventOwnerHomePageModule = (function () {
    function EventOwnerHomePageModule() {
    }
    EventOwnerHomePageModule = __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["NgModule"])({
            declarations: [
                __WEBPACK_IMPORTED_MODULE_2__event_owner_home__["a" /* EventOwnerHomePage */]
            ],
            imports: [
                __WEBPACK_IMPORTED_MODULE_1_ionic_angular__["f" /* IonicPageModule */].forChild(__WEBPACK_IMPORTED_MODULE_2__event_owner_home__["a" /* EventOwnerHomePage */]),
                __WEBPACK_IMPORTED_MODULE_3__components_expandable_expandable_module__["a" /* ExpandableModule */]
            ],
        })
    ], EventOwnerHomePageModule);
    return EventOwnerHomePageModule;
}());

//# sourceMappingURL=event-owner-home.module.js.map

/***/ }),

/***/ 698:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return PssPageComponent; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__(1);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1_ionic_angular__ = __webpack_require__(43);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__providers_event_auth_event_auth__ = __webpack_require__(151);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3__providers_pss_api_pss_api__ = __webpack_require__(347);
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
    function PssPageComponent(eventAuth, navParams, navCtrl, appCtrl, pssApi, platform) {
        this.eventAuth = eventAuth;
        this.navParams = navParams;
        this.navCtrl = navCtrl;
        this.appCtrl = appCtrl;
        this.pssApi = pssApi;
        this.platform = platform;
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
    PssPageComponent.prototype.getHomePageString = function () {
        var role = this.eventAuth.getRoleName(this.eventId);
        if (role == "tournamentdirector") {
            return 'TournamentDirectorHomePage';
        }
        //if(role=="eventowner"){
        //        return 'EventOwnerHomePage'            
        //}        
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
    PssPageComponent = __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["Component"])({
            selector: 'pss-page',template:/*ion-inline-start:"/Users/agoldma/git/github/TD/front_v2/src/components/pss-page/pss-page.html"*/'<!-- Generated template for the TopNavComponent component -->\n<div>\n  {{text}}\n</div>\n'/*ion-inline-end:"/Users/agoldma/git/github/TD/front_v2/src/components/pss-page/pss-page.html"*/
        }),
        __metadata("design:paramtypes", [typeof (_a = typeof __WEBPACK_IMPORTED_MODULE_2__providers_event_auth_event_auth__["a" /* EventAuthProvider */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_2__providers_event_auth_event_auth__["a" /* EventAuthProvider */]) === "function" && _a || Object, typeof (_b = typeof __WEBPACK_IMPORTED_MODULE_1_ionic_angular__["j" /* NavParams */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_1_ionic_angular__["j" /* NavParams */]) === "function" && _b || Object, typeof (_c = typeof __WEBPACK_IMPORTED_MODULE_1_ionic_angular__["i" /* NavController */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_1_ionic_angular__["i" /* NavController */]) === "function" && _c || Object, typeof (_d = typeof __WEBPACK_IMPORTED_MODULE_1_ionic_angular__["b" /* App */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_1_ionic_angular__["b" /* App */]) === "function" && _d || Object, typeof (_e = typeof __WEBPACK_IMPORTED_MODULE_3__providers_pss_api_pss_api__["a" /* PssApiProvider */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_3__providers_pss_api_pss_api__["a" /* PssApiProvider */]) === "function" && _e || Object, typeof (_f = typeof __WEBPACK_IMPORTED_MODULE_1_ionic_angular__["k" /* Platform */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_1_ionic_angular__["k" /* Platform */]) === "function" && _f || Object])
    ], PssPageComponent);
    return PssPageComponent;
    var _a, _b, _c, _d, _e, _f;
}());

//# sourceMappingURL=pss-page.js.map

/***/ }),

/***/ 709:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return EventOwnerHomePage; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__(1);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__components_pss_page_pss_page__ = __webpack_require__(698);
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
 * Generated class for the EventOwnerHomePage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */
var EventOwnerHomePage = (function (_super) {
    __extends(EventOwnerHomePage, _super);
    function EventOwnerHomePage() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.itemExpandHeight = 100;
        return _this;
    }
    EventOwnerHomePage.prototype.expand = function (item) {
        item.expanded = item.expanded == false ? true : false;
    };
    EventOwnerHomePage.prototype.generateGetAllEventsAndTournamentsProcessor = function () {
        var _this = this;
        return function (result) {
            if (result == null) {
                return;
            }
            console.log('got back tournaments and events...');
            _this.eventsAndTournaments = result.data;
            _this.eventsAndTournaments.map(function (event) {
                event.expanded = false;
                event.tournaments.map(function (tournament) {
                    tournament.expanded = false;
                });
            });
            console.log(_this.eventsAndTournaments);
        };
    };
    EventOwnerHomePage.prototype.ionViewWillLoad = function () {
        this.pssApi.getAllEventsAndTournaments()
            .subscribe(this.generateGetAllEventsAndTournamentsProcessor());
        console.log('ionViewDidLoad EventOwnerHomePage');
    };
    EventOwnerHomePage = __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["Component"])({
            selector: 'page-event-owner-home',template:/*ion-inline-start:"/Users/agoldma/git/github/TD/front_v2/src/pages/event-owner-home/event-owner-home.html"*/'<!--\n    Generated template for the EventOwnerHomePage page.\n\n    See http://ionicframework.com/docs/components/#navigation for more info on\n    Ionic pages and navigation.\n  -->\n<ion-header>\n\n  <ion-navbar>\n    <ion-title>EventOwnerHomePage</ion-title>\n    <ion-buttons end >\n      <button icon-only ion-button [navPush]="\'EventSelectPage\'">Switch Events</button>    \n    </ion-buttons>\n  </ion-navbar>\n\n</ion-header>\n\n\n<ion-content padding>\n  <h1><b>Event Creation</b></h1>\n  <ion-list>\n    <ion-item no-lines [navPush]="\'CreateEventPage\'" [navParams]="buildNavParams({actionType:\'create\',\'wizardMode\':true})">\n      <ion-icon item-start name="ios-add-circle-outline"></ion-icon> Create Event \n\n      <!--<button item-start ion-button [navPush]="\'CreateEventPage\'" [navParams]="buildNavParams({actionType:\'create\',\'wizardMode\':true})" >Create Event</button>-->\n    </ion-item>\n  </ion-list>\n\n  <!--  <button ion-button [navPush]="\'CreateTournamentPage\'" [navParams]="{entityType:\'tournament\',actionType:\'create\',targetEventId:1,eventName:\'poop\'}" >Create Tournament</button> -->\n  <h1><b>Your Events</b></h1>\n  <ion-list>\n    <ng-container *ngFor="let event of eventsAndTournaments">\n      <ion-item-divider (click)="expand(event)">\n        <h1>{{event.name}}</h1><ion-icon item-end [name]="event.expanded==false?\'ios-arrow-dropdown\':\'ios-arrow-dropup\'"></ion-icon>\n      </ion-item-divider>\n      <!--    <ion-item>\n              <ion-icon item-start></ion-icon>\n              <button item-end ion-button [navPush]="\'EventOwnerCreateTournamentPage\'" [navParams]="{entityType:\'tournament\',actionType:\'create\'}" >Create Tournament</button>\n              <b>Tournaments</b>\n      </ion-item>-->\n      <ion-item no-lines *ngIf="event.expanded" [navPush]="\'EventOwnerCreateTournamentPage\'" [navParams]="{entityType:\'tournament\',actionType:\'create\'}">\n        <ion-icon item-start name="ios-add-circle-outline"></ion-icon> Create Tournament \n\n<!--        <button item-start ion-button [navPush]="\'EventOwnerCreateTournamentPage\'" [navParams]="{entityType:\'tournament\',actionType:\'create\'}" >Create Tournament</button>-->\n      </ion-item>\n      \n      <ng-container *ngFor="let tournament of event.tournaments">\n        <ion-item (click)="expand(tournament)" *ngIf="event.expanded">      \n          {{tournament.tournament_name}}<ion-icon item-end [name]="tournament.expanded==false?\'ios-arrow-dropdown\':\'ios-arrow-dropup\'"></ion-icon>\n        </ion-item>\n        <ng-container *ngIf="tournament.expanded!=true?false:true">\n          <ion-item>\n            <button ion-button [navPush]="\'EventOwnerTournamentMachinesPage\'" [navParams]="buildNavParams({tournamentId:tournament.tournament_id, eventId:event.event_id})">Add Machines To Tournament</button>\n            <br>\n            <button ion-button >Edit Tournament</button>\n            <br>\n            <button ion-button ><ion-icon item-start [name]="tournament.active?\'play\':\'pause\'"></ion-icon>Toggle Tournament</button>\n          </ion-item>\n        </ng-container>\n      </ng-container>\n    </ng-container>\n  </ion-list>\n</ion-content>\n'/*ion-inline-end:"/Users/agoldma/git/github/TD/front_v2/src/pages/event-owner-home/event-owner-home.html"*/,
        })
    ], EventOwnerHomePage);
    return EventOwnerHomePage;
}(__WEBPACK_IMPORTED_MODULE_1__components_pss_page_pss_page__["a" /* PssPageComponent */]));

//# sourceMappingURL=event-owner-home.js.map

/***/ })

});
//# sourceMappingURL=14.js.map