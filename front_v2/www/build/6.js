webpackJsonp([6],{

/***/ 714:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
Object.defineProperty(__webpack_exports__, "__esModule", { value: true });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "TicketPurchasePageModule", function() { return TicketPurchasePageModule; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__(1);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1_ionic_angular__ = __webpack_require__(40);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__ticket_purchase__ = __webpack_require__(743);
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};



var TicketPurchasePageModule = (function () {
    function TicketPurchasePageModule() {
    }
    TicketPurchasePageModule = __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["NgModule"])({
            declarations: [
                __WEBPACK_IMPORTED_MODULE_2__ticket_purchase__["a" /* TicketPurchasePage */],
            ],
            imports: [
                __WEBPACK_IMPORTED_MODULE_1_ionic_angular__["g" /* IonicPageModule */].forChild(__WEBPACK_IMPORTED_MODULE_2__ticket_purchase__["a" /* TicketPurchasePage */]),
            ],
        })
    ], TicketPurchasePageModule);
    return TicketPurchasePageModule;
}());

//# sourceMappingURL=ticket-purchase.module.js.map

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

/***/ 743:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return TicketPurchasePage; });
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
 * Generated class for the TicketPurchasePage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */
var TicketPurchasePage = (function (_super) {
    __extends(TicketPurchasePage, _super);
    function TicketPurchasePage() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.ticketPriceLists = null;
        _this.ticketCounts = null;
        _this.eventPlayer = {};
        _this.player_id_for_event = null;
        _this.totalCost = 0;
        return _this;
    }
    TicketPurchasePage.prototype.ionViewDidLoad = function () {
        console.log('ionViewDidLoad TicketPurchasePage');
    };
    TicketPurchasePage.prototype.generateGetEventPlayerProcessor = function () {
        var _this = this;
        return function (result) {
            if (result == null) {
                return;
            }
            _this.eventPlayer = result.data != null ? result.data : {};
            _this.ticketPriceLists = result.tournament_calculated_lists;
            _this.ticketCounts = result.tournament_counts;
            console.log(result);
        };
    };
    TicketPurchasePage.prototype.generatePurchaseTicketProcessor = function (purchaseSummary) {
        var _this = this;
        return function (result) {
            if (result == null) {
                return;
            }
            var success_title_string = 'Tickets Purchased!';
            var successSummary = new __WEBPACK_IMPORTED_MODULE_2__classes_success_summary__["a" /* SuccessSummary */](success_title_string, purchaseSummary.pop(), null);
            successSummary.setSummaryTable(purchaseSummary);
            var successButton = new __WEBPACK_IMPORTED_MODULE_3__classes_SuccessButton__["a" /* SuccessButton */]('Go Home', _this.getHomePageString(_this.eventId), _this.buildNavParams({}));
            _this.navCtrl.push("SuccessPage", _this.buildNavParams({ 'successSummary': successSummary,
                'successButtons': [successButton] }));
        };
    };
    TicketPurchasePage.prototype.clearValues = function () {
        this.ticketPriceLists = null;
        this.ticketCounts = null;
        this.eventPlayer = {};
        //this.player_id_for_event=null;
        this.totalCost = 0;
    };
    TicketPurchasePage.prototype.onInput = function (event) {
        if (this.player_id_for_event != null && this.player_id_for_event > 99 && this.player_id_for_event < 1000) {
            console.log('in onInput');
            this.pssApi.getEventPlayer(this.eventId, this.player_id_for_event)
                .subscribe(this.generateGetEventPlayerProcessor());
        }
        else {
            this.clearValues();
        }
    };
    TicketPurchasePage.prototype.onSelect = function (event) {
        this.totalCost = 0;
        console.log('in onSelect');
        for (var _i = 0, _a = this.ticketPriceLists; _i < _a.length; _i++) {
            var ticketPrice = _a[_i];
            if (ticketPrice.selectedCount != null) {
                this.totalCost = this.totalCost + ticketPrice.selectedCount.price;
            }
        }
    };
    TicketPurchasePage.prototype.ticketPurchase = function () {
        var ticketsToBuy = {};
        ticketsToBuy['player_id'] = this.eventPlayer.player_id;
        ticketsToBuy['tournament_token_counts'] = [];
        var purchaseSummary = [];
        for (var _i = 0, _a = this.ticketPriceLists; _i < _a.length; _i++) {
            var ticketsSelected = _a[_i];
            if (ticketsSelected.selectedCount != null) {
                ticketsToBuy['tournament_token_counts'].push({ token_count: ticketsSelected.selectedCount.amount,
                    tournament_id: ticketsSelected.tournament_id });
                purchaseSummary.push(ticketsSelected.tournament_name + " : " + ticketsSelected.selectedCount.amount);
            }
        }
        purchaseSummary.push("total cost : " + this.totalCost);
        console.log(ticketsToBuy);
        this.pssApi.purchaseTicket(ticketsToBuy, this.eventId)
            .subscribe(this.generatePurchaseTicketProcessor(purchaseSummary));
        //        post_dict={"player_id":player_id,
        //                   "tournament_token_counts":[{"token_count":1,"tournament_id":tournament_id}],
        //                   "meta_tournament_token_counts":[{"token_count":1,"meta_tournament_id":meta_tournament['data']['meta_tournament_id']}]}        
    };
    TicketPurchasePage = __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["Component"])({
            selector: 'page-ticket-purchase',template:/*ion-inline-start:"/Users/agoldma/git/github/TD/front_v2/src/pages/ticket-purchase/ticket-purchase.html"*/'<ion-content padding>\n  <ion-searchbar\n     [(ngModel)]="player_id_for_event"\n     (ionInput)="onInput($event)">\n  </ion-searchbar>\n  <ng-container *ngIf="eventPlayer.first_name!=null ">\n    <ion-item>\n      Player Name : {{eventPlayer.player_full_name}}\n    </ion-item>\n    <form #myForm="ngForm">\n    \n    <ng-container *ngFor="let ticketPriceList of ticketPriceLists">\n      <ion-item no-lines>\n        Existing Count : {{ticketCounts[ticketPriceList.tournament_id]==null?0:ticketCounts[ticketPriceList.tournament_id].count}}\n      </ion-item>\n      <ion-item>\n        <ion-label>{{ticketPriceList.tournament_name}}</ion-label>\n        <ion-select [name]="ticketPriceList.tournament_name" [(ngModel)]="ticketPriceList.selectedCount" [selectOptions]="{title:\'poop\'}" (ionChange)="onSelect($event)">\n          <ion-option *ngFor="let calculatedPrice of ticketPriceList.calculated_price_list" [value]="calculatedPrice">{{calculatedPrice.amount}}</ion-option>\n        </ion-select>\n      </ion-item>\n    </ng-container>\n    <ion-item>\n      Total Cost : {{totalCost}}\n    </ion-item>\n    <ion-item>\n      <button [disabled]="!myForm.dirty" ion-button (click)="ticketPurchase()"> Purchase Tickets </button>\n    </ion-item>\n    </form>\n    \n  </ng-container>\n</ion-content>\n'/*ion-inline-end:"/Users/agoldma/git/github/TD/front_v2/src/pages/ticket-purchase/ticket-purchase.html"*/,
        })
    ], TicketPurchasePage);
    return TicketPurchasePage;
}(__WEBPACK_IMPORTED_MODULE_1__components_pss_page_pss_page__["a" /* PssPageComponent */]));

//# sourceMappingURL=ticket-purchase.js.map

/***/ })

});
//# sourceMappingURL=6.js.map