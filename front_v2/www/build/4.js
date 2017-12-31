webpackJsonp([4],{

/***/ 690:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
Object.defineProperty(__webpack_exports__, "__esModule", { value: true });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "EditEventPageModule", function() { return EditEventPageModule; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__(1);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1_ionic_angular__ = __webpack_require__(43);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__edit_event__ = __webpack_require__(720);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3_angular2_image_upload__ = __webpack_require__(352);
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};




var EditEventPageModule = (function () {
    function EditEventPageModule() {
    }
    EditEventPageModule = __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["NgModule"])({
            declarations: [
                __WEBPACK_IMPORTED_MODULE_2__edit_event__["a" /* EditEventPage */],
            ],
            imports: [
                __WEBPACK_IMPORTED_MODULE_1_ionic_angular__["f" /* IonicPageModule */].forChild(__WEBPACK_IMPORTED_MODULE_2__edit_event__["a" /* EditEventPage */]),
                __WEBPACK_IMPORTED_MODULE_3_angular2_image_upload__["a" /* ImageUploadModule */].forRoot()
            ],
        })
    ], EditEventPageModule);
    return EditEventPageModule;
}());

//# sourceMappingURL=edit-event.module.js.map

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

/***/ 715:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return EventComponent; });
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





/**
 * Generated class for the EventComponent component.
 *
 * See https://angular.io/api/core/Component for more info on Angular
 * Components.
 */
