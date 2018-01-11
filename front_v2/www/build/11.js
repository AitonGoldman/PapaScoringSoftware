webpackJsonp([11],{

/***/ 698:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
Object.defineProperty(__webpack_exports__, "__esModule", { value: true });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "AddPlayerPageModule", function() { return AddPlayerPageModule; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__(1);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1_ionic_angular__ = __webpack_require__(34);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__add_player__ = __webpack_require__(734);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3__components_custom_components_module__ = __webpack_require__(360);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_4_ionic2_auto_complete__ = __webpack_require__(358);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_5_angular2_image_upload__ = __webpack_require__(359);
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};






var AddPlayerPageModule = (function () {
    function AddPlayerPageModule() {
    }
    AddPlayerPageModule = __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["NgModule"])({
            declarations: [
                __WEBPACK_IMPORTED_MODULE_2__add_player__["a" /* AddPlayerPage */],
            ],
            imports: [
                __WEBPACK_IMPORTED_MODULE_1_ionic_angular__["g" /* IonicPageModule */].forChild(__WEBPACK_IMPORTED_MODULE_2__add_player__["a" /* AddPlayerPage */]),
                __WEBPACK_IMPORTED_MODULE_3__components_custom_components_module__["a" /* CustomComponentsModule */],
                __WEBPACK_IMPORTED_MODULE_4_ionic2_auto_complete__["a" /* AutoCompleteModule */],
                __WEBPACK_IMPORTED_MODULE_5_angular2_image_upload__["a" /* ImageUploadModule */].forRoot()
            ]
        })
    ], AddPlayerPageModule);
    return AddPlayerPageModule;
}());

//# sourceMappingURL=add-player.module.js.map

/***/ }),

/***/ 726:
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

/***/ 727:
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

/***/ 728:
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

/***/ 734:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return AddPlayerPage; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__(1);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__components_pss_page_pss_page__ = __webpack_require__(726);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__components_take_pic_take_pic__ = __webpack_require__(361);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3__providers_auto_complete_auto_complete__ = __webpack_require__(357);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_4_ionic_angular__ = __webpack_require__(34);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_5__providers_event_auth_event_auth__ = __webpack_require__(87);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_6__providers_pss_api_pss_api__ = __webpack_require__(155);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_7_angular2_notifications__ = __webpack_require__(356);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_7_angular2_notifications___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_7_angular2_notifications__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_8__classes_success_summary__ = __webpack_require__(727);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_9__classes_SuccessButton__ = __webpack_require__(728);
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
 * Generated class for the AddPlayerPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */
