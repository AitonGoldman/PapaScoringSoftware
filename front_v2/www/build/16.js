webpackJsonp([16],{

/***/ 708:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
Object.defineProperty(__webpack_exports__, "__esModule", { value: true });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "EventOwnerRequestPageModule", function() { return EventOwnerRequestPageModule; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__(1);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1_ionic_angular__ = __webpack_require__(30);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__event_owner_request__ = __webpack_require__(746);
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};



var EventOwnerRequestPageModule = (function () {
    function EventOwnerRequestPageModule() {
    }
    EventOwnerRequestPageModule = __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["NgModule"])({
            declarations: [
                __WEBPACK_IMPORTED_MODULE_2__event_owner_request__["a" /* EventOwnerRequestPage */],
            ],
            imports: [
                __WEBPACK_IMPORTED_MODULE_1_ionic_angular__["h" /* IonicPageModule */].forChild(__WEBPACK_IMPORTED_MODULE_2__event_owner_request__["a" /* EventOwnerRequestPage */]),
            ],
        })
    ], EventOwnerRequestPageModule);
    return EventOwnerRequestPageModule;
}());

//# sourceMappingURL=event-owner-request.module.js.map

/***/ }),

/***/ 728:
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

/***/ 729:
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

/***/ 746:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return EventOwnerRequestPage; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__(1);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1_ionic_angular__ = __webpack_require__(30);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__classes_success_summary__ = __webpack_require__(728);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3__classes_SuccessButton__ = __webpack_require__(729);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_4__providers_pss_api_pss_api__ = __webpack_require__(155);
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
 * Generated class for the EventOwnerRequestPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */
var EventOwnerRequestPage = (function () {
    function EventOwnerRequestPage(pssApi, navCtrl, navParams) {
        this.pssApi = pssApi;
        this.navCtrl = navCtrl;
        this.navParams = navParams;
        this.userInfo = {};
    }
    EventOwnerRequestPage.prototype.ionViewDidLoad = function () {
        console.log('ionViewDidLoad EventOwnerRequestPage');
    };
    EventOwnerRequestPage.prototype.generateEventOwnerCreateRequestProcessor = function () {
        var _this = this;
        return function (result) {
            if (result == null) {
                return;
            }
            var successSummary = new __WEBPACK_IMPORTED_MODULE_2__classes_success_summary__["a" /* SuccessSummary */]('Request has been submitted.', 'You will recieve an email shortly with instructions', 'on how to activate your account.');
            var successButton = new __WEBPACK_IMPORTED_MODULE_3__classes_SuccessButton__["a" /* SuccessButton */]('Go Home', 'EventSelectPage', {}, null);
            _this.navCtrl.push("SuccessPage", { 'successSummary': successSummary,
                'successButtons': [successButton] });
        };
    };
    EventOwnerRequestPage.prototype.submitRequest = function () {
        this.pssApi.eventOwnerCreateRequest(this.userInfo)
            .subscribe(this.generateEventOwnerCreateRequestProcessor());
    };
    EventOwnerRequestPage = __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["Component"])({
            selector: 'page-event-owner-request',template:/*ion-inline-start:"/Users/agoldma/git/github/TD/front_v2/src/pages/event-owner-request/event-owner-request.html"*/'<!--\n  Generated template for the EventOwnerRequestPage page.\n\n  See http://ionicframework.com/docs/components/#navigation for more info on\n  Ionic pages and navigation.\n-->\n<ion-header>\n\n  <ion-navbar>\n    <ion-title>EventOwnerRequest</ion-title>\n  </ion-navbar>\n\n</ion-header>\n\n\n<ion-content padding>\n  <div text-center>\n    If you want to create new events, you will need to create an account.  <br><br>After filling out your info below and clicking "submit request", you will recieve an email with instructions on how to activate your account.\n  </div>\n  <form #loginForm="ngForm">\n  <ion-item>\n  <ion-label floating>Username</ion-label>\n  <ion-input type="text" required\n         [(ngModel)]="userInfo.username" name="username"></ion-input>\n  </ion-item>\n  <ion-item>\n  <ion-label floating>First Name</ion-label>\n  <ion-input type="text" required\n         [(ngModel)]="userInfo.first_name" name="firstname"></ion-input>\n  </ion-item>\n  <ion-item>\n  <ion-label floating>Last Name</ion-label>\n  <ion-input type="text" required\n         [(ngModel)]="userInfo.last_name" name="lastname"></ion-input>\n  </ion-item>\n  <ion-item>\n  <ion-label floating>Password</ion-label>\n  <ion-input type="text" required\n         [(ngModel)]="userInfo.password" name="password"></ion-input>\n  </ion-item>\n  <ion-item>\n  <ion-label floating>email</ion-label>\n  <ion-input type="text" required\n         [(ngModel)]="userInfo.email" name="email"></ion-input>\n  </ion-item>  \n<ion-item no-lines>\n  <button [disabled]=\'!loginForm.valid\' ion-button default (click)="submitRequest()">Submit Request</button>\n</ion-item>\n</form>\n  \n</ion-content>\n'/*ion-inline-end:"/Users/agoldma/git/github/TD/front_v2/src/pages/event-owner-request/event-owner-request.html"*/,
        }),
        __metadata("design:paramtypes", [__WEBPACK_IMPORTED_MODULE_4__providers_pss_api_pss_api__["a" /* PssApiProvider */],
            __WEBPACK_IMPORTED_MODULE_1_ionic_angular__["l" /* NavController */],
            __WEBPACK_IMPORTED_MODULE_1_ionic_angular__["m" /* NavParams */]])
    ], EventOwnerRequestPage);
    return EventOwnerRequestPage;
}());

//# sourceMappingURL=event-owner-request.js.map

/***/ })

});
//# sourceMappingURL=16.js.map