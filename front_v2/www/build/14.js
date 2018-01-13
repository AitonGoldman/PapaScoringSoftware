webpackJsonp([14],{

/***/ 715:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
Object.defineProperty(__webpack_exports__, "__esModule", { value: true });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "PlayerInfoPageModule", function() { return PlayerInfoPageModule; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__(1);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1_ionic_angular__ = __webpack_require__(34);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__player_info__ = __webpack_require__(751);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3_ionic2_auto_complete__ = __webpack_require__(358);
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};




//import { SimpleNotificationsModule } from 'angular2-notifications';
//import { ToastModule } from 'ng2-toastr/ng2-toastr';
var PlayerInfoPageModule = (function () {
    function PlayerInfoPageModule() {
    }
    PlayerInfoPageModule = __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["NgModule"])({
            declarations: [
                __WEBPACK_IMPORTED_MODULE_2__player_info__["a" /* PlayerInfoPage */],
            ],
            imports: [
                __WEBPACK_IMPORTED_MODULE_1_ionic_angular__["g" /* IonicPageModule */].forChild(__WEBPACK_IMPORTED_MODULE_2__player_info__["a" /* PlayerInfoPage */]),
                __WEBPACK_IMPORTED_MODULE_3_ionic2_auto_complete__["a" /* AutoCompleteModule */],
            ],
        })
    ], PlayerInfoPageModule);
    return PlayerInfoPageModule;
}());

//# sourceMappingURL=player-info.module.js.map

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

/***/ 751:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return PlayerInfoPage; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__(1);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__components_auto_complete_auto_complete__ = __webpack_require__(752);
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
 * Generated class for the PlayerInfoPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */
var PlayerInfoPage = (function (_super) {
    __extends(PlayerInfoPage, _super);
    function PlayerInfoPage() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.loading = false;
        _this.ticketCounts = null;
        _this.selectedPlayer = null;
        _this.player_id_for_event = null;
        _this.playerLoadStatus = 'notStarted';
        _this.singleUser = null;
        return _this;
    }
    // generateGetEventPlayerProcessor(){
    //     return (result)=>{
    //         if(result==null){                
    //             return
    //         }
    //         this.selectedPlayer=result.data;
    //         this.ticketCounts=this.generateListFromObj(this.selectedPlayer.tournament_counts);            
    //     }
    // }
    PlayerInfoPage.prototype.ionViewWillLoad = function () {
        console.log('ionViewDidLoad PlayerInfoPage');
        //this.autoCompleteProvider.setPlayerSearchType("allPlayers",
        //                                              this.generateLoadingFunction());      
        this.autoCompleteProvider.initializeAutoComplete(null, null, this.generatePlayerLoadingFunction(), this.eventId);
        var player_id_for_event = this.navParams.get('player_id_for_event');
        if (player_id_for_event == null) {
            return;
        }
        this.player_id_for_event = player_id_for_event;
        //this.pssApi.getEventPlayer(this.eventId,this.player_id_for_event)
        //    .subscribe(this.generateGetEventPlayerProcessor())                                                  
    };
    PlayerInfoPage.prototype.onFocus = function () {
        console.log('in onFocus..');
        this.selectedPlayer = null;
        this.ticketCounts = null;
        //this.selectedPlayer={player_full_name:null,player_id_for_event:null,first_name:null,last_name:null};
    };
    // onSelected(){
    //     console.log(this.selectedPlayer);
    //     this.pssApi.getEventPlayer(this.eventId,this.selectedPlayer.player_id_for_event)
    //         .subscribe(this.generateAutoCompleteGetEventPlayerProcessor())
    // }
    PlayerInfoPage.prototype.onInput = function (event) {
        console.log('in onInput...');
        console.log(event);
        this.loading = true;
        //if(event.length==3){
        //this.searchbar.select(100);
        //}
    };
    PlayerInfoPage.prototype.onItemsShown = function () {
        console.log('in onItemsShown');
        //        console.log(event);
        //        console.log(this.searchbar);
        //        this.searchbar.select(null);
        //this.searchbar._showList=false;
        //        console.log("-----------");        
        //        console.log(this.searchbar.getItems());
        //        console.log("-----------");        
    };
    // generateLoadingFunction(){
    //     return (input?)=>{
    //         if(input!=null){
    //             console.log(input)
    //             this.selectedPlayer=input.data;
    //             console.log(this.selectedPlayer);
    //             this.ticketCounts=this.generateListFromObj(this.selectedPlayer.tournament_counts);
    //         }            
    //         setTimeout(()=>{this.loading=false;},500)            
    //     }
    // }
    // generateListFromObj(obj){
    //     if(obj==null){
    //         return []
    //     }
    //     return Object.keys(obj).map(function(key){
    //         let objValue =obj[key];
    //         // do something with person
    //         return objValue
    //     });
    // }
    // onInput(event){        
    //     this.playerLoadStatus='notStarted';
    //     if(this.player_id_for_event != null && this.player_id_for_event > 99 && this.player_id_for_event < 1000){
    //         console.log('in onInput')
    //         this.pssApi.getEventPlayer(this.eventId,this.player_id_for_event)
    //             .subscribe(this.generateGetEventPlayerProcessor())                                                  
    //     } else {
    //         this.clearValues();
    //     }        
    // }
    PlayerInfoPage.prototype.clearValues = function () {
        this.selectedPlayer = {};
        //this.eventPlayer={};
        //this.player_id_for_event=null;        
    };
    __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["ViewChild"])('searchbar'),
        __metadata("design:type", Object)
    ], PlayerInfoPage.prototype, "searchbar", void 0);
    PlayerInfoPage = __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["Component"])({
            selector: 'page-player-info',template:/*ion-inline-start:"/Users/agoldma/git/github/TD/front_v2/src/pages/player-info/player-info.html"*/'<!--\n  Generated template for the PlayerInfoPage page.\n\n  See http://ionicframework.com/docs/components/#navigation for more info on\n  Ionic pages and navigation.\n  -->\n\n<ion-header>\n\n  <ion-navbar>\n    <ion-title>PlayerInfo</ion-title>\n  </ion-navbar>\n\n</ion-header>\n\n\n\n<ion-content padding>\n  <ion-auto-complete name="myautocomplete" [(ngModel)]="selectedPlayer" #searchbar (autoFocus)="onFocus()" (ionAutoInput)="onInput($event)" (itemsShown)="onItemsShown()" (itemSelected)="onAutoCompletePlayerSelected($event)" [dataProvider]="autoCompleteProvider" [options]="{ placeholder : \'Enter Player Name/ID\', debounce:500}"></ion-auto-complete>\n  <!--\n      Player name\n      player event number\n      player pic\n      \n      Available Tickets\n      - tournament/metatournament name : count\n      \n      Results (when they are available)\n\n    -->\n  <ion-list *ngIf="selectedPlayer!=null">\n    <ion-item-divider text-center color="light">\n      Player Name\n    </ion-item-divider>\n    <ion-item no-lines text-center>\n      {{selectedPlayer.player_full_name}}\n    </ion-item>\n    <ion-item-divider text-center color="light">\n      Player Number\n    </ion-item-divider>\n    <ion-item text-center no-lines>\n      {{selectedPlayer.player_id_for_event}}\n    </ion-item>\n    <ion-item-divider text-center color="light">\n      Available Tickets\n    </ion-item-divider>\n    <ion-item no-lines text-center *ngFor="let ticketCount of ticketCounts">\n      {{ticketCount.tournament_name}} : {{ticketCount.count}}\n    </ion-item>\n  </ion-list>\n  <!--   {{selectedPlayer!=null?selectedPlayer.player_id_for_event:""}}-- -->\n  <!--   <div *ngFor="let ticketCount of ticketCounts"> -->\n  <!--     {{ticketCount.tournament_name}} : {{ticketCount.count}} -->\n  <!--   </div> -->\n  <!-- </div>   -->\n</ion-content>\n'/*ion-inline-end:"/Users/agoldma/git/github/TD/front_v2/src/pages/player-info/player-info.html"*/,
        })
    ], PlayerInfoPage);
    return PlayerInfoPage;
}(__WEBPACK_IMPORTED_MODULE_1__components_auto_complete_auto_complete__["a" /* AutoCompleteComponent */]));

