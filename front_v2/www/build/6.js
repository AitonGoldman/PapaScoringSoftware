webpackJsonp([6],{

/***/ 717:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
Object.defineProperty(__webpack_exports__, "__esModule", { value: true });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "QueueSelectPlayerTournamentMachinePageModule", function() { return QueueSelectPlayerTournamentMachinePageModule; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__(1);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1_ionic_angular__ = __webpack_require__(34);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__queue_select_player_tournament_machine__ = __webpack_require__(754);
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};



var QueueSelectPlayerTournamentMachinePageModule = (function () {
    function QueueSelectPlayerTournamentMachinePageModule() {
    }
    QueueSelectPlayerTournamentMachinePageModule = __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["NgModule"])({
            declarations: [
                __WEBPACK_IMPORTED_MODULE_2__queue_select_player_tournament_machine__["a" /* QueueSelectPlayerTournamentMachinePage */],
            ],
            imports: [
                __WEBPACK_IMPORTED_MODULE_1_ionic_angular__["g" /* IonicPageModule */].forChild(__WEBPACK_IMPORTED_MODULE_2__queue_select_player_tournament_machine__["a" /* QueueSelectPlayerTournamentMachinePage */]),
            ],
        })
    ], QueueSelectPlayerTournamentMachinePageModule);
    return QueueSelectPlayerTournamentMachinePageModule;
}());

//# sourceMappingURL=queue-select-player-tournament-machine.module.js.map

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

/***/ 754:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return QueueSelectPlayerTournamentMachinePage; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__(1);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__components_pss_page_pss_page__ = __webpack_require__(727);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__classes_success_summary__ = __webpack_require__(728);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3__classes_SuccessButton__ = __webpack_require__(729);
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
 * Generated class for the QueueSelectPlayerTournamentMachinePage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */
