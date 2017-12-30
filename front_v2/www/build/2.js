webpackJsonp([2],{

/***/ 676:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
Object.defineProperty(__webpack_exports__, "__esModule", { value: true });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "CreateEventPageModule", function() { return CreateEventPageModule; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__(1);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1_ionic_angular__ = __webpack_require__(44);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__create_event__ = __webpack_require__(697);
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};



var CreateEventPageModule = (function () {
    function CreateEventPageModule() {
    }
    CreateEventPageModule = __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["I" /* NgModule */])({
            declarations: [
                __WEBPACK_IMPORTED_MODULE_2__create_event__["a" /* CreateEventPage */],
            ],
            imports: [
                __WEBPACK_IMPORTED_MODULE_1_ionic_angular__["f" /* IonicPageModule */].forChild(__WEBPACK_IMPORTED_MODULE_2__create_event__["a" /* CreateEventPage */]),
            ],
        })
    ], CreateEventPageModule);
    return CreateEventPageModule;
}());

//# sourceMappingURL=create-event.module.js.map

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

/***/ 692:
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

/***/ 693:
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

/***/ 694:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return CreateEditEntityComponent; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__(1);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__classes_entity_fields__ = __webpack_require__(695);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__pss_page_pss_page__ = __webpack_require__(691);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3__classes_success_summary__ = __webpack_require__(692);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_4__classes_SuccessButton__ = __webpack_require__(693);
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
 * Generated class for the CreateEditEntityComponent component.
 *
 * See https://angular.io/api/core/Component for more info on Angular
 * Components.
 */
