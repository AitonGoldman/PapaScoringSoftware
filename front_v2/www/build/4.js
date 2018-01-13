webpackJsonp([4],{

/***/ 725:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
Object.defineProperty(__webpack_exports__, "__esModule", { value: true });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "TournamentMachinesPageModule", function() { return TournamentMachinesPageModule; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__(1);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1_ionic_angular__ = __webpack_require__(34);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__tournament_machines__ = __webpack_require__(761);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3_ionic2_auto_complete__ = __webpack_require__(358);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_4_angular2_notifications__ = __webpack_require__(356);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_4_angular2_notifications___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_4_angular2_notifications__);
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};





var TournamentMachinesPageModule = (function () {
    function TournamentMachinesPageModule() {
    }
    TournamentMachinesPageModule = __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["NgModule"])({
            declarations: [
                __WEBPACK_IMPORTED_MODULE_2__tournament_machines__["a" /* TournamentMachinesPage */],
            ],
            imports: [
                __WEBPACK_IMPORTED_MODULE_1_ionic_angular__["g" /* IonicPageModule */].forChild(__WEBPACK_IMPORTED_MODULE_2__tournament_machines__["a" /* TournamentMachinesPage */]),
                __WEBPACK_IMPORTED_MODULE_3_ionic2_auto_complete__["a" /* AutoCompleteModule */],
                __WEBPACK_IMPORTED_MODULE_4_angular2_notifications__["SimpleNotificationsModule"].forRoot()
            ],
        })
    ], TournamentMachinesPageModule);
    return TournamentMachinesPageModule;
}());

//# sourceMappingURL=tournament-machines.module.js.map

/***/ }),

/***/ 727:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return PssPageComponent; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__(1);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1_ionic_angular__ = __webpack_require__(34);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__providers_event_auth_event_auth__ = __webpack_require__(87);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3__providers_pss_api_pss_api__ = __webpack_require__(155);
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
        if (role == "tournamentdirector") {
            return 'TournamentDirectorHomePage';
        }
        if (role == "eventowner") {
            return 'EventOwnerHomePage';
        }
        if (role == "player") {
            return 'PlayerHomePage';
        }
        if (role == "scorekeeper") {
            return 'ScorekeeperHomePage';
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
            this.navCtrl.parent.getByIndex(tabIndex).setRoot(pageName, navParams, { animate: false });
            this.navCtrl.parent.select(tabIndex);
            return;
        }
        this.navCtrl.getActive().willLeave.subscribe(function () {
            _this.navCtrl.last().showBackButton(false);
        });
        this.navCtrl.push(pageName, this.buildNavParams(navParams));
    };
    PssPageComponent.prototype.expand = function (item) {
        item.expanded = item.expanded == false ? true : false;
    };
    PssPageComponent.prototype.generateEditTournamentProcessor = function (message_string) {
        return function (result) {
            if (result == null) {
                return;
            }
        };
    };
    PssPageComponent.prototype.onTournamentToggle = function (eventId, tournament) {
        tournament.active = tournament.active != true;
        var stringDescription = tournament.active != true ? "deactivated" : "activated";
        this.pssApi.editTournament(tournament, eventId)
            .subscribe(this.generateEditTournamentProcessor(tournament.tournament_name + " has been " + stringDescription));
    };
    // auto complete stuff
    PssPageComponent.prototype.generateAutoCompleteGetEventPlayerProcessor = function () {
        var _this = this;
        return function (result) {
            if (result == null) {
                return;
            }
            _this['selectedPlayer'] = result.data;
            _this['ticketCounts'] = _this.generateListFromObj(_this['selectedPlayer'].tournament_counts);
        };
    };
    PssPageComponent.prototype.onAutoCompletePlayerSelected = function () {
        this.pssApi.getEventPlayer(this.eventId, this['selectedPlayer'].player_id_for_event)
            .subscribe(this.generateAutoCompleteGetEventPlayerProcessor());
    };
    PssPageComponent.prototype.generatePlayerLoadingFunction = function () {
        var _this = this;
        return function (input) {
            if (input != null) {
                _this['selectedPlayer'] = input.data;
                _this['ticketCounts'] = _this.generateListFromObj(_this['selectedPlayer'].tournament_counts);
            }
            setTimeout(function () { _this['loading'] = false; }, 500);
        };
    };
    PssPageComponent.prototype.generateListFromObj = function (obj) {
        if (obj == null) {
            return [];
        }
        return Object.keys(obj).map(function (key) {
            var objValue = obj[key];
            // do something with person
            return objValue;
        });
    };
    PssPageComponent = __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["Component"])({
            selector: 'pss-page',template:/*ion-inline-start:"/Users/agoldma/git/github/TD/front_v2/src/components/pss-page/pss-page.html"*/'<!-- Generated template for the TopNavComponent component -->\n<div>\n  {{text}}\n</div>\n'/*ion-inline-end:"/Users/agoldma/git/github/TD/front_v2/src/components/pss-page/pss-page.html"*/
        }),
        __metadata("design:paramtypes", [__WEBPACK_IMPORTED_MODULE_2__providers_event_auth_event_auth__["a" /* EventAuthProvider */],
            __WEBPACK_IMPORTED_MODULE_1_ionic_angular__["m" /* NavParams */],
            __WEBPACK_IMPORTED_MODULE_1_ionic_angular__["l" /* NavController */],
            __WEBPACK_IMPORTED_MODULE_1_ionic_angular__["c" /* App */],
            __WEBPACK_IMPORTED_MODULE_3__providers_pss_api_pss_api__["a" /* PssApiProvider */],
            __WEBPACK_IMPORTED_MODULE_1_ionic_angular__["n" /* Platform */],
            __WEBPACK_IMPORTED_MODULE_4_angular2_notifications__["NotificationsService"]])
    ], PssPageComponent);
    return PssPageComponent;
}());