var QueueSelectPlayerTournamentMachinePage = (function (_super) {
    __extends(QueueSelectPlayerTournamentMachinePage, _super);
    function QueueSelectPlayerTournamentMachinePage() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.tournaments = [];
        _this.eventPlayer = {};
        _this.player_id_for_event = null;
        _this.hideSearchbar = false;
        _this.ticketCounts = null;
        _this.queueMode = "manage";
        _this.role = null;
        _this.loggedInPlayerId = null;
        return _this;
    }
    QueueSelectPlayerTournamentMachinePage.prototype.generateGetEventPlayerProcessor = function () {
        var _this = this;
        return function (result) {
            if (result == null) {
                return;
            }
            _this.eventPlayer = result.data != null ? result.data : {};
            _this.ticketCounts = result.tournament_counts;
        };
    };
    QueueSelectPlayerTournamentMachinePage.prototype.generateAddEventPlayerToQueueProcessor = function () {
        var _this = this;
        return function (result) {
            if (result == null) {
                return;
            }
            var success_title_string = _this.eventPlayer.player_full_name + ' has been added to queue.';
            var success_line_one_string = 'Player position in the queue is ' + result.data.position + '.';
            var successSummary = new __WEBPACK_IMPORTED_MODULE_2__classes_success_summary__["a" /* SuccessSummary */](success_title_string, success_line_one_string, null);
            var successButtonHome = new __WEBPACK_IMPORTED_MODULE_3__classes_SuccessButton__["a" /* SuccessButton */]('Go Home', _this.getHomePageString(_this.eventId), _this.buildNavParams({}));
            _this.navCtrl.push("SuccessPage", _this.buildNavParams({ 'successSummary': successSummary,
                'successButtons': [successButtonHome] }));
        };
    };
    QueueSelectPlayerTournamentMachinePage.prototype.addEventPlayerToQueue = function (tournament_machine_id) {
        this.pssApi.addEventPlayerToQueue({ 'player_id': this.eventPlayer.player_id, 'tournament_machine_id': tournament_machine_id }, this.eventId)
            .subscribe(this.generateAddEventPlayerToQueueProcessor());
    };
    QueueSelectPlayerTournamentMachinePage.prototype.generateRemovePlayerFromQueueProcessor = function () {
        var _this = this;
        return function (result) {
            if (result == null) {
                return;
            }
            var success_title_string = result.data.player_full_name + ' has been removed from queue.';
            var successSummary = new __WEBPACK_IMPORTED_MODULE_2__classes_success_summary__["a" /* SuccessSummary */](success_title_string, null, null);
            var successButtonHome = new __WEBPACK_IMPORTED_MODULE_3__classes_SuccessButton__["a" /* SuccessButton */]('Go Home', _this.getHomePageString(_this.eventId), _this.buildNavParams({}));
            _this.navCtrl.push("SuccessPage", _this.buildNavParams({ 'successSummary': successSummary,
                'successButtons': [successButtonHome] }));
        };
    };
    QueueSelectPlayerTournamentMachinePage.prototype.generateRemovePlayerFromQueue = function () {
        var _this = this;
        return function (queue, tournament_machine) {
            console.log(queue);
            _this.pssApi.removePlayerFromQueue({ player_id: queue.player.player_id, tournament_machine_id: tournament_machine.tournament_machine_id }, _this.eventId)
                .subscribe(_this.generateRemovePlayerFromQueueProcessor());
        };
    };
    QueueSelectPlayerTournamentMachinePage.prototype.generateGetAllTournamentsAndMachinesAndEventPlayerProcessor = function (withPlayer) {
        var _this = this;
        if (withPlayer === void 0) { withPlayer = false; }
        return function (result) {
            if (result == null) {
                return;
            }
            if (withPlayer == true) {
                _this.eventPlayer = result.player;
            }
            _this.tournaments = result.data;
            var role = null;
            var loggedInPlayerId = null;
            if (_this.eventAuth.isEventUserLoggedIn(_this.eventId)) {
                role = _this.eventAuth.getRoleName(_this.eventId);
                if (role == 'player') {
                    loggedInPlayerId = _this.eventAuth.getEventPlayerId(_this.eventId);
                }
            }
            _this.tournaments.map(function (tournament) {
                tournament.expanded = false;
                tournament.tournament_machines.map(function (tournament_machine) {
                    tournament_machine.expanded = false;
                    tournament_machine.queues.map(function (queue) {
                        queue.icon = 'person';
                        if (role == null || role == 'scorekeeper') {
                            queue.whatToDo = function (x, y) { };
                        }
                        if (role == 'player') {
                            if (queue.player != null && queue.player.player_id == loggedInPlayerId) {
                                queue.icon = 'remove-circle';
                                queue.allowedToRemove = true;
                                queue.whatToDo = _this.generateRemovePlayerFromQueue();
                            }
                        }
                        if (role == 'tournamentdirector' || role == 'deskworker') {
                            queue.icon = 'remove-circle';
                            queue.allowedToRemove = true;
                            queue.whatToDo = _this.generateRemovePlayerFromQueue();
                        }
                    });
                });
            });
        };
    };
    QueueSelectPlayerTournamentMachinePage.prototype.ionViewWillLoad = function () {
        //this.queueMode=this.navParams.get('queueMode');
        this.role = this.eventAuth.getRoleName(this.eventId);
        if (this.eventAuth.getRoleName(this.eventId) == 'player') {
            this.loggedInPlayerId = this.eventAuth.getPlayerId(this.eventId);
            this.player_id_for_event = this.eventAuth.getEventPlayerId(this.eventId);
        }
        if (this.player_id_for_event == null) {
            this.pssApi.getAllTournamentsAndMachines(this.eventId)
                .subscribe(this.generateGetAllTournamentsAndMachinesAndEventPlayerProcessor());
        }
        else {
            this.pssApi.getAllTournamentsAndMachinesAndEventPlayer(this.eventId, this.player_id_for_event)
                .subscribe(this.generateGetAllTournamentsAndMachinesAndEventPlayerProcessor(true));
        }
        console.log('ionViewDidLoad QueueSelectPlayerTournamentMachinePage');
        console.log(this.role);
    };
    QueueSelectPlayerTournamentMachinePage = __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["Component"])({
            selector: 'page-queue-select-player-tournament-machine',template:/*ion-inline-start:"/Users/agoldma/git/github/TD/front_v2/src/pages/queue-select-player-tournament-machine/queue-select-player-tournament-machine.html"*/'<!--\n  Generated template for the QueueSelectPlayerTournamentMachinePage page.\n\n  See http://ionicframework.com/docs/components/#navigation for more info on\n  Ionic pages and navigation.\n-->\n<ion-header>\n\n  <ion-navbar>\n    <ion-title>QueueSelectPlayerTournamentMachine</ion-title>\n  </ion-navbar>\n\n</ion-header>\n\n\n<ion-content padding>\n  <div>    \n  <ion-list>\n    <ng-container *ngFor="let tournament of tournaments">\n      <ion-item-divider (click)="expand(tournament)">\n        <ion-avatar item-start *ngIf="tournament.img_url!=null">\n          <img [src]="tournament.img_url">\n        </ion-avatar>        \n        <h1>{{tournament.tournament_name}}</h1><ion-icon item-end [name]="tournament.expanded==false?\'ios-arrow-dropdown\':\'ios-arrow-dropup\'"></ion-icon>\n      </ion-item-divider>      \n      <ng-container *ngIf="tournament.expanded!=true?false:true">\n        <ion-list>\n          <ng-container *ngFor="let tournament_machine of tournament.tournament_machines">\n            <ion-item  (click)="expand(tournament_machine)">\n              {{tournament_machine.tournament_machine_name}} <span *ngIf=\'tournament_machine.queue_length > 0\'>({{tournament_machine.queue_length}})</span><ion-icon item-end [name]="tournament_machine.expanded==false?\'ios-arrow-dropdown\':\'ios-arrow-dropup\'"></ion-icon>\n            </ion-item>            \n            <ion-list *ngIf="tournament_machine.expanded==true && tournament.expanded==true">\n              <ion-item>\n                <ion-icon item-start name="play" *ngIf="tournament_machine.player_id!=null"></ion-icon>\n                <ion-icon item-start *ngIf="tournament_machine.player_id==null"></ion-icon>\n                {{tournament_machine.player_id==null?"Not Being Played":tournament_machine.player.player_full_name}}\n              </ion-item>\n              <ng-container *ngFor="let queue of tournament_machine.queues" >\n                <ion-item *ngIf="queue.player!=null" (click)="queue.whatToDo(queue,tournament_machine)">\n                  <ion-icon item-start [name]="queue.icon"></ion-icon> <span>{{queue.player.player_full_name}}</span>\n                </ion-item>\n              </ng-container>\n              \n              <ng-container *ngIf="player_id_for_event==null && role != null">\n                <ion-item  [navPush]="\'AddPlayerToQueuePage\'" [navParams]="buildNavParams({tournamentMachine:tournament_machine})" *ngIf="tournament_machine.player_id!=null || tournament_machine.queues[0].player!=null ">\n                <ion-icon item-start name="add-circle"></ion-icon> Add To Queue\n              </ion-item>\n              </ng-container>\n              <ng-container *ngIf="player_id_for_event!=null">\n                <ion-item  (click)="addEventPlayerToQueue(tournament_machine.tournament_machine_id)">\n                <ion-icon item-start name="add-circle"></ion-icon> Add To Queue\n              </ion-item>\n              </ng-container>\n              \n            </ion-list>\n          </ng-container>\n        </ion-list>\n      </ng-container>      \n    </ng-container>\n  </ion-list>\n</div>\n</ion-content>\n'/*ion-inline-end:"/Users/agoldma/git/github/TD/front_v2/src/pages/queue-select-player-tournament-machine/queue-select-player-tournament-machine.html"*/,
        })
    ], QueueSelectPlayerTournamentMachinePage);
    return QueueSelectPlayerTournamentMachinePage;
}(__WEBPACK_IMPORTED_MODULE_1__components_pss_page_pss_page__["a" /* PssPageComponent */]));

//# sourceMappingURL=queue-select-player-tournament-machine.js.map

/***/ })

});
//# sourceMappingURL=6.js.map