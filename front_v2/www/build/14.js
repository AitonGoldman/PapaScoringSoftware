webpackJsonp([14],{

/***/ 712:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
Object.defineProperty(__webpack_exports__, "__esModule", { value: true });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "SuccessPageModule", function() { return SuccessPageModule; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__(1);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1_ionic_angular__ = __webpack_require__(40);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__success__ = __webpack_require__(741);
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};



var SuccessPageModule = (function () {
    function SuccessPageModule() {
    }
    SuccessPageModule = __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["NgModule"])({
            declarations: [
                __WEBPACK_IMPORTED_MODULE_2__success__["a" /* SuccessPage */]
            ],
            imports: [
                __WEBPACK_IMPORTED_MODULE_1_ionic_angular__["g" /* IonicPageModule */].forChild(__WEBPACK_IMPORTED_MODULE_2__success__["a" /* SuccessPage */]),
            ],
        })
    ], SuccessPageModule);
    return SuccessPageModule;
}());

//# sourceMappingURL=success.module.js.map

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

/***/ 741:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return SuccessPage; });
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
 * Generated class for the SuccessPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */
var SuccessPage = (function (_super) {
    __extends(SuccessPage, _super);
    function SuccessPage() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.successSummary = null;
        _this.successButtons = null;
        return _this;
    }
    // pushPageWithNoBackButton(pageName,navParams){        
    //     this.navCtrl.getActive().willLeave.subscribe(
    //         ()=>{
    //             this.navCtrl.last().showBackButton(false);
    //         }
    //     )        
    //     this.navCtrl.push(pageName,this.buildNavParams(navParams));
    // }
    SuccessPage.prototype.ionViewWillLoad = function () {
        this.successSummary = this.navParams.get('successSummary');
        this.successButtons = this.navParams.get('successButtons');
        console.log('ionViewDidLoad SuccessPage');
    };
    SuccessPage = __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["Component"])({
            selector: 'page-success',template:/*ion-inline-start:"/Users/agoldma/git/github/TD/front_v2/src/pages/success/success.html"*/'<!--\n  Generated template for the SuccessPage page.\n\n  See http://ionicframework.com/docs/components/#navigation for more info on\n  Ionic pages and navigation.\n-->\n<ion-header>\n  <ion-navbar hideBackButton="true">\n    <ion-title>Success</ion-title>\n  </ion-navbar>\n</ion-header>\n\n<ion-content padding>\n  <ion-grid>\n  <ion-row>\n    <ion-col>      \n    </ion-col>\n    <ion-col style=\'text-align:center\'> \n      <ion-icon *ngIf="successSummary" style="zoom:4.0;" name="thumbs-up"></ion-icon>\n      <ion-icon *ngIf="successSummary == undefined" style="zoom:4.0;" name="thumbs-down"></ion-icon>\n\n    </ion-col>\n    <ion-col>     \n    </ion-col>\n  </ion-row>\n  <ion-row>\n    <ion-col style=\'text-align:center\'>         \n      {{successSummary ? successSummary.getTitle():\'You can not reload this page\'}}\n      <hr style=\'width:75%\'>      \n    </ion-col>\n  </ion-row>\n\n  <ng-container *ngIf="successSummary.summaryTable.length>0">      \n    <ion-row *ngFor="let summaryTableRow of successSummary.summaryTable">\n      <ion-col style=\'text-align:center\'>         \n        {{summaryTableRow}}\n      </ion-col>                     \n    </ion-row>\n    <hr style=\'width:75%\' text-center>\n  </ng-container>\n\n  <ion-row>\n    <ion-col style=\'text-align:center\'>         \n      {{successSummary ? successSummary.getFirstLine():\'\'}}\n    </ion-col>               \n  </ion-row>\n  <ion-row>\n    <ion-col style=\'text-align:center\'>         \n      {{successSummary ? successSummary.getSecondLine():\'\'}}\n    </ion-col>               \n  </ion-row>\n  <ion-row>\n    <ion-col *ngFor="let button of successButtons" style=\'text-align:center\'>\n      <!--<button ion-button [navPush]="button.getTargetPage()" [navParams]="buildNavParams(button.getParams())">{{button.getTitle()}}</button>-->\n      <button ion-button (click)="pushPageWithNoBackButton(button.getTargetPage(),button.getParams(),button.getTargetTabIndex())">{{button.getTitle()}}</button>\n    </ion-col>\n  </ion-row>\n  </ion-grid>\n  \n</ion-content>\n'/*ion-inline-end:"/Users/agoldma/git/github/TD/front_v2/src/pages/success/success.html"*/,
        })
    ], SuccessPage);
    return SuccessPage;
}(__WEBPACK_IMPORTED_MODULE_1__components_pss_page_pss_page__["a" /* PssPageComponent */]));

//# sourceMappingURL=success.js.map

/***/ })

});
//# sourceMappingURL=14.js.map