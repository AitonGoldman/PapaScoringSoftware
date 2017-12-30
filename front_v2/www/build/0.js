webpackJsonp([0],{

/***/ 684:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
Object.defineProperty(__webpack_exports__, "__esModule", { value: true });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "EventOwnerCreateTournamentPageModule", function() { return EventOwnerCreateTournamentPageModule; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__(1);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1_ionic_angular__ = __webpack_require__(43);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__event_owner_create_tournament__ = __webpack_require__(708);
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};



var EventOwnerCreateTournamentPageModule = (function () {
    function EventOwnerCreateTournamentPageModule() {
    }
    EventOwnerCreateTournamentPageModule = __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["NgModule"])({
            declarations: [
                __WEBPACK_IMPORTED_MODULE_2__event_owner_create_tournament__["a" /* EventOwnerCreateTournamentPage */],
            ],
            imports: [
                __WEBPACK_IMPORTED_MODULE_1_ionic_angular__["f" /* IonicPageModule */].forChild(__WEBPACK_IMPORTED_MODULE_2__event_owner_create_tournament__["a" /* EventOwnerCreateTournamentPage */]),
            ],
        })
    ], EventOwnerCreateTournamentPageModule);
    return EventOwnerCreateTournamentPageModule;
}());

//# sourceMappingURL=event-owner-create-tournament.module.js.map

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

/***/ 699:
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

/***/ 700:
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

/***/ 701:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return EntityFields; });
var EntityFields = (function () {
    function EntityFields(entityType) {
        this.entityType = entityType;
        this.fields = {};
        this.fieldsArray = [];
    }
    EntityFields.prototype.setField = function (fieldName, fieldType, basic, advanced, description) {
        var field = {
            fieldName: fieldName,
            fieldType: fieldType,
            advanced: advanced,
            basic: basic,
            description: description
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

/***/ 702:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return TournamentComponent; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__(1);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__classes_entity_fields__ = __webpack_require__(701);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__pss_page_pss_page__ = __webpack_require__(698);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3__classes_success_summary__ = __webpack_require__(699);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_4__classes_SuccessButton__ = __webpack_require__(700);
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





var tournamentDescriptions = {
    'tournament_name': {
        'short': 'Name of the tournament.',
        'long': 'Name of the tournament (i.e. Classics I, Main A, etc).'
    },
    'multi_division_tournament': {
        'short': 'Multiple divisions.',
        'long': 'Create a tournament with multiple divisions (i.e. Main A, Main B, Main C, etc).'
    },
    'division_count': {
        'short': 'Number of divisions in multi-division tournament',
        'long': 'Number of divisions in multi-division tournament'
    },
    'queuing': {
        'short': 'Queuing',
        'long': 'Enable/Disable queues'
    }, 'manually_set_price': {
        'short': 'Price of single ticket',
        'long': 'Price of single ticket'
    }, 'number_of_qualifiers': {
        'short': 'Top X players will qualify for finals',
        'long': 'Top X players will qualify for finals'
    }
};
/**
 * Generated class for the TournamentComponent component.
 *
 * See https://angular.io/api/core/Component for more info on Angular
 * Components.
 */
var TournamentComponent = (function (_super) {
    __extends(TournamentComponent, _super);
    function TournamentComponent() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.entity = {};
        _this.wizardMode = null;
        return _this;
    }
    TournamentComponent.prototype.ionViewWillLoad = function () {
        this.actionType = this.navParams.get('actionType');
        this.entityFields = new __WEBPACK_IMPORTED_MODULE_1__classes_entity_fields__["a" /* EntityFields */]("tournament");
        this.wizardMode = this.navParams.get('wizardMode');
        this.eventId = this.navParams.get('eventId');
        var wizardEntity = this.navParams.get('wizardEntity');
        if (wizardEntity != null) {
            this.wizardEntity = wizardEntity;
        }
        this.entityFields.setField('tournament_name', 'text', false, true, tournamentDescriptions['tournament_name']);
        this.entityFields.setField('multi_division_tournament', 'boolean', false, true, tournamentDescriptions['multi_division_tournament']);
        this.entityFields.setField('division_count', 'text', false, true, tournamentDescriptions['division_count']);
        this.entityFields.setDependency('division_count', 'multi_division_tournament', true);
        this.entityFields.setField('queuing', 'boolean', false, true, tournamentDescriptions['queuing']);
        this.entityFields.setField('manually_set_price', 'text', false, true, tournamentDescriptions['manually_set_price']);
        this.entityFields.setField('number_of_qualifiers', 'text', false, true, tournamentDescriptions['number_of_qualifiers']);
        if (this.actionType == "edit") {
            //get the entity
        }
    };
    TournamentComponent.prototype.generateCreateTournamentProcessor = function () {
        var _this = this;
        return function (result) {
            if (result == null) {
                return;
            }
            var successTitle = 'Tournament ' + result.data[0].tournament_name + ' has been created.';
            var successSummary = new __WEBPACK_IMPORTED_MODULE_3__classes_success_summary__["a" /* SuccessSummary */](successTitle, null, null);
            var successButton = new __WEBPACK_IMPORTED_MODULE_4__classes_SuccessButton__["a" /* SuccessButton */]('Go Home', _this.destPageAfterSuccess, _this.buildNavParams({}));
            _this.navCtrl.push("SuccessPage", _this.buildNavParams({ 'successSummary': successSummary,
                'successButtons': [successButton] }));
        };
    };
    TournamentComponent.prototype.wizardCreateTournamentSubmit = function () {
        var success_title_string = 'Tournament ' + this.entity['tournament_name'] + ' has been recorded.';
        var success_first_line = 'Click "Proceed" button to proceed.';
        var successSummary = new __WEBPACK_IMPORTED_MODULE_3__classes_success_summary__["a" /* SuccessSummary */](success_title_string, success_first_line, null);
        if (this.wizardEntity != null) {
            this.wizardEntity['tournament'] = this.entity;
        }
        else {
            this.wizardEntity = { tournament: this.entity };
        }
        this.wizardEntity['tournament'] = { tournament: this.entity, division_count: this.entity['division_count'], multi_division_tournament: this.entity['multi_division_tournament'] };
        var successButton = new __WEBPACK_IMPORTED_MODULE_4__classes_SuccessButton__["a" /* SuccessButton */]('Proceed', this.wizardModeNextPage, this.buildNavParams({ wizardMode: this.wizardMode,
            wizardEntity: this.wizardEntity }));
        this.navCtrl.push("SuccessPage", this.buildNavParams({ 'successSummary': successSummary,
            'successButtons': [successButton] }));
    };
    TournamentComponent.prototype.processEntity = function () {
        console.log('process entity...' + this.wizardMode);
        if (this.wizardMode != null) {
            this.wizardCreateTournamentSubmit();
            return;
        }
        if (this.actionType == "create") {
            this.pssApi.createTournament({ tournament: this.entity, division_count: this.entity['division_count'], multi_division_tournament: this.entity['multi_division_tournament'] }, this.eventId)
                .subscribe(this.generateCreateTournamentProcessor());
        }
    };
    TournamentComponent = __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["Component"])({
            selector: 'tournament',template:/*ion-inline-start:"/Users/agoldma/git/github/TD/front_v2/src/components/tournament/tournament.html"*/'<!-- Generated template for the TournamentComponent component -->\n<div>\n  {{text}}\n</div>\n'/*ion-inline-end:"/Users/agoldma/git/github/TD/front_v2/src/components/tournament/tournament.html"*/
        })
    ], TournamentComponent);
    return TournamentComponent;
}(__WEBPACK_IMPORTED_MODULE_2__pss_page_pss_page__["a" /* PssPageComponent */]));

