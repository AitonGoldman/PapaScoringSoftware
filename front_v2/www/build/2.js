webpackJsonp([2],{

/***/ 691:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
Object.defineProperty(__webpack_exports__, "__esModule", { value: true });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "EditTournamentPageModule", function() { return EditTournamentPageModule; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__(1);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1_ionic_angular__ = __webpack_require__(43);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__edit_tournament__ = __webpack_require__(721);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3_angular2_image_upload__ = __webpack_require__(352);
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};




var EditTournamentPageModule = (function () {
    function EditTournamentPageModule() {
    }
    EditTournamentPageModule = __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["NgModule"])({
            declarations: [
                __WEBPACK_IMPORTED_MODULE_2__edit_tournament__["a" /* EditTournamentPage */],
            ],
            imports: [
                __WEBPACK_IMPORTED_MODULE_1_ionic_angular__["f" /* IonicPageModule */].forChild(__WEBPACK_IMPORTED_MODULE_2__edit_tournament__["a" /* EditTournamentPage */]),
                __WEBPACK_IMPORTED_MODULE_3_angular2_image_upload__["a" /* ImageUploadModule */].forRoot()
            ],
        })
    ], EditTournamentPageModule);
    return EditTournamentPageModule;
}());

//# sourceMappingURL=edit-tournament.module.js.map

/***/ }),

/***/ 710:
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

/***/ 711:
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

/***/ 712:
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

/***/ 713:
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
    EntityFields.prototype.getFieldsArray = function (advanced) {
        var fieldsArray = [];
        for (var i in this.fields) {
            fieldsArray.push(this.fields[i]);
        }
        if (advanced == false) {
            return fieldsArray.filter(function (field) { return field.basic == true; });
        }
        else {
            return fieldsArray;
        }
    };
    return EntityFields;
}());

//# sourceMappingURL=entity-fields.js.map

/***/ }),

