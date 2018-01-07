webpackJsonp([12],{

/***/ 715:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
Object.defineProperty(__webpack_exports__, "__esModule", { value: true });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "TournamentDirectorHomePageModule", function() { return TournamentDirectorHomePageModule; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__(1);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1_ionic_angular__ = __webpack_require__(40);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__tournament_director_home__ = __webpack_require__(744);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3_angular2_notifications__ = __webpack_require__(356);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3_angular2_notifications___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_3_angular2_notifications__);
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};




var TournamentDirectorHomePageModule = (function () {
    function TournamentDirectorHomePageModule() {
    }
    TournamentDirectorHomePageModule = __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["NgModule"])({
            declarations: [
                __WEBPACK_IMPORTED_MODULE_2__tournament_director_home__["a" /* TournamentDirectorHomePage */],
            ],
            imports: [
                __WEBPACK_IMPORTED_MODULE_1_ionic_angular__["g" /* IonicPageModule */].forChild(__WEBPACK_IMPORTED_MODULE_2__tournament_director_home__["a" /* TournamentDirectorHomePage */]),
                __WEBPACK_IMPORTED_MODULE_3_angular2_notifications__["SimpleNotificationsModule"].forRoot()
            ],
        })
    ], TournamentDirectorHomePageModule);
    return TournamentDirectorHomePageModule;
}());

//# sourceMappingURL=tournament-director-home.module.js.map

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
        __metadata("design:paramtypes", [__WEBPACK_IMPORTED_MODULE_2__providers_event_auth_event_auth__["a" /* EventAuthProvider */],
            __WEBPACK_IMPORTED_MODULE_1_ionic_angular__["k" /* NavParams */],
            __WEBPACK_IMPORTED_MODULE_1_ionic_angular__["j" /* NavController */],
            __WEBPACK_IMPORTED_MODULE_1_ionic_angular__["c" /* App */],
            __WEBPACK_IMPORTED_MODULE_3__providers_pss_api_pss_api__["a" /* PssApiProvider */],
            __WEBPACK_IMPORTED_MODULE_1_ionic_angular__["l" /* Platform */],
            __WEBPACK_IMPORTED_MODULE_4_angular2_notifications__["NotificationsService"]])
    ], PssPageComponent);
    return PssPageComponent;
}());

//# sourceMappingURL=pss-page.js.map

/***/ }),

/***/ 744:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return TournamentDirectorHomePage; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__(1);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__components_pss_page_pss_page__ = __webpack_require__(718);
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
 * Generated class for the TournamentDirectorHomePage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */
