webpackJsonp([11],{

/***/ 685:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
Object.defineProperty(__webpack_exports__, "__esModule", { value: true });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "QuickLinksPageModule", function() { return QuickLinksPageModule; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__(1);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1_ionic_angular__ = __webpack_require__(44);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__quick_links__ = __webpack_require__(706);
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};



var QuickLinksPageModule = (function () {
    function QuickLinksPageModule() {
    }
    QuickLinksPageModule = __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["I" /* NgModule */])({
            declarations: [
                __WEBPACK_IMPORTED_MODULE_2__quick_links__["a" /* QuickLinksPage */],
            ],
            imports: [
                __WEBPACK_IMPORTED_MODULE_1_ionic_angular__["f" /* IonicPageModule */].forChild(__WEBPACK_IMPORTED_MODULE_2__quick_links__["a" /* QuickLinksPage */]),
            ],
        })
    ], QuickLinksPageModule);
    return QuickLinksPageModule;
}());

//# sourceMappingURL=quick-links.module.js.map

/***/ }),

/***/ 691:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return PssPageComponent; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__(1);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1_ionic_angular__ = __webpack_require__(44);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__providers_event_auth_event_auth__ = __webpack_require__(150);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3__providers_pss_api_pss_api__ = __webpack_require__(346);
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
    }
    PssPageComponent.prototype.buildNavParams = function (params) {
        params['eventId'] = this.eventId;
        params['eventName'] = this.eventName;
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
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["m" /* Component */])({
            selector: 'pss-page',template:/*ion-inline-start:"/Users/agoldma/git/github/TD/front_v2/src/components/pss-page/pss-page.html"*/'<!-- Generated template for the TopNavComponent component -->\n<div>\n  {{text}}\n</div>\n'/*ion-inline-end:"/Users/agoldma/git/github/TD/front_v2/src/components/pss-page/pss-page.html"*/
        }),
        __metadata("design:paramtypes", [__WEBPACK_IMPORTED_MODULE_2__providers_event_auth_event_auth__["a" /* EventAuthProvider */],
            __WEBPACK_IMPORTED_MODULE_1_ionic_angular__["j" /* NavParams */],
            __WEBPACK_IMPORTED_MODULE_1_ionic_angular__["i" /* NavController */],
            __WEBPACK_IMPORTED_MODULE_1_ionic_angular__["b" /* App */],
            __WEBPACK_IMPORTED_MODULE_3__providers_pss_api_pss_api__["a" /* PssApiProvider */],
            __WEBPACK_IMPORTED_MODULE_1_ionic_angular__["k" /* Platform */]])
    ], PssPageComponent);
    return PssPageComponent;
}());

//# sourceMappingURL=pss-page.js.map

/***/ }),

/***/ 706:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return QuickLinksPage; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__(1);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__components_pss_page_pss_page__ = __webpack_require__(691);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2_ionic_angular__ = __webpack_require__(44);
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
 * Generated class for the QuickLinksPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */
var QuickLinksPage = (function (_super) {
    __extends(QuickLinksPage, _super);
    function QuickLinksPage() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.reorderEnabled = false;
        _this.items = [{ 'title': 'Results - Classics I',
                'icon': 'md-clipboard' },
            { 'title': 'Results - Main A',
                'icon': 'md-clipboard' },
            { 'title': 'Queues - Classics I',
                'icon': 'git-branch' },
            { 'title': 'Queues - Classics I',
                'icon': 'git-branch' },
        ];
        return _this;
    }
    QuickLinksPage.prototype.ionViewDidLoad = function () {
        console.log('ionViewDidLoad QuickLinksPage');
    };
    QuickLinksPage.prototype.reorderItems = function (indexes) {
        this.items = Object(__WEBPACK_IMPORTED_MODULE_2_ionic_angular__["n" /* reorderArray */])(this.items, indexes);
    };
    QuickLinksPage = __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["m" /* Component */])({
            selector: 'page-quick-links',template:/*ion-inline-start:"/Users/agoldma/git/github/TD/front_v2/src/pages/quick-links/quick-links.html"*/'<!--<bobo>-->\n<ion-header>\n<ion-navbar>  \n    <ion-title showWhen=\'mobile\'>\n      {{title}}\n    </ion-title>    \n  <ion-title hideWhen=\'mobile\'>Pss</ion-title>\n  <ion-buttons end hideWhen=\'mobile\'>\n    <button icon-only ion-button [navPush]="eventAuth.isEventUserLoggedIn(eventId)? \'LogoutPage\' : \'LoginPage\'" [navParams]="buildNavParams({})" >{{eventAuth.isEventUserLoggedIn(eventId)? "Logout" : "Login"}}</button>\n    <button icon-only ion-button [navPush]="\'EventSelectPage\'">Switch Events</button>    \n    <button [navPush]="\'ResultsPage\'" icon-only ion-button>Results</button>\n    <button icon-only ion-button>Queues</button>\n    <button *ngIf="eventAuth.getRoleName(eventId)" icon-only ion-button [navPush]="getHomePageString()" [navParams]="buildNavParams({})">{{eventAuth.getRoleName(eventId)}}</button>\n  </ion-buttons>\n</ion-navbar>\n</ion-header>\n<!--</bobo>-->\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n<ion-content>\n\n  <ion-list>\n    <ion-list-header>Jump To...\n      <ion-icon item-end name="cog" (click)="reorderEnabled = reorderEnabled==false"></ion-icon>\n    </ion-list-header>\n      <button ion-item detail-push [navPush]="\'LoginPage\'" [navParams]="buildNavParams({})">\n        <ion-icon name="person" item-end></ion-icon>Login\n      </button>\n      <button ion-item detail-push (click)="pushRootPage(\'EventSelectPage\')">\n        <ion-icon name="md-git-compare" item-end></ion-icon>Switch Event\n      </button>      \n    <ion-item-group [reorder]="reorderEnabled" (ionItemReorder)="reorderItems($event)">      \n    <button *ngFor="let item of items"  ion-item detail-push>{{item.title}}<ion-icon [name]="item.icon" item-end></ion-icon></button>\n    </ion-item-group>\n  </ion-list>\n\n</ion-content>\n'/*ion-inline-end:"/Users/agoldma/git/github/TD/front_v2/src/pages/quick-links/quick-links.html"*/,
        })
    ], QuickLinksPage);
    return QuickLinksPage;
}(__WEBPACK_IMPORTED_MODULE_1__components_pss_page_pss_page__["a" /* PssPageComponent */]));

//# sourceMappingURL=quick-links.js.map

/***/ })

});
//# sourceMappingURL=11.js.map