webpackJsonp([7],{

/***/ 710:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
Object.defineProperty(__webpack_exports__, "__esModule", { value: true });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "TournamentMachinesPageModule", function() { return TournamentMachinesPageModule; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__(1);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1_ionic_angular__ = __webpack_require__(43);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__tournament_machines__ = __webpack_require__(742);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3_ionic2_auto_complete__ = __webpack_require__(354);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_4_angular2_notifications__ = __webpack_require__(350);
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
                __WEBPACK_IMPORTED_MODULE_1_ionic_angular__["f" /* IonicPageModule */].forChild(__WEBPACK_IMPORTED_MODULE_2__tournament_machines__["a" /* TournamentMachinesPage */]),
                __WEBPACK_IMPORTED_MODULE_3_ionic2_auto_complete__["a" /* AutoCompleteModule */],
                __WEBPACK_IMPORTED_MODULE_4_angular2_notifications__["SimpleNotificationsModule"].forRoot()
            ],
        })
    ], TournamentMachinesPageModule);
    return TournamentMachinesPageModule;
}());

//# sourceMappingURL=tournament-machines.module.js.map

/***/ }),

/***/ 711:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return PssPageComponent; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__(1);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1_ionic_angular__ = __webpack_require__(43);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__providers_event_auth_event_auth__ = __webpack_require__(151);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3__providers_pss_api_pss_api__ = __webpack_require__(351);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_4_angular2_notifications__ = __webpack_require__(350);
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
            __WEBPACK_IMPORTED_MODULE_1_ionic_angular__["j" /* NavParams */],
            __WEBPACK_IMPORTED_MODULE_1_ionic_angular__["i" /* NavController */],
            __WEBPACK_IMPORTED_MODULE_1_ionic_angular__["b" /* App */],
            __WEBPACK_IMPORTED_MODULE_3__providers_pss_api_pss_api__["a" /* PssApiProvider */],
            __WEBPACK_IMPORTED_MODULE_1_ionic_angular__["k" /* Platform */],
            __WEBPACK_IMPORTED_MODULE_4_angular2_notifications__["NotificationsService"]])
    ], PssPageComponent);
    return PssPageComponent;
}());

//# sourceMappingURL=pss-page.js.map

/***/ }),