//# sourceMappingURL=tournament.js.map

/***/ }),

/***/ 708:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return EventOwnerCreateTournamentPage; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__(1);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__components_tournament_tournament__ = __webpack_require__(702);
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
 * Generated class for the EventOwnerCreateTournamentPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */
var EventOwnerCreateTournamentPage = (function (_super) {
    __extends(EventOwnerCreateTournamentPage, _super);
    function EventOwnerCreateTournamentPage() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.destPageAfterSuccess = "EventOwnerHomePage";
        _this.wizardModeNextPage = "EventOwnerTournamentMachinesPage";
        return _this;
    }
    EventOwnerCreateTournamentPage.prototype.ionViewDidLoad = function () {
        console.log('ionViewDidLoad EventOwnerCreateTournamentPage');
    };
    EventOwnerCreateTournamentPage = __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["Component"])({
            selector: 'page-event-owner-create-tournament',template:/*ion-inline-start:"/Users/agoldma/git/github/TD/front_v2/src/components/create-edit-entity/create-edit-entity.html"*/'<!-- Generated template for the CreateEditEntityComponent component -->\n<!--<bobo>-->\n<ion-header>\n</ion-header>\n<!--</bobo>-->\n\n\n<ion-content>\n  <form #createEditForm="ngForm">\n    <ion-list>\n      <div margin>\n        <h2>{{actionType| titlecase}} {{entityFields.entityType| titlecase}}</h2>\n      </div>\n\n      <ng-container *ngFor="let entityField of entityFields.getFieldsArray()">\n        <ng-container *ngIf="entityField.dependsOn==null || (entityField.dependsOn && entity[entityField.dependsOn.dependsOn]==entityField.dependsOn.value)">\n        <ion-item-divider color="light" text-wrap>  {{entityField.description.long}} </ion-item-divider>\n        <ng-container *ngIf="entityField.fieldType==\'text\'" >\n          \n          <ion-item>\n            <ion-icon name="md-create" item-start></ion-icon>\n            <ion-input [(ngModel)]="entity[entityField.fieldName]" [name]="entityField.fieldName" type="text" placeholder="input here">\n            </ion-input>    \n          </ion-item>\n        </ng-container>\n        <ng-container *ngIf="entityField.fieldType==\'boolean\'">          \n          <ion-item>\n            <ion-label>{{entityField.description.short}}</ion-label>\n            <ion-toggle [(ngModel)]="entity[entityField.fieldName]" [name]="entityField.fieldName"></ion-toggle>                       \n          </ion-item>\n        </ng-container>\n      </ng-container>        \n      </ng-container>\n    </ion-list>\n    <button [disabled]=\'!createEditForm.valid\' ion-button default (click)="processEntity()">Apply</button>\n  </form>  \n</ion-content>\n\n'/*ion-inline-end:"/Users/agoldma/git/github/TD/front_v2/src/components/create-edit-entity/create-edit-entity.html"*/
        })
    ], EventOwnerCreateTournamentPage);
    return EventOwnerCreateTournamentPage;
}(__WEBPACK_IMPORTED_MODULE_1__components_tournament_tournament__["a" /* TournamentComponent */]));

//# sourceMappingURL=event-owner-create-tournament.js.map

/***/ })

});
//# sourceMappingURL=0.js.map