//# sourceMappingURL=pss-page.js.map

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

/***/ 761:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return TournamentMachinesPage; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__(1);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__components_pss_page_pss_page__ = __webpack_require__(727);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__providers_auto_complete_auto_complete__ = __webpack_require__(357);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3_ionic_angular__ = __webpack_require__(34);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_4__providers_event_auth_event_auth__ = __webpack_require__(87);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_5__providers_pss_api_pss_api__ = __webpack_require__(155);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_6__classes_success_summary__ = __webpack_require__(728);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_7__classes_SuccessButton__ = __webpack_require__(729);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_8_angular2_notifications__ = __webpack_require__(356);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_8_angular2_notifications___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_8_angular2_notifications__);
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
 * Generated class for the TournamentMachinesPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */
var TournamentMachinesPage = (function (_super) {
    __extends(TournamentMachinesPage, _super);
    function TournamentMachinesPage(autoCompleteProvider, eventAuth, navParams, navCtrl, appCtrl, pssApi, platform, actionSheetCtrl, notificationsService) {
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
        _this.wizardMode = null;
        _this.wizardEntity = null;
        _this.sliding = true;
        _this.selectedMachines = [];
        return _this;
    }
    TournamentMachinesPage.prototype.generateGetAllTournamentMachinesProcessor = function () {
        var _this = this;
        return function (result) {
            if (result == null) {
                return;
            }
            _this.autoCompleteProvider.setMachines(result.data.machines_list);
            _this.selectedMachines = result.data.tournament_machines_list;
        };
    };
    TournamentMachinesPage.prototype.generateGetAllMachinesProcessor = function () {
        var _this = this;
        return function (result) {
            if (result == null) {
                return;
            }
            _this.autoCompleteProvider.setMachines(result.data);
        };
    };
    TournamentMachinesPage.prototype.generateAddEditTournamentMachineProcessor = function (message_string, action) {
        var _this = this;
        return function (result) {
            if (result == null) {
                return;
            }
            //toast.present();
            _this.notificationsService.success("Success", message_string, {
                timeOut: 0,
                position: ["top", "right"],
                theClass: 'poop'
            });
            if (action == "add") {
                _this.selectedMachines[_this.selectedMachines.length - 1] = result.data;
            }
        };
    };
    TournamentMachinesPage.prototype.generateCreateWizardProcessor = function () {
        var _this = this;
        return function (result) {
            if (result == null) {
                return;
            }
            var successTitle = 'Fix This Message';
            var successSummary = new __WEBPACK_IMPORTED_MODULE_6__classes_success_summary__["a" /* SuccessSummary */](successTitle, null, null);
            var successButton = new __WEBPACK_IMPORTED_MODULE_7__classes_SuccessButton__["a" /* SuccessButton */]('Go Home', _this.getHomePageString(), _this.buildNavParams({}));
            _this.navCtrl.push("SuccessPage", _this.buildNavParams({ 'successSummary': successSummary,
                'successButtons': [successButton] }));
        };
    };
    TournamentMachinesPage.prototype.onRemove = function (machine) {
        var _this = this;
        var actionSheet = this.actionSheetCtrl.create({
            title: 'Are you SURE you want to remove ' + machine.tournament_machine_name + '?',
            buttons: [
                {
                    text: 'Remove',
                    role: 'destructive',
                    handler: function () {
                        _this.onRemoveConfirmed(machine);
                        console.log('Destructive clicked');
                    }
                },
                {
                    text: 'Cancel',
                    role: 'cancel',
                    handler: function () {
                        console.log('Cancel clicked');
                    }
                }
            ]
        });
        actionSheet.present();
    };
    TournamentMachinesPage.prototype.onRemoveConfirmed = function (machine) {
        machine.removed = true;
        if (this.wizardMode != null) {
            return;
        }
        this.pssApi.editTournamentMachine(machine, this.eventId)
            .subscribe(this.generateAddEditTournamentMachineProcessor(machine.tournament_machine_name + " has been removed!", "edit"));
    };
    TournamentMachinesPage.prototype.onInput = function (event) {
    };
    TournamentMachinesPage.prototype.onItemsShown = function (event) {
    };
    TournamentMachinesPage.prototype.onDisable = function (machine) {
        machine.active = machine.active == false;
        if (this.wizardMode != null) {
            return;
        }
        var stringDescription = machine.active == true ? "enabled" : "disabled";
        this.pssApi.editTournamentMachine(machine, this.eventId)
            .subscribe(this.generateAddEditTournamentMachineProcessor(machine.tournament_machine_name + " has been " + stringDescription, "edit"));
    };
    TournamentMachinesPage.prototype.onSelect = function (event) {
        this.selectedMachine.tournament_id = this.tournamentId;
        this.selectedMachine.tournament_machine_name = this.selectedMachine.machine_name;
        //this.selectedMachine=result.data;
        this.selectedMachines.push(this.selectedMachine);
        if (this.wizardMode != null) {
            return;
        }
        this.pssApi.addTournamentMachine(this.selectedMachine, this.eventId)
            .subscribe(this.generateAddEditTournamentMachineProcessor(this.selectedMachine.tournament_machine_name + " has been added", "add"));
    };
    TournamentMachinesPage.prototype.onSubmit = function () {
        this.wizardEntity['tournament_machines'] = this.selectedMachines;
        if ('event' in this.wizardEntity) {
            this.pssApi.createWizardEvent(this.wizardEntity)
                .subscribe(this.generateCreateWizardProcessor());
        }
        else {
            this.wizardEntity['tournament']['tournament']['event_id'] = this.eventId;
            this.pssApi.createWizardTournament(this.wizardEntity)
                .subscribe(this.generateCreateWizardProcessor());
        }
    };
    TournamentMachinesPage.prototype.onFocus = function () {
        this.selectedMachine = null;
    };
    TournamentMachinesPage.prototype.ionViewWillLoad = function () {
        //this.targetEventId=this.navParams.get('eventId');
        this.tournamentId = this.navParams.get('tournamentId');
        this.eventId = this.navParams.get('eventId');
        this.wizardMode = this.navParams.get('wizardMode');
        this.wizardEntity = this.navParams.get('wizardEntity');
        if (this.wizardMode == null) {
            this.pssApi.getAllTournamentMachines(this.eventId, this.tournamentId)
                .subscribe(this.generateGetAllTournamentMachinesProcessor());
        }
        else {
            this.pssApi.getAllMachines()
                .subscribe(this.generateGetAllMachinesProcessor());
        }
        console.log('ionViewDidLoad TournamentMachinesPage');
    };
    __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["ViewChild"])('searchbar'),
        __metadata("design:type", Object)
    ], TournamentMachinesPage.prototype, "searchbar", void 0);
    __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["ViewChild"])('myform'),
        __metadata("design:type", Object)
    ], TournamentMachinesPage.prototype, "myform", void 0);
    __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["ViewChild"])(__WEBPACK_IMPORTED_MODULE_3_ionic_angular__["h" /* List */]),
        __metadata("design:type", __WEBPACK_IMPORTED_MODULE_3_ionic_angular__["h" /* List */])
    ], TournamentMachinesPage.prototype, "list", void 0);
    TournamentMachinesPage = __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["Component"])({
            selector: 'page-tournament-machines',template:/*ion-inline-start:"/Users/agoldma/git/github/TD/front_v2/src/components/tournament-machines/tournament-machines.html"*/'<!--\n  Generated template for the TournamentMachinesPage page.\n\n  See http://ionicframework.com/docs/components/#navigation for more info on\n  Ionic pages and navigation.\n-->\n<ion-header>\n  <ion-navbar>\n    <ion-title></ion-title>\n    <ion-buttons end hideWhen="mobile">\n      <button icon-only ion-button [navPush]="\'EventSelectPage\'">Switch Events</button>    \n      <button icon-only ion-button [navPush]="destPageAfterSuccess" [navParams]=\'buildNavParams({})\'>Home</button>    \n    </ion-buttons>\n  </ion-navbar>\n</ion-header>\n\n<simple-notifications  [options]="{position:[\'top\',\'right\']}"></simple-notifications>\n<ion-content padding>\n  <form #myform="ngForm" novalidate>\n    <ion-auto-complete name="myautocomplete" [(ngModel)]="selectedMachine" (itemsShown)="onItemsShown($event)" (ionAutoInput)="onInput($event)" (autoFocus)="onFocus()" (itemSelected)="onSelect()" #searchbar [dataProvider]="autoCompleteProvider"></ion-auto-complete>\n  </form>\n  <br>\n  <ion-list [sliding]="sliding" #list>\n      <ion-item-sliding *ngFor="let machine of selectedMachines">\n        <ion-item *ngIf="machine.removed!=true">\n          <ion-icon [name]="machine.active==true? \'play\' : \'pause\'" ></ion-icon>\n          <button hideWhen=\'mobile\' (click)="onRemove(machine)" ion-button item-end>Remove</button> {{machine.tournament_machine_name}}\n          <button hideWhen=\'mobile\' (click)="onDisable(machine)" ion-button item-end>{{machine.active==true?"Disable":"Enable"}}</button> \n        </ion-item>\n        <ion-item-options *ngIf="machine.removed!=true" side="right">\n          <button round ion-button color="danger">\n            <ion-icon name="archive"></ion-icon>\n            Remove\n          </button>\n          <button round ion-button>\n            <ion-icon name="archive"></ion-icon>\n            {{machine.active==true?"Disable":"Enable"}}\n          </button>\n        </ion-item-options>\n      </ion-item-sliding>\n  </ion-list>\n  <button ion-button *ngIf="wizardMode!=null" (click)="onSubmit()">Submit</button>\n</ion-content>\n'/*ion-inline-end:"/Users/agoldma/git/github/TD/front_v2/src/components/tournament-machines/tournament-machines.html"*/,
        }),
        __metadata("design:paramtypes", [__WEBPACK_IMPORTED_MODULE_2__providers_auto_complete_auto_complete__["a" /* AutoCompleteProvider */],
            __WEBPACK_IMPORTED_MODULE_4__providers_event_auth_event_auth__["a" /* EventAuthProvider */],
            __WEBPACK_IMPORTED_MODULE_3_ionic_angular__["m" /* NavParams */],
            __WEBPACK_IMPORTED_MODULE_3_ionic_angular__["l" /* NavController */],
            __WEBPACK_IMPORTED_MODULE_3_ionic_angular__["c" /* App */],
            __WEBPACK_IMPORTED_MODULE_5__providers_pss_api_pss_api__["a" /* PssApiProvider */],
            __WEBPACK_IMPORTED_MODULE_3_ionic_angular__["n" /* Platform */],
            __WEBPACK_IMPORTED_MODULE_3_ionic_angular__["a" /* ActionSheetController */],
            __WEBPACK_IMPORTED_MODULE_8_angular2_notifications__["NotificationsService"]])
    ], TournamentMachinesPage);
    return TournamentMachinesPage;
}(__WEBPACK_IMPORTED_MODULE_1__components_pss_page_pss_page__["a" /* PssPageComponent */]));

//# sourceMappingURL=tournament-machines.js.map

/***/ })

});
//# sourceMappingURL=4.js.map