var TournamentDirectorHomePage = (function (_super) {
    __extends(TournamentDirectorHomePage, _super);
    function TournamentDirectorHomePage() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.tournaments = [];
        return _this;
    }
    TournamentDirectorHomePage.prototype.generateGetAllTournamentsProcessor = function () {
        var _this = this;
        return function (result) {
            if (result == null) {
                return;
            }
            _this.tournaments = result.data;
            _this.tournaments.map(function (tournament) {
                tournament.expanded = false;
            });
        };
    };
    TournamentDirectorHomePage.prototype.ionViewDidLoad = function () {
        this.pssApi.getAllTournaments(this.eventId)
            .subscribe(this.generateGetAllTournamentsProcessor());
        console.log('ionViewDidLoad TournamentDirectorHomePage');
    };
    TournamentDirectorHomePage = __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["Component"])({
            selector: 'page-tournament-director-home',template:/*ion-inline-start:"/Users/agoldma/git/github/TD/front_v2/src/pages/tournament-director-home/tournament-director-home.html"*/'<!--\n  Generated template for the TournamentDirectorHomePage page.\n\n  See http://ionicframework.com/docs/components/#navigation for more info on\n  Ionic pages and navigation.\n  -->\n<!--<bobo>-->\n<ion-header>\n<ion-navbar hideBackButton>  \n    <ion-title showWhen=\'mobile\'>\n      {{title}}\n    </ion-title>    \n  <ion-title hideWhen=\'mobile\'>Pss</ion-title>\n  <ion-buttons end>\n<!--    <button icon-only menuToggle ion-button>Queues</button>-->\n  </ion-buttons>\n</ion-navbar>\n<ion-navbar color="primary">\nExample of sub header\n</ion-navbar>\n\n</ion-header>\n<!--</bobo>-->\n<simple-notifications  [options]="{position:[\'top\',\'right\']}"></simple-notifications>\n\n\n<ion-content padding>\n  <h1><b>Purchase Tickets</b></h1>\n  <ion-list>\n    <ion-item no-lines [navPush]="\'TicketPurchasePage\'" [navParams]="buildNavParams({})">\n      <ion-icon item-start name="ios-cash-outline"></ion-icon> Ticket Purchase\n    </ion-item>\n  </ion-list>\n\n  <h1><b>Add Players</b></h1>\n  <ion-list>\n    <ion-item no-lines [navPush]="\'AddPlayerPage\'" [navParams]="buildNavParams({})">\n      <ion-icon item-start name="ios-add-circle-outline"></ion-icon> Add Player\n    </ion-item>\n  </ion-list>\n  \n  <h1><b>Tournament Creation</b></h1>\n  <ion-list>\n    <ion-item no-lines [navPush]="\'TournamentPage\'" [navParams]="buildNavParams({actionType:\'create\',\'wizardMode\':true})">\n      <ion-icon item-start name="ios-add-circle-outline"></ion-icon> Create Tournament \n\n      <!--<button item-start ion-button [navPush]="\'CreateEventPage\'" [navParams]="buildNavParams({actionType:\'create\',\'wizardMode\':true})" >Create Event</button>-->\n    </ion-item>\n  </ion-list>\n\n  <!--  <button ion-button [navPush]="\'CreateTournamentPage\'" [navParams]="{entityType:\'tournament\',actionType:\'create\',targetEventId:1,eventName:\'poop\'}" >Create Tournament</button> -->\n  <h1><b>Tournaments</b></h1>\n  <ion-list>\n    <ng-container *ngFor="let tournament of tournaments">\n      <ion-item-divider (click)="expand(tournament)">\n        <ion-avatar item-start *ngIf="tournament.img_url!=null">\n          <img [src]="tournament.img_url">\n        </ion-avatar>        \n        <h1>{{tournament.tournament_name}}</h1><ion-icon item-end [name]="tournament.expanded==false?\'ios-arrow-dropdown\':\'ios-arrow-dropup\'"></ion-icon>\n      </ion-item-divider>      \n      <ng-container *ngIf="tournament.expanded!=true?false:true">\n        <ion-item>\n          <button ion-button [navPush]="\'TournamentMachinesPage\'" [navParams]="buildNavParams({tournamentId:tournament.tournament_id, eventId:tournament.event_id})">Add Machines To Tournament</button>\n          <br>\n            <button [navPush]="\'EditTournamentPage\'" [navParams]="buildNavParams({tournamentId:tournament.tournament_id, eventId:tournament.event_id, actionType:\'edit\'})" ion-button >Edit Tournament</button>\n          <br>\n          <button ion-button (click)="onTournamentToggle(eventId,tournament)"><ion-icon item-start [name]="tournament.active?\'play\':\'pause\'"></ion-icon>Toggle Tournament</button>\n        </ion-item>\n      </ng-container>      \n    </ng-container>\n  </ion-list>\n</ion-content>\n\n\n'/*ion-inline-end:"/Users/agoldma/git/github/TD/front_v2/src/pages/tournament-director-home/tournament-director-home.html"*/,
        })
    ], TournamentDirectorHomePage);
    return TournamentDirectorHomePage;
}(__WEBPACK_IMPORTED_MODULE_1__components_pss_page_pss_page__["a" /* PssPageComponent */]));

//# sourceMappingURL=tournament-director-home.js.map

/***/ })

});
//# sourceMappingURL=12.js.map