/***/ 714:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return TournamentComponent; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__(1);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__classes_entity_fields__ = __webpack_require__(713);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__pss_page_pss_page__ = __webpack_require__(710);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3__classes_success_summary__ = __webpack_require__(711);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_4__classes_SuccessButton__ = __webpack_require__(712);
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
        _this.entityFieldsArray = null;
        _this.advanced = false;
        return _this;
    }
    TournamentComponent.prototype.ionViewWillLoad = function () {
        this.actionType = this.navParams.get('actionType');
        this.entityFields = new __WEBPACK_IMPORTED_MODULE_1__classes_entity_fields__["a" /* EntityFields */]("tournament");
        this.wizardMode = this.navParams.get('wizardMode');
        this.eventId = this.navParams.get('eventId');
        this.tournamentId = this.navParams.get('tournamentId');
        var wizardEntity = this.navParams.get('wizardEntity');
        if (wizardEntity != null) {
            this.wizardEntity = wizardEntity;
        }
        this.entityFields.setField('tournament_name', 'text', true, false, tournamentDescriptions['tournament_name']);
        this.entityFields.setField('multi_division_tournament', 'boolean', true, false, tournamentDescriptions['multi_division_tournament']);
        this.entityFields.setField('division_count', 'text', true, false, tournamentDescriptions['division_count']);
        this.entityFields.setDependency('division_count', 'multi_division_tournament', true);
        this.entityFields.setField('queuing', 'boolean', true, false, tournamentDescriptions['queuing']);
        this.entityFields.setField('manually_set_price', 'text', true, false, tournamentDescriptions['manually_set_price']);
        this.entityFields.setField('number_of_qualifiers', 'text', true, false, tournamentDescriptions['number_of_qualifiers']);
        this.entityFieldsArray = this.entityFields.getFieldsArray(this.advanced);
        if (this.actionType == "edit") {
            this.pssApi.getTournament(this.eventId, this.tournamentId)
                .subscribe(this.generateGetTournamentProcessor());
        }
    };
    TournamentComponent.prototype.generateGetTournamentProcessor = function () {
        var _this = this;
        return function (result) {
            if (result == null) {
                return;
            }
            _this.entity = result.data;
        };
    };
    TournamentComponent.prototype.onAdvancedChange = function () {
        this.entityFieldsArray = this.entityFields.getFieldsArray(this.advanced);
    };
    TournamentComponent.prototype.generateEditTournamentProcessor = function () {
        var _this = this;
        return function (result) {
            if (result == null) {
                return;
            }
            var success_title_string = 'Tournament ' + result.data.tournament_name + ' has been edited.';
            var successSummary = new __WEBPACK_IMPORTED_MODULE_3__classes_success_summary__["a" /* SuccessSummary */](success_title_string, null, null);
            var successButton = new __WEBPACK_IMPORTED_MODULE_4__classes_SuccessButton__["a" /* SuccessButton */]('Go Home', _this.destPageAfterSuccess, _this.buildNavParams({ wizardMode: _this.wizardMode }));
            _this.navCtrl.push("SuccessPage", _this.buildNavParams({ 'successSummary': successSummary,
                'successButtons': [successButton] }));
        };
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
        if (this.actionType == "edit") {
            this.pssApi.editTournament(this.entity, this.eventId)
                .subscribe(this.generateEditTournamentProcessor());
        }
    };
    TournamentComponent.prototype.onUploadFinished = function (event) {
        this.entity.has_pic = true;
        this.entity.img_file = JSON.parse(event.serverResponse._body).data;
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

/***/ 721:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return EditTournamentPage; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__(1);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__components_tournament_tournament__ = __webpack_require__(714);
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
 * Generated class for the EditTournamentPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */
var EditTournamentPage = (function (_super) {
    __extends(EditTournamentPage, _super);
    function EditTournamentPage() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.destPageAfterSuccess = "TournamentDirectorHomePage";
        _this.entityType = "tournament";
        return _this;
    }
    EditTournamentPage.prototype.ionViewDidLoad = function () {
        console.log('ionViewDidLoad EditTournamentPage');
    };
    EditTournamentPage = __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["Component"])({
            selector: 'page-edit-tournament',template:/*ion-inline-start:"/Users/agoldma/git/github/TD/front_v2/src/components/create-edit-entity/create-edit-entity.html"*/'<!-- Generated template for the CreateEditEntityComponent component -->\n<ion-header>\n  <ion-navbar >\n    <ion-title></ion-title>\n    <ion-buttons end hideWhen="mobile">\n      <button icon-only ion-button [navPush]="\'EventSelectPage\'">Switch Events</button>    \n      <button icon-only ion-button [navPush]="destPageAfterSuccess" [navParams]="buildNavParams({})">Home</button>    \n    </ion-buttons>\n  </ion-navbar>\n</ion-header>\n\n\n<ion-content>\n  <form #createEditForm="ngForm">\n    <ion-list>\n      <div margin>\n        <h2>{{actionType| titlecase}} {{entityFields.entityType| titlecase}}</h2>\n      </div>\n      <ion-item>\n        <ion-label>Advanced Settings</ion-label>\n        <ion-toggle (ionChange)="onAdvancedChange()" name="myadvanced" [(ngModel)]="advanced"></ion-toggle>\n      </ion-item>\n\n      <ng-container *ngFor="let entityField of entityFieldsArray">\n        <ng-container *ngIf="entityField.dependsOn==null || (entityField.dependsOn && entity[entityField.dependsOn.dependsOn]==entityField.dependsOn.value)">\n        <ion-item-divider color="light" text-wrap>  {{entityField.description.long}} </ion-item-divider>\n        <ng-container *ngIf="entityField.fieldType==\'text\'" >\n          \n          <ion-item>\n            <ion-icon name="md-create" item-start></ion-icon>\n            <ion-input [(ngModel)]="entity[entityField.fieldName]" [name]="entityField.fieldName" type="text" placeholder="input here">\n            </ion-input>    \n          </ion-item>\n        </ng-container>\n        <ng-container *ngIf="entityField.fieldType==\'boolean\'">          \n          <ion-item>\n            <ion-label>{{entityField.description.short}}</ion-label>\n            <ion-toggle [(ngModel)]="entity[entityField.fieldName]" [name]="entityField.fieldName"></ion-toggle>                       \n          </ion-item>\n        </ng-container>\n      </ng-container>        \n      </ng-container>\n      <ng-container *ngIf="entity.img_url!=null">\n        <ion-item-divider color="light" text-wrap> Current {{entityType}} image </ion-item-divider>\n        <ion-item>\n          <ion-avatar item-start *ngIf="entity.img_url!=null">\n            <img [src]="entity.img_url">\n          </ion-avatar>                \n        </ion-item>\n      </ng-container>\n      \n      <ion-item-divider color="light" text-wrap>Upload an image that will be used as the event icon </ion-item-divider>\n      <ion-item>\n        <image-upload (uploadFinished)="onUploadFinished($event)" url="http://0.0.0.0:8000/media_upload"></image-upload>\n      </ion-item>\n    </ion-list>    \n    <button [disabled]=\'!createEditForm.valid\' ion-button default (click)="processEntity()">Apply</button>\n  </form>  \n</ion-content>\n\n'/*ion-inline-end:"/Users/agoldma/git/github/TD/front_v2/src/components/create-edit-entity/create-edit-entity.html"*/,
        })
    ], EditTournamentPage);
    return EditTournamentPage;
}(__WEBPACK_IMPORTED_MODULE_1__components_tournament_tournament__["a" /* TournamentComponent */]));

//# sourceMappingURL=edit-tournament.js.map

/***/ })

});
//# sourceMappingURL=2.js.map