/***/ 712:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return SuccessSummary; });
var SuccessSummary = (function () {
    //title:string = null;
    //firstLine:string = null;
    //secondLine:string = null;
    function SuccessSummary(title, firstLine, secondLine) {
        this.title = title;
        this.firstLine = firstLine;
        this.secondLine = secondLine;
    }
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

/***/ 713:
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

/***/ 718:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return TournamentMachinesComponent; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__(1);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__pss_page_pss_page__ = __webpack_require__(711);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__providers_auto_complete_auto_complete__ = __webpack_require__(353);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3_ionic_angular__ = __webpack_require__(43);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_4__providers_event_auth_event_auth__ = __webpack_require__(151);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_5__providers_pss_api_pss_api__ = __webpack_require__(351);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_6__classes_success_summary__ = __webpack_require__(712);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_7__classes_SuccessButton__ = __webpack_require__(713);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_8_angular2_notifications__ = __webpack_require__(350);
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
var TournamentMachinesComponent = (function (_super) {
    __extends(TournamentMachinesComponent, _super);
    function TournamentMachinesComponent(autoCompleteProvider, eventAuth, navParams, navCtrl, appCtrl, pssApi, platform, toastCtrl, actionSheetCtrl, notificationsService) {
        var _this = _super.call(this, eventAuth, navParams, navCtrl, appCtrl, pssApi, platform, notificationsService) || this;
        _this.autoCompleteProvider = autoCompleteProvider;
        _this.eventAuth = eventAuth;
        _this.navParams = navParams;
        _this.navCtrl = navCtrl;
        _this.appCtrl = appCtrl;
        _this.pssApi = pssApi;
        _this.platform = platform;
        _this.toastCtrl = toastCtrl;
        _this.actionSheetCtrl = actionSheetCtrl;
        _this.notificationsService = notificationsService;
        _this.wizardMode = null;
        _this.wizardEntity = null;
        _this.sliding = true;
        _this.selectedMachines = [];
        return _this;
    }
    TournamentMachinesComponent.prototype.generateGetAllTournamentMachinesProcessor = function () {
        var _this = this;
        return function (result) {
            if (result == null) {
                return;
            }
            _this.autoCompleteProvider.setMachines(result.data.machines_list);
            _this.selectedMachines = result.data.tournament_machines_list;
        };
    };
    TournamentMachinesComponent.prototype.generateGetAllMachinesProcessor = function () {
        var _this = this;
        return function (result) {
            if (result == null) {
                return;
            }
            _this.autoCompleteProvider.setMachines(result.data);
        };
    };
    TournamentMachinesComponent.prototype.generateAddEditTournamentMachineProcessor = function (message_string, action) {
        var _this = this;
        return function (result) {
            if (result == null) {
                return;
            }
            var toast = _this.toastCtrl.create({
                message: message_string,
                duration: 99000,
                position: 'top',
                showCloseButton: true
            });
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
    TournamentMachinesComponent.prototype.generateCreateWizardProcessor = function () {
        var _this = this;
        return function (result) {
            if (result == null) {
                return;
            }
            var successTitle = 'Fix This Message';
            var successSummary = new __WEBPACK_IMPORTED_MODULE_6__classes_success_summary__["a" /* SuccessSummary */](successTitle, null, null);
            var successButton = new __WEBPACK_IMPORTED_MODULE_7__classes_SuccessButton__["a" /* SuccessButton */]('Go Home', _this.destPageAfterSuccess, _this.buildNavParams({}));
            _this.navCtrl.push("SuccessPage", _this.buildNavParams({ 'successSummary': successSummary,
                'successButtons': [successButton] }));
        };
    };
    TournamentMachinesComponent.prototype.onRemove = function (machine) {
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
    TournamentMachinesComponent.prototype.onRemoveConfirmed = function (machine) {
        machine.removed = true;
        if (this.wizardMode != null) {
            return;
        }
        this.pssApi.editTournamentMachine(machine, this.eventId)
            .subscribe(this.generateAddEditTournamentMachineProcessor(machine.tournament_machine_name + " has been removed!", "edit"));
    };
    TournamentMachinesComponent.prototype.onInput = function (event) {
        console.log(this.searchbar);
        console.log(event);
    };
    TournamentMachinesComponent.prototype.onItemsShown = function (event) {
        console.log(event);
    };
    TournamentMachinesComponent.prototype.onDisable = function (machine) {
        machine.active = machine.active == false;
        if (this.wizardMode != null) {
            return;
        }
        var stringDescription = machine.active == true ? "enabled" : "disabled";
        this.pssApi.editTournamentMachine(machine, this.eventId)
            .subscribe(this.generateAddEditTournamentMachineProcessor(machine.tournament_machine_name + " has been " + stringDescription, "edit"));
    };
    TournamentMachinesComponent.prototype.onSelect = function (event) {
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
    TournamentMachinesComponent.prototype.onSubmit = function () {
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
    TournamentMachinesComponent.prototype.onFocus = function () {
        this.selectedMachine = null;
    };
    TournamentMachinesComponent.prototype.ionViewWillLoad = function () {
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
        console.log(this.constructor.name);
    };
    __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["ViewChild"])('searchbar'),
        __metadata("design:type", Object)
    ], TournamentMachinesComponent.prototype, "searchbar", void 0);
    __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["ViewChild"])('myform'),
        __metadata("design:type", Object)
    ], TournamentMachinesComponent.prototype, "myform", void 0);
    __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["ViewChild"])(__WEBPACK_IMPORTED_MODULE_3_ionic_angular__["g" /* List */]),
        __metadata("design:type", __WEBPACK_IMPORTED_MODULE_3_ionic_angular__["g" /* List */])
    ], TournamentMachinesComponent.prototype, "list", void 0);
    TournamentMachinesComponent = __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["Component"])({
            selector: 'page-tournament-machines',template:/*ion-inline-start:"/Users/agoldma/git/github/TD/front_v2/src/components/tournament-machines/tournament-machines.html"*/'<!--\n  Generated template for the TournamentMachinesPage page.\n\n  See http://ionicframework.com/docs/components/#navigation for more info on\n  Ionic pages and navigation.\n-->\n<ion-header>\n  <ion-navbar>\n    <ion-title></ion-title>\n    <ion-buttons end hideWhen="mobile">\n      <button icon-only ion-button [navPush]="\'EventSelectPage\'">Switch Events</button>    \n      <button icon-only ion-button [navPush]="destPageAfterSuccess" [navParams]=\'buildNavParams({})\'>Home</button>    \n    </ion-buttons>\n  </ion-navbar>\n</ion-header>\n\n<simple-notifications  [options]="{position:[\'top\',\'right\']}"></simple-notifications>\n<ion-content padding>\n  <form #myform="ngForm" novalidate>\n    <ion-auto-complete name="myautocomplete" [(ngModel)]="selectedMachine" (itemsShown)="onItemsShown($event)" (ionAutoInput)="onInput($event)" (autoFocus)="onFocus()" (itemSelected)="onSelect()" #searchbar [dataProvider]="autoCompleteProvider"></ion-auto-complete>\n  </form>\n  <br>\n  <ion-list [sliding]="sliding" #list>\n      <ion-item-sliding *ngFor="let machine of selectedMachines">\n        <ion-item *ngIf="machine.removed!=true">\n          <ion-icon [name]="machine.active==true? \'play\' : \'pause\'" ></ion-icon>\n          <button hideWhen=\'mobile\' (click)="onRemove(machine)" ion-button item-end>Remove</button> {{machine.tournament_machine_name}}\n          <button hideWhen=\'mobile\' (click)="onDisable(machine)" ion-button item-end>{{machine.active==true?"Disable":"Enable"}}</button> \n        </ion-item>\n        <ion-item-options *ngIf="machine.removed!=true" side="right">\n          <button round ion-button color="danger">\n            <ion-icon name="archive"></ion-icon>\n            Remove\n          </button>\n          <button round ion-button>\n            <ion-icon name="archive"></ion-icon>\n            {{machine.active==true?"Disable":"Enable"}}\n          </button>\n        </ion-item-options>\n      </ion-item-sliding>\n  </ion-list>\n  <button ion-button *ngIf="wizardMode!=null" (click)="onSubmit()">Submit</button>\n</ion-content>\n'/*ion-inline-end:"/Users/agoldma/git/github/TD/front_v2/src/components/tournament-machines/tournament-machines.html"*/,
        }),
        __metadata("design:paramtypes", [__WEBPACK_IMPORTED_MODULE_2__providers_auto_complete_auto_complete__["a" /* AutoCompleteProvider */],
            __WEBPACK_IMPORTED_MODULE_4__providers_event_auth_event_auth__["a" /* EventAuthProvider */],
            __WEBPACK_IMPORTED_MODULE_3_ionic_angular__["j" /* NavParams */],
            __WEBPACK_IMPORTED_MODULE_3_ionic_angular__["i" /* NavController */],
            __WEBPACK_IMPORTED_MODULE_3_ionic_angular__["b" /* App */],
            __WEBPACK_IMPORTED_MODULE_5__providers_pss_api_pss_api__["a" /* PssApiProvider */],
            __WEBPACK_IMPORTED_MODULE_3_ionic_angular__["k" /* Platform */],
            __WEBPACK_IMPORTED_MODULE_3_ionic_angular__["m" /* ToastController */],
            __WEBPACK_IMPORTED_MODULE_3_ionic_angular__["a" /* ActionSheetController */],
            __WEBPACK_IMPORTED_MODULE_8_angular2_notifications__["NotificationsService"]])
    ], TournamentMachinesComponent);
    return TournamentMachinesComponent;
}(__WEBPACK_IMPORTED_MODULE_1__pss_page_pss_page__["a" /* PssPageComponent */]));