var eventDescriptions = {
    'name': {
        'short': 'Name of the event.',
        'long': 'Name of the event (i.e. PAPA 25, INDISC 2018, etc).',
    },
    'number_unused_tickets_allowed': {
        'short': 'Number of unused tickets allowed.',
        'long': 'Number of unused tickets a player is allowed to have.  This takes into account any tickets the player is currently using.',
    },
    'stripe_api_key': {
        'short': 'Stripe Api key.',
        'long': 'The private Stripe Api key.',
    },
    'stripe_public_key': {
        'short': 'Stripe public Api key.',
        'long': 'The public Stripe Api Key.',
    },
    'force_ifpa_lookup': {
        'short': 'Force IFPA ranking lookup.',
        'long': 'When registering player for events, force an IFPA ranking lookup.  This ranking will be used for IFPA ranking restrictions.',
    }
};
var EventComponent = (function (_super) {
    __extends(EventComponent, _super);
    function EventComponent() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.entity = {};
        _this.wizardMode = null;
        _this.advanced = false;
        _this.entityFieldsArray = null;
        return _this;
    }
    EventComponent.prototype.ionViewWillLoad = function () {
        this.actionType = this.navParams.get('actionType');
        this.eventId = this.navParams.get('eventId');
        this.wizardMode = this.navParams.get('wizardMode');
        this.entityFields = new __WEBPACK_IMPORTED_MODULE_1__classes_entity_fields__["a" /* EntityFields */]("event");
        this.entityFields.setField('name', 'text', true, false, eventDescriptions['name']);
        this.entityFields.setField('number_unused_tickets_allowed', 'text', true, false, eventDescriptions['number_unused_tickets_allowed']);
        this.entityFields.setField('stripe_api_key', 'text', false, true, eventDescriptions['stripe_api_key']);
        this.entityFields.setField('stripe_public_key', 'text', false, true, eventDescriptions['stripe_public_key']);
        this.entityFields.setField('force_ifpa_lookup', 'boolean', false, true, eventDescriptions['force_ifpa_lookup']);
        this.entityFieldsArray = this.entityFields.getFieldsArray(this.advanced);
        if (this.actionType == "edit") {
            this.pssApi.getEvent(this.eventId)
                .subscribe(this.generateGetEventProcessor());
        }
    };
    EventComponent.prototype.onAdvancedChange = function () {
        this.entityFieldsArray = this.entityFields.getFieldsArray(this.advanced);
    };
    EventComponent.prototype.generateGetEventProcessor = function () {
        var _this = this;
        return function (result) {
            if (result == null) {
                return;
            }
            _this.entity = result.data;
        };
    };
    EventComponent.prototype.generateEditEventProcessor = function () {
        var _this = this;
        return function (result) {
            if (result == null) {
                return;
            }
            var success_title_string = 'Event ' + result.data.name + ' has been edited.';
            var successSummary = new __WEBPACK_IMPORTED_MODULE_3__classes_success_summary__["a" /* SuccessSummary */](success_title_string, null, null);
            var successButton = new __WEBPACK_IMPORTED_MODULE_4__classes_SuccessButton__["a" /* SuccessButton */]('Go Home', _this.destPageAfterSuccess, _this.buildNavParams({ wizardMode: _this.wizardMode }));
            _this.navCtrl.push("SuccessPage", _this.buildNavParams({ 'successSummary': successSummary,
                'successButtons': [successButton] }));
        };
    };
    EventComponent.prototype.generateCreateEventProcessor = function () {
        var _this = this;
        return function (result) {
            if (result == null) {
                return;
            }
            var success_title_string = 'Event ' + result.data.name + ' has been created.';
            var successSummary = new __WEBPACK_IMPORTED_MODULE_3__classes_success_summary__["a" /* SuccessSummary */](success_title_string, null, null);
            var successButton = new __WEBPACK_IMPORTED_MODULE_4__classes_SuccessButton__["a" /* SuccessButton */]('Go Home', _this.destPageAfterSuccess, _this.buildNavParams({ wizardMode: _this.wizardMode }));
            _this.navCtrl.push("SuccessPage", _this.buildNavParams({ 'successSummary': successSummary,
                'successButtons': [successButton] }));
        };
    };
    EventComponent.prototype.wizardCreateEventSubmit = function () {
        var success_title_string = 'Event ' + this.entity['name'] + ' has been recorded.';
        var success_first_line = 'Click "Proceed" button to proceed.';
        var successSummary = new __WEBPACK_IMPORTED_MODULE_3__classes_success_summary__["a" /* SuccessSummary */](success_title_string, success_first_line, null);
        var successButton = new __WEBPACK_IMPORTED_MODULE_4__classes_SuccessButton__["a" /* SuccessButton */]('Proceed', this.wizardModeNextPage, this.buildNavParams({ wizardMode: this.wizardMode,
            wizardEntity: { 'event': this.entity },
            actionType: 'create' }));
        this.navCtrl.push("SuccessPage", this.buildNavParams({ 'successSummary': successSummary,
            'successButtons': [successButton] }));
    };
    EventComponent.prototype.processEntity = function () {
        console.log('process entity...' + this.wizardMode);
        if (this.wizardMode != null) {
            this.wizardCreateEventSubmit();
            return;
        }
        if (this.actionType == "create") {
            this.pssApi.createEvent(this.entity)
                .subscribe(this.generateCreateEventProcessor());
        }
        if (this.actionType == "edit") {
            this.pssApi.editEvent(this.entity)
                .subscribe(this.generateEditEventProcessor());
        }
    };
    //FIXME : needs to be shared between tourney and event
    EventComponent.prototype.onUploadFinished = function (event) {
        this.entity.has_pic = true;
        this.entity.img_file = JSON.parse(event.serverResponse._body).data;
    };
    EventComponent = __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["Component"])({
            selector: 'event',template:/*ion-inline-start:"/Users/agoldma/git/github/TD/front_v2/src/components/event/event.html"*/'<!-- Generated template for the EventComponent component -->\n<div>\n  {{text}}\n</div>\n'/*ion-inline-end:"/Users/agoldma/git/github/TD/front_v2/src/components/event/event.html"*/
        })
    ], EventComponent);
    return EventComponent;
}(__WEBPACK_IMPORTED_MODULE_2__pss_page_pss_page__["a" /* PssPageComponent */]));

//# sourceMappingURL=event.js.map

/***/ }),

/***/ 720:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return EditEventPage; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__(1);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__components_event_event__ = __webpack_require__(715);
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
 * Generated class for the EditEventPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */
var EditEventPage = (function (_super) {
    __extends(EditEventPage, _super);
    function EditEventPage() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.destPageAfterSuccess = "EventOwnerHomePage";
        return _this;
    }
    EditEventPage.prototype.ionViewDidLoad = function () {
        console.log('ionViewDidLoad EditEventPage');
    };
    EditEventPage = __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["Component"])({
            selector: 'page-edit-event',template:/*ion-inline-start:"/Users/agoldma/git/github/TD/front_v2/src/components/create-edit-entity/create-edit-entity.html"*/'<!-- Generated template for the CreateEditEntityComponent component -->\n<ion-header>\n  <ion-navbar >\n    <ion-title></ion-title>\n    <ion-buttons end hideWhen="mobile">\n      <button icon-only ion-button [navPush]="\'EventSelectPage\'">Switch Events</button>    \n      <button icon-only ion-button [navPush]="destPageAfterSuccess" [navParams]="buildNavParams({})">Home</button>    \n    </ion-buttons>\n  </ion-navbar>\n</ion-header>\n\n\n<ion-content>\n  <form #createEditForm="ngForm">\n    <ion-list>\n      <div margin>\n        <h2>{{actionType| titlecase}} {{entityFields.entityType| titlecase}}</h2>\n      </div>\n      <ion-item>\n        <ion-label>Advanced Settings</ion-label>\n        <ion-toggle (ionChange)="onAdvancedChange()" name="myadvanced" [(ngModel)]="advanced"></ion-toggle>\n      </ion-item>\n\n      <ng-container *ngFor="let entityField of entityFieldsArray">\n        <ng-container *ngIf="entityField.dependsOn==null || (entityField.dependsOn && entity[entityField.dependsOn.dependsOn]==entityField.dependsOn.value)">\n        <ion-item-divider color="light" text-wrap>  {{entityField.description.long}} </ion-item-divider>\n        <ng-container *ngIf="entityField.fieldType==\'text\'" >\n          \n          <ion-item>\n            <ion-icon name="md-create" item-start></ion-icon>\n            <ion-input [(ngModel)]="entity[entityField.fieldName]" [name]="entityField.fieldName" type="text" placeholder="input here">\n            </ion-input>    \n          </ion-item>\n        </ng-container>\n        <ng-container *ngIf="entityField.fieldType==\'boolean\'">          \n          <ion-item>\n            <ion-label>{{entityField.description.short}}</ion-label>\n            <ion-toggle [(ngModel)]="entity[entityField.fieldName]" [name]="entityField.fieldName"></ion-toggle>                       \n          </ion-item>\n        </ng-container>\n      </ng-container>        \n      </ng-container>\n      <ng-container *ngIf="entity.img_url!=null">\n        <ion-item-divider color="light" text-wrap> Current {{entityType}} image </ion-item-divider>\n        <ion-item>\n          <ion-avatar item-start *ngIf="entity.img_url!=null">\n            <img [src]="entity.img_url">\n          </ion-avatar>                \n        </ion-item>\n      </ng-container>\n      \n      <ion-item-divider color="light" text-wrap>Upload an image that will be used as the event icon </ion-item-divider>\n      <ion-item>\n        <image-upload (uploadFinished)="onUploadFinished($event)" url="http://0.0.0.0:8000/media_upload"></image-upload>\n      </ion-item>\n    </ion-list>    \n    <button [disabled]=\'!createEditForm.valid\' ion-button default (click)="processEntity()">Apply</button>\n  </form>  \n</ion-content>\n\n'/*ion-inline-end:"/Users/agoldma/git/github/TD/front_v2/src/components/create-edit-entity/create-edit-entity.html"*/,
        })
    ], EditEventPage);
    return EditEventPage;
}(__WEBPACK_IMPORTED_MODULE_1__components_event_event__["a" /* EventComponent */]));

//# sourceMappingURL=edit-event.js.map

/***/ })

});
//# sourceMappingURL=4.js.map