var entityDescriptions = {
    'event': {
        'name': {
            'short': 'Name of the event.',
            'long': 'Name of the event (i.e. PAPA 25, INDISC 2018, etc).',
            'type': 'text'
        },
        'number_unused_tickets_allowed': {
            'short': 'Number of unused tickets allowed.',
            'long': 'Number of unused tickets a player is allowed to have.  This takes into account any tickets the player is currently using.',
            'type': 'text'
        }
    },
    'tournament': {
        'tournament_name': {
            'short': 'Name of the tournament.',
            'long': 'Name of the tournament (i.e. Classics I, Main A, etc).',
            'type': 'text'
        },
        'multi_division_tournament': {
            'short': 'Multiple divisions.',
            'long': 'Create a tournament with multiple divisions (i.e. Main A, Main B, Main C, etc).',
            'type': 'boolean'
        },
        'division_count': {
            'short': 'Number of divisions in multi-division tournament',
            'long': 'Number of divisions in multi-division tournament',
            'type': 'text'
        },
        'queuing': {
            'short': 'Queuing',
            'long': 'Enable/Disable queues',
            'type': 'boolean'
        }, 'manually_set_price': {
            'short': 'Price of single ticket',
            'long': 'Price of single ticket',
            'type': 'text'
        }, 'number_of_qualifiers': {
            'short': 'Top X players will qualify for finals',
            'long': 'Top X players will qualify for finals',
            'type': 'text'
        }
    }
};
var CreateEditEntityComponent = (function (_super) {
    __extends(CreateEditEntityComponent, _super);
    function CreateEditEntityComponent() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.entityDescriptions = entityDescriptions;
        _this.entity = {};
        _this.destPageAfterSuccess = 'TournamentDirectorHomePage';
        _this.wizardMode = false;
        _this.wizardModeStack = null;
        _this.wizardModeIndex = null;
        return _this;
    }
    CreateEditEntityComponent.prototype.ionViewWillLoad = function () {
        console.log('hi there');
        //this.entityType=this.navParams.get('entityType');
        this.actionType = this.navParams.get('actionType');
        this.eventId = this.navParams.get('eventId');
        this.entityFields = new __WEBPACK_IMPORTED_MODULE_1__classes_entity_fields__["a" /* EntityFields */](this.entityType);
        this.wizardMode = this.navParams.get('wizardMode');
        this.wizardModeIndex = this.navParams.get('wizardModeIndex');
        this.wizardModeStack = this.navParams.get('wizardModeStack');
        console.log('in create/edit....' + this.eventId);
        if (this.entityType == "event") {
            this.entityFields.setField('name', 'text', false, true);
            this.entityFields.setField('number_unused_tickets_allowed', 'text', false, true);
            if (this.actionType == "edit") {
                //get the entity
            }
        }
        if (this.entityType == "tournament") {
            console.log('in tournament create....');
            this.entityFields.setField('tournament_name', 'text', false, true);
            this.entityFields.setField('multi_division_tournament', 'boolean', false, true);
            this.entityFields.setField('division_count', 'text', false, true);
            this.entityFields.setDependency('division_count', 'multi_division_tournament', true);
            this.entityFields.setField('queuing', 'boolean', false, true);
            this.entityFields.setField('manually_set_price', 'text', false, true);
            this.entityFields.setField('number_of_qualifiers', 'text', false, true);
            if (this.actionType == "edit") {
                //get the entity
            }
        }
        console.log('ionViewDidLoad CreateEditEntity');
    };
    CreateEditEntityComponent.prototype.generateCreateEventProcessor = function () {
        var _this = this;
        return function (result) {
            if (result == null) {
                return;
            }
            var successSummary = new __WEBPACK_IMPORTED_MODULE_3__classes_success_summary__["a" /* SuccessSummary */]('Event ' + result.data.name + ' has been created.', null, null);
            var successButton = new __WEBPACK_IMPORTED_MODULE_4__classes_SuccessButton__["a" /* SuccessButton */]('Go Home', "EventOwnerHomePage", _this.buildNavParams({}));
            _this.navCtrl.push("SuccessPage", _this.buildNavParams({ 'successSummary': successSummary,
                'successButtons': [successButton] }));
        };
    };
    CreateEditEntityComponent.prototype.generateCreateTournamentProcessor = function () {
        var _this = this;
        return function (result) {
            if (result == null) {
                return;
            }
            console.log('in create tourney processor ...');
            var successSummary = new __WEBPACK_IMPORTED_MODULE_3__classes_success_summary__["a" /* SuccessSummary */]('Tournament ' + result.data[0].tournament_name + ' has been created.', null, null);
            var successButton = new __WEBPACK_IMPORTED_MODULE_4__classes_SuccessButton__["a" /* SuccessButton */]('Go Home', _this.destPageAfterSuccess, _this.buildNavParams({}));
            _this.navCtrl.push("SuccessPage", _this.buildNavParams({ 'successSummary': successSummary,
                'successButtons': [successButton] }));
        };
    };
    CreateEditEntityComponent.prototype.processEntity = function () {
        if (this.entityType == "event") {
            if (this.actionType == "create") {
                console.log('in process entity....');
                console.log(this.entity);
                if (this.wizardMode != true) {
                    this.pssApi.createEvent(this.entity)
                        .subscribe(this.generateCreateEventProcessor());
                }
            }
        }
        if (this.entityType == "tournament") {
            if (this.actionType == "create") {
                console.log('in process entity....');
                this.entity['event_id'] = this.eventId;
                if (this.wizardMode != true) {
                    this.pssApi.createTournament({ tournament: this.entity, division_count: this.entity['division_count'], multi_division_tournament: this.entity['multi_division_tournament'] }, this.eventId)
                        .subscribe(this.generateCreateTournamentProcessor());
                }
            }
        }
        if (this.wizardMode == true) {
        }
    };
    CreateEditEntityComponent = __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["m" /* Component */])({
            selector: 'create-edit-entity',template:/*ion-inline-start:"/Users/agoldma/git/github/TD/front_v2/src/components/create-edit-entity/create-edit-entity.html"*/'<!-- Generated template for the CreateEditEntityComponent component -->\n<!--<bobo>-->\n<ion-header>\n  <ion-navbar>  \n    <ion-title showWhen=\'mobile\'>\n      {{title}}\n    </ion-title>    \n    <ion-title hideWhen=\'mobile\'>Pss</ion-title>\n    <ion-buttons end hideWhen=\'mobile\'>\n      <button icon-only ion-button [navPush]="eventAuth.isEventUserLoggedIn(eventId)? \'LogoutPage\' : \'LoginPage\'" [navParams]="buildNavParams({})" >{{eventAuth.isEventUserLoggedIn(eventId)? "Logout" : "Login"}}</button>\n      <button icon-only ion-button [navPush]="\'EventSelectPage\'">Switch Events</button>    \n      <button [navPush]="\'ResultsPage\'" icon-only ion-button>Results</button>\n      <button icon-only ion-button>Queues</button>\n      <button *ngIf="eventAuth.getRoleName(eventId)" icon-only ion-button [navPush]="getHomePageString()" [navParams]="buildNavParams({})">{{eventAuth.getRoleName(eventId)}}</button>\n    </ion-buttons>\n  </ion-navbar>\n</ion-header>\n<!--</bobo>-->\n\n<ion-content>\n  <form #createEditForm="ngForm">\n    <ion-list>\n      <div margin>\n        <h2>{{actionType| titlecase}} {{entityFields.entityType| titlecase}}</h2>\n      </div>\n\n      <ng-container *ngFor="let entityField of entityFields.getFieldsArray()">\n        <ng-container *ngIf="entityField.dependsOn==null || (entityField.dependsOn && entity[entityField.dependsOn.dependsOn]==entityField.dependsOn.value)">\n        <ion-item-divider color="light" text-wrap>  {{entityDescriptions[entityFields.entityType][entityField.fieldName].long}} </ion-item-divider>\n        <ng-container *ngIf="entityField.fieldType==\'text\'" >\n          \n          <ion-item>\n            <ion-icon name="md-create" item-start></ion-icon>\n            <ion-input [(ngModel)]="entity[entityField.fieldName]" [name]="entityField.fieldName" type="text" placeholder="input here">\n            </ion-input>    \n          </ion-item>\n        </ng-container>\n        <ng-container *ngIf="entityField.fieldType==\'boolean\'">          \n          <ion-item>\n            <ion-label>{{entityDescriptions[entityFields.entityType][entityField.fieldName].short}}</ion-label>\n            <ion-toggle [(ngModel)]="entity[entityField.fieldName]" [name]="entityField.fieldName"></ion-toggle>                       \n          </ion-item>\n        </ng-container>\n      </ng-container>        \n      </ng-container>\n    </ion-list>\n    <button [disabled]=\'!createEditForm.valid\' ion-button default (click)="processEntity()">Apply</button>\n  </form>  \n</ion-content>\n\n'/*ion-inline-end:"/Users/agoldma/git/github/TD/front_v2/src/components/create-edit-entity/create-edit-entity.html"*/
        })
    ], CreateEditEntityComponent);
    return CreateEditEntityComponent;
}(__WEBPACK_IMPORTED_MODULE_2__pss_page_pss_page__["a" /* PssPageComponent */]));