//# sourceMappingURL=tournament-machines.js.map

/***/ }),

/***/ 742:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return TournamentMachinesPage; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__(1);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__components_tournament_machines_tournament_machines__ = __webpack_require__(718);
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
 * Generated class for the TournamentMachinesPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */
var TournamentMachinesPage = (function (_super) {
    __extends(TournamentMachinesPage, _super);
    function TournamentMachinesPage() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.destPageAfterSuccess = 'TournamentDirectorHomePage';
        return _this;
    }
    TournamentMachinesPage = __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["Component"])({
            selector: 'page-tournament-machines',template:/*ion-inline-start:"/Users/agoldma/git/github/TD/front_v2/src/components/tournament-machines/tournament-machines.html"*/'<!--\n  Generated template for the TournamentMachinesPage page.\n\n  See http://ionicframework.com/docs/components/#navigation for more info on\n  Ionic pages and navigation.\n-->\n<ion-header>\n  <ion-navbar>\n    <ion-title></ion-title>\n    <ion-buttons end hideWhen="mobile">\n      <button icon-only ion-button [navPush]="\'EventSelectPage\'">Switch Events</button>    \n      <button icon-only ion-button [navPush]="destPageAfterSuccess" [navParams]=\'buildNavParams({})\'>Home</button>    \n    </ion-buttons>\n  </ion-navbar>\n</ion-header>\n\n<simple-notifications  [options]="{position:[\'top\',\'right\']}"></simple-notifications>\n<ion-content padding>\n  <form #myform="ngForm" novalidate>\n    <ion-auto-complete name="myautocomplete" [(ngModel)]="selectedMachine" (itemsShown)="onItemsShown($event)" (ionAutoInput)="onInput($event)" (autoFocus)="onFocus()" (itemSelected)="onSelect()" #searchbar [dataProvider]="autoCompleteProvider"></ion-auto-complete>\n  </form>\n  <br>\n  <ion-list [sliding]="sliding" #list>\n      <ion-item-sliding *ngFor="let machine of selectedMachines">\n        <ion-item *ngIf="machine.removed!=true">\n          <ion-icon [name]="machine.active==true? \'play\' : \'pause\'" ></ion-icon>\n          <button hideWhen=\'mobile\' (click)="onRemove(machine)" ion-button item-end>Remove</button> {{machine.tournament_machine_name}}\n          <button hideWhen=\'mobile\' (click)="onDisable(machine)" ion-button item-end>{{machine.active==true?"Disable":"Enable"}}</button> \n        </ion-item>\n        <ion-item-options *ngIf="machine.removed!=true" side="right">\n          <button round ion-button color="danger">\n            <ion-icon name="archive"></ion-icon>\n            Remove\n          </button>\n          <button round ion-button>\n            <ion-icon name="archive"></ion-icon>\n            {{machine.active==true?"Disable":"Enable"}}\n          </button>\n        </ion-item-options>\n      </ion-item-sliding>\n  </ion-list>\n  <button ion-button *ngIf="wizardMode!=null" (click)="onSubmit()">Submit</button>\n</ion-content>\n'/*ion-inline-end:"/Users/agoldma/git/github/TD/front_v2/src/components/tournament-machines/tournament-machines.html"*/,
        })
    ], TournamentMachinesPage);
    return TournamentMachinesPage;
}(__WEBPACK_IMPORTED_MODULE_1__components_tournament_machines_tournament_machines__["a" /* TournamentMachinesComponent */]));

//# sourceMappingURL=tournament-machines.js.map

/***/ })

});
//# sourceMappingURL=7.js.map