//# sourceMappingURL=player-info.js.map

/***/ }),

/***/ 752:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return AutoCompleteComponent; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__(1);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__components_pss_page_pss_page__ = __webpack_require__(727);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__providers_auto_complete_auto_complete__ = __webpack_require__(357);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3_ionic_angular__ = __webpack_require__(34);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_4__providers_event_auth_event_auth__ = __webpack_require__(87);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_5__providers_pss_api_pss_api__ = __webpack_require__(155);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_6_angular2_notifications__ = __webpack_require__(356);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_6_angular2_notifications___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_6_angular2_notifications__);
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









//import { IonicPage } from 'ionic-angular';
/**
 * Generated class for the AutoCompleteComponent component.
 *
 * See https://angular.io/api/core/Component for more info on Angular
 * Components.
 */
var AutoCompleteComponent = (function (_super) {
    __extends(AutoCompleteComponent, _super);
    function AutoCompleteComponent(autoCompleteProvider, eventAuth, navParams, navCtrl, appCtrl, pssApi, platform, actionSheetCtrl, notificationsService, alertCtrl, modalCtrl) {
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
        _this.alertCtrl = alertCtrl;
        _this.modalCtrl = modalCtrl;
        return _this;
    }
    AutoCompleteComponent = __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["Component"])({
            selector: 'auto-complete',template:/*ion-inline-start:"/Users/agoldma/git/github/TD/front_v2/src/components/auto-complete/auto-complete.html"*/'<!-- Generated template for the AutoCompleteComponent component -->\n<div>\n  {{text}}\n</div>\n'/*ion-inline-end:"/Users/agoldma/git/github/TD/front_v2/src/components/auto-complete/auto-complete.html"*/
        }),
        __metadata("design:paramtypes", [__WEBPACK_IMPORTED_MODULE_2__providers_auto_complete_auto_complete__["a" /* AutoCompleteProvider */],
            __WEBPACK_IMPORTED_MODULE_4__providers_event_auth_event_auth__["a" /* EventAuthProvider */],
            __WEBPACK_IMPORTED_MODULE_3_ionic_angular__["m" /* NavParams */],
            __WEBPACK_IMPORTED_MODULE_3_ionic_angular__["l" /* NavController */],
            __WEBPACK_IMPORTED_MODULE_3_ionic_angular__["c" /* App */],
            __WEBPACK_IMPORTED_MODULE_5__providers_pss_api_pss_api__["a" /* PssApiProvider */],
            __WEBPACK_IMPORTED_MODULE_3_ionic_angular__["n" /* Platform */],
            __WEBPACK_IMPORTED_MODULE_3_ionic_angular__["a" /* ActionSheetController */],
            __WEBPACK_IMPORTED_MODULE_6_angular2_notifications__["NotificationsService"],
            __WEBPACK_IMPORTED_MODULE_3_ionic_angular__["b" /* AlertController */],
            __WEBPACK_IMPORTED_MODULE_3_ionic_angular__["j" /* ModalController */]])
    ], AutoCompleteComponent);
    return AutoCompleteComponent;
}(__WEBPACK_IMPORTED_MODULE_1__components_pss_page_pss_page__["a" /* PssPageComponent */]));

//# sourceMappingURL=auto-complete.js.map

/***/ })

});
//# sourceMappingURL=14.js.map