var AddPlayerPage = (function (_super) {
    __extends(AddPlayerPage, _super);
    function AddPlayerPage(autoCompleteProvider, eventAuth, navParams, navCtrl, appCtrl, pssApi, platform, actionSheetCtrl, notificationsService, alertCtrl, modalCtrl) {
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
        _this.selectedPlayer = {};
        _this.loading = false;
        _this.ifpaLookup = false;
        _this.existingPlayerFound = true;
        return _this;
    }
    AddPlayerPage.prototype.ionViewDidLoad = function () {
        console.log('ionViewDidLoad AddPlayerPage');
    };
    AddPlayerPage.prototype.generateAddEventPlayersProcessor = function () {
        var _this = this;
        return function (result) {
            if (result == null) {
                return;
            }
            console.log('in generateAddEventPlayerProcessor');
            var success_title_string = 'Player ' + result.data[0].player_full_name + ' has been added to event.';
            var success_line_one_string = 'Player Pin is ' + result.data[0].pin;
            var success_line_two_string = 'Player Number is ' + result.data[0].events[0].player_id_for_event;
            var successSummary = new __WEBPACK_IMPORTED_MODULE_8__classes_success_summary__["a" /* SuccessSummary */](success_title_string, success_line_one_string, success_line_two_string);
            var successButtonHome = new __WEBPACK_IMPORTED_MODULE_9__classes_SuccessButton__["a" /* SuccessButton */]('Go Home', _this.getHomePageString(_this.eventId), _this.buildNavParams({}));
            var successButtonTickets = new __WEBPACK_IMPORTED_MODULE_9__classes_SuccessButton__["a" /* SuccessButton */]('Purchase Tickets', 'TicketPurchasePage', _this.buildNavParams({ player_id_for_event: result.data[0].events[0].player_id_for_event }));
            _this.navCtrl.push("PostPlayerAddSuccessPage", _this.buildNavParams({ 'successSummary': successSummary,
                'successButtons': [successButtonHome, successButtonTickets] }));
        };
    };
    AddPlayerPage.prototype.generateSearchPlayerProcessor = function () {
        return function (result) {
            console.log('in generateSearchPlayerProcessor');
        };
    };
    AddPlayerPage.prototype.takePicture = function () {
        var _this = this;
        var profileModal = this.modalCtrl.create(__WEBPACK_IMPORTED_MODULE_2__components_take_pic_take_pic__["a" /* TakePicComponent */], { userId: 8675309 });
        profileModal.onDidDismiss(function (data) {
            console.log('in modal...');
            console.log(data);
            if (data != null) {
                _this.selectedPlayer.has_pic = true;
                _this.selectedPlayer.img_file = data;
            }
        });
        profileModal.present();
    };
    AddPlayerPage.prototype.generateGetIfpaRankingProcessor = function () {
        var _this = this;
        return function (result) {
            console.log('in generateGetIfpaRankingProcessor');
            if (result == null) {
                return;
            }
            _this.ifpaLookup = true;
            if (result.ifpa_ranking.search.length == 0) {
                var alert_1 = _this.alertCtrl.create();
                alert_1.setTitle('No IFPA Players Found');
                alert_1.setMessage('No players found with the name specified.  Please change the name and try again.');
                alert_1.addButton('Ok');
                alert_1.present();
            }
            if (result.ifpa_ranking.search.length == 1) {
                _this.selectedPlayer.ifpa_ranking = result.ifpa_ranking.search[0].wppr_rank;
            }
            if (result.ifpa_ranking.search.length > 1) {
                var alert_2 = _this.alertCtrl.create();
                alert_2.setTitle('Multiple IFPA Players Found');
                alert_2.setSubTitle('Select Correct Player');
                for (var _i = 0, _a = result.ifpa_ranking.search; _i < _a.length; _i++) {
                    var ifpaPlayer = _a[_i];
                    alert_2.addInput({
                        type: 'radio',
                        label: ifpaPlayer.first_name + " (rank : " + ifpaPlayer.wppr_rank + ")",
                        value: ifpaPlayer.wppr_rank
                    });
                }
                alert_2.addButton('Cancel');
                alert_2.addButton({
                    text: 'OK',
                    handler: function (data) {
                        _this.selectedPlayer.ifpa_ranking = data;
                    }
                });
                alert_2.present();
            }
        };
    };
    AddPlayerPage.prototype.onFocus = function () {
        this.selectedPlayer = { first_name: null, last_name: null };
    };
    AddPlayerPage.prototype.onSelected = function () {
        this.existingPlayerFound = false;
        this.getIfpaRanking(this.selectedPlayer.first_name + " " + this.selectedPlayer.last_name);
    };
    AddPlayerPage.prototype.getIfpaRanking = function (playerName) {
        this.ifpaLookup = true;
        this.pssApi.getIfpaRanking(playerName)
            .subscribe(this.generateGetIfpaRankingProcessor());
    };
    AddPlayerPage.prototype.getIfpaRankingMobile = function (playerName, slidingItem) {
        slidingItem.close();
        this.getIfpaRanking(playerName);
    };
    AddPlayerPage.prototype.onChange = function (event) {
        console.log('in onChange...');
    };
    AddPlayerPage.prototype.onInput = function (event) {
        console.log('in onInput...');
        this.loading = true;
    };
    AddPlayerPage.prototype.onItemsShown = function (event) {
        console.log('onItemsShown...');
        //this.loading=true;
    };
    AddPlayerPage.prototype.generateLoadingFunction = function () {
        var _this = this;
        return function (input) {
            console.log('in loading function');
            if (input.length == 0) {
                if (_this.searchbar.keyword.length > 2) {
                    console.log(_this.searchbar.suggestions.length);
                    _this.existingPlayerFound = false;
                    var nameElements = _this.searchbar.keyword.split(' ');
                    if (nameElements.length > 0) {
                        _this.selectedPlayer.first_name = nameElements[0];
                    }
                    if (nameElements.length > 1) {
                        _this.selectedPlayer.last_name = nameElements[1];
                    }
                }
            }
            else {
                _this.existingPlayerFound = true;
            }
            setTimeout(function () { _this.loading = false; }, 500);
        };
    };
    AddPlayerPage.prototype.ionViewWillLoad = function () {
        console.log('ionViewDidLoad AddPlayerPage');
        this.eventId = this.navParams.get('eventId');
        this.autoCompleteProvider.setPlayerSearchType("allPlayers", this.generateLoadingFunction());
        //this.autoCompleteProvider.setPlayers(true);
        //this.pssApi.searchPlayers('poop2')
        //    .subscribe(this.generateSearchPlayerProcessor())            
    };
    // onUploadFinished(event){
    //     this.selectedPlayer.has_pic=true;        
    //     console.log(event.serverResponse._body);
    //     this.selectedPlayer.img_file=JSON.parse(event.serverResponse._body).data;        
    // }
    AddPlayerPage.prototype.onSubmit = function () {
        if (this.selectedPlayer.ifpa_ranking == 'not ranked') {
            this.selectedPlayer.ifpa_ranking = 99999;
        }
        this.pssApi.addEventPlayers({ players: [this.selectedPlayer] }, this.eventId)
            .subscribe(this.generateAddEventPlayersProcessor());
    };
    __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["ViewChild"])('searchbar'),
        __metadata("design:type", Object)
    ], AddPlayerPage.prototype, "searchbar", void 0);
    AddPlayerPage = __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["Component"])({
            selector: 'page-add-player',template:/*ion-inline-start:"/Users/agoldma/git/github/TD/front_v2/src/pages/add-player/add-player.html"*/'<ion-header>\n  <ion-navbar>\n    <custom-headers [eventId]="eventId" [homePage]="getHomePageString()"></custom-headers>\n  </ion-navbar>\n</ion-header>\n<ion-content padding>\n  <div class=\'desktopSlim\'>\n    <ion-grid>\n      <ion-row>\n        <ion-col col-1>\n        </ion-col>\n        <ion-col col-10>\n          <ion-auto-complete name="myautocomplete" [(ngModel)]="selectedPlayer" #searchbar (autoFocus)="onFocus()" (itemsShown)="onItemsShown($event)" (ionAutoInput)="onInput($event)" (itemSelected)="onSelected($event)" [dataProvider]="autoCompleteProvider" [options]="{ placeholder : \'Enter Player Name\', debounce:500}"></ion-auto-complete>\n        </ion-col>\n        <ion-col col-1>\n          <ion-spinner *ngIf=\'loading==true\' style=\'margin-bottom:7px\'></ion-spinner>\n        </ion-col>\n      </ion-row>\n    </ion-grid>\n\n    <form #myForm="ngForm" *ngIf="existingPlayerFound==false && loading==false">\n      <ion-list>\n        <ion-item no-line *ngIf="selectedPlayer.img_url!=null">\n          <!-- <ion-grid> -->\n          <!--   <ion-row> -->\n          <!--     <ion-col col-5 style=\'background-color:red\'> -->\n          <!--     </ion-col> -->\n          <!--     <ion-col justify-content-center align-items-center> -->\n                <ion-avatar style=\'zoom:3.0\'>\n                  <img [src]="selectedPlayer.img_url" style=\'margin-left:auto;margin-right:auto\'>\n                </ion-avatar>\n          <!--     </ion-col> -->\n          <!--     <ion-col col-5 style=\'background-color:red\'> -->\n          <!--     </ion-col>               -->\n          <!--   </ion-row> -->\n          <!-- </ion-grid> -->\n        </ion-item>\n        <ion-item>\n        <ion-label floating>First Name</ion-label>\n        <ion-input type="text" required\n                   [(ngModel)]="selectedPlayer.first_name" name="first_name"></ion-input>\n      </ion-item>\n      <ion-item>\n        <ion-label stacked>Last Name</ion-label>\n        <ion-input type="text" required\n                   [(ngModel)]="selectedPlayer.last_name" name="last_name"></ion-input>\n      </ion-item>\n      <ion-item-sliding #slidingItem>\n        <ion-item>\n          <ion-label stacked>Ifpa Ranking <span showWhen="mobile">(slide left to re-lookup)</span></ion-label>\n          <ion-input type="text" required\n                     [(ngModel)]="selectedPlayer.ifpa_ranking" name="ifpa_ranking">           \n          </ion-input>\n          <ion-icon (click)=\'getIfpaRanking(selectedPlayer.first_name+" "+selectedPlayer.last_name)\' hideWhen="mobile" name=\'cloud-download\' item-end></ion-icon>\n        </ion-item>\n        <ion-item-options side="right">\n          <button ion-button (click)=\'getIfpaRankingMobile(selectedPlayer.first_name+" "+selectedPlayer.last_name,slidingItem)\'>\n            Lookup\n            <ion-icon name="cloud-download"></ion-icon>            \n          </button>\n        </ion-item-options>        \n      </ion-item-sliding>\n      <ion-item (click)="takePicture()">\n        Take a picture <span>{{selectedPlayer.has_pic==true?"(pic uploaded)":"poop"}}</span>\n           <ion-icon name=\'camera\' item-end></ion-icon>\n      </ion-item>\n      <!-- <ion-item-divider color="light" text-wrap>Upload an image that will be used as the event icon </ion-item-divider> -->\n      <!-- <ion-item> -->\n      <!--   <image-upload (uploadFinished)="onUploadFinished($event)" url="http://192.168.1.178:8000/media_upload"></image-upload> -->\n      <!-- </ion-item> -->      \n      <ion-item text-center>\n        <button ion-button padding (click)="onSubmit()">\n          register player \n        </button>\n      </ion-item>\n      </ion-list>\n    </form>\n    </div>\n</ion-content>\n'/*ion-inline-end:"/Users/agoldma/git/github/TD/front_v2/src/pages/add-player/add-player.html"*/,
        }),
        __metadata("design:paramtypes", [__WEBPACK_IMPORTED_MODULE_3__providers_auto_complete_auto_complete__["a" /* AutoCompleteProvider */],
            __WEBPACK_IMPORTED_MODULE_5__providers_event_auth_event_auth__["a" /* EventAuthProvider */],
            __WEBPACK_IMPORTED_MODULE_4_ionic_angular__["m" /* NavParams */],
            __WEBPACK_IMPORTED_MODULE_4_ionic_angular__["l" /* NavController */],
            __WEBPACK_IMPORTED_MODULE_4_ionic_angular__["c" /* App */],
            __WEBPACK_IMPORTED_MODULE_6__providers_pss_api_pss_api__["a" /* PssApiProvider */],
            __WEBPACK_IMPORTED_MODULE_4_ionic_angular__["n" /* Platform */],
            __WEBPACK_IMPORTED_MODULE_4_ionic_angular__["a" /* ActionSheetController */],
            __WEBPACK_IMPORTED_MODULE_7_angular2_notifications__["NotificationsService"],
            __WEBPACK_IMPORTED_MODULE_4_ionic_angular__["b" /* AlertController */],
            __WEBPACK_IMPORTED_MODULE_4_ionic_angular__["j" /* ModalController */]])
    ], AddPlayerPage);
    return AddPlayerPage;
}(__WEBPACK_IMPORTED_MODULE_1__components_pss_page_pss_page__["a" /* PssPageComponent */]));

//# sourceMappingURL=add-player.js.map

/***/ })

});
//# sourceMappingURL=11.js.map