//# sourceMappingURL=create-edit-entity.js.map

/***/ }),

/***/ 695:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return EntityFields; });
var EntityFields = (function () {
    function EntityFields(entityType) {
        this.entityType = entityType;
        this.fields = {};
        this.fieldsArray = [];
    }
    EntityFields.prototype.setField = function (fieldName, fieldType, basic, advanced) {
        var field = {
            fieldName: fieldName,
            fieldType: fieldType,
            advanced: advanced,
            basic: basic
        };
        this.fields[fieldName] = field;
        //this.fieldsArray.push(field);
    };
    EntityFields.prototype.setDependency = function (fieldName, dependsOn, value) {
        this.fields[fieldName].dependsOn = {
            dependsOn: dependsOn,
            value: value
        };
    };
    EntityFields.prototype.getFields = function () {
        return this.fields;
    };
    EntityFields.prototype.getFieldsArray = function () {
        var fieldsArray = [];
        for (var i in this.fields) {
            fieldsArray.push(this.fields[i]);
        }
        return fieldsArray;
    };
    return EntityFields;
}());

//# sourceMappingURL=entity-fields.js.map

/***/ }),

/***/ 697:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return CreateEventPage; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__(1);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__components_create_edit_entity_create_edit_entity__ = __webpack_require__(694);
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
 * Generated class for the CreateEventPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */
var CreateEventPage = (function (_super) {
    __extends(CreateEventPage, _super);
    function CreateEventPage() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.entityType = 'event';
        return _this;
    }
    CreateEventPage.prototype.ionViewDidLoad = function () {
        console.log('ionViewDidLoad CreateEventPage');
    };
    CreateEventPage = __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["m" /* Component */])({
            selector: 'page-create-event',template:/*ion-inline-start:"/Users/agoldma/git/github/TD/front_v2/src/components/create-edit-entity/create-edit-entity.html"*/'<!-- Generated template for the CreateEditEntityComponent component -->\n<!--<bobo>-->\n<ion-header>\n  <ion-navbar>  \n    <ion-title showWhen=\'mobile\'>\n      {{title}}\n    </ion-title>    \n    <ion-title hideWhen=\'mobile\'>Pss</ion-title>\n    <ion-buttons end hideWhen=\'mobile\'>\n      <button icon-only ion-button [navPush]="eventAuth.isEventUserLoggedIn(eventId)? \'LogoutPage\' : \'LoginPage\'" [navParams]="buildNavParams({})" >{{eventAuth.isEventUserLoggedIn(eventId)? "Logout" : "Login"}}</button>\n      <button icon-only ion-button [navPush]="\'EventSelectPage\'">Switch Events</button>    \n      <button [navPush]="\'ResultsPage\'" icon-only ion-button>Results</button>\n      <button icon-only ion-button>Queues</button>\n      <button *ngIf="eventAuth.getRoleName(eventId)" icon-only ion-button [navPush]="getHomePageString()" [navParams]="buildNavParams({})">{{eventAuth.getRoleName(eventId)}}</button>\n    </ion-buttons>\n  </ion-navbar>\n</ion-header>\n<!--</bobo>-->\n\n<ion-content>\n  <form #createEditForm="ngForm">\n    <ion-list>\n      <div margin>\n        <h2>{{actionType| titlecase}} {{entityFields.entityType| titlecase}}</h2>\n      </div>\n\n      <ng-container *ngFor="let entityField of entityFields.getFieldsArray()">\n        <ng-container *ngIf="entityField.dependsOn==null || (entityField.dependsOn && entity[entityField.dependsOn.dependsOn]==entityField.dependsOn.value)">\n        <ion-item-divider color="light" text-wrap>  {{entityDescriptions[entityFields.entityType][entityField.fieldName].long}} </ion-item-divider>\n        <ng-container *ngIf="entityField.fieldType==\'text\'" >\n          \n          <ion-item>\n            <ion-icon name="md-create" item-start></ion-icon>\n            <ion-input [(ngModel)]="entity[entityField.fieldName]" [name]="entityField.fieldName" type="text" placeholder="input here">\n            </ion-input>    \n          </ion-item>\n        </ng-container>\n        <ng-container *ngIf="entityField.fieldType==\'boolean\'">          \n          <ion-item>\n            <ion-label>{{entityDescriptions[entityFields.entityType][entityField.fieldName].short}}</ion-label>\n            <ion-toggle [(ngModel)]="entity[entityField.fieldName]" [name]="entityField.fieldName"></ion-toggle>                       \n          </ion-item>\n        </ng-container>\n      </ng-container>        \n      </ng-container>\n    </ion-list>\n    <button [disabled]=\'!createEditForm.valid\' ion-button default (click)="processEntity()">Apply</button>\n  </form>  \n</ion-content>\n\n'/*ion-inline-end:"/Users/agoldma/git/github/TD/front_v2/src/components/create-edit-entity/create-edit-entity.html"*/,
        })
    ], CreateEventPage);
    return CreateEventPage;
}(__WEBPACK_IMPORTED_MODULE_1__components_create_edit_entity_create_edit_entity__["a" /* CreateEditEntityComponent */]));

//# sourceMappingURL=create-event.js.map

/***/ })

});
//# sourceMappingURL=2.js.map