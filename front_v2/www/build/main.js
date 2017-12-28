webpackJsonp([8],{

/***/ 125:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return EventAuthProvider; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_common_http__ = __webpack_require__(59);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__angular_core__ = __webpack_require__(0);
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};


/*
  Generated class for the EventAuthProvider provider.

  See https://angular.io/guide/dependency-injection for more info on providers
  and Angular DI.
*/
var EventAuthProvider = (function () {
    function EventAuthProvider(http) {
        this.http = http;
        this.userEventRoles = {};
        this.userLoggedInEvents = {};
        this.userName = null;
        console.log('Hello EventAuthProvider Provider');
    }
    EventAuthProvider.prototype.setEventUserLoggedIn = function (eventId, userInfo) {
        this.userLoggedInEvents[eventId] = true;
        this.userName = userInfo.username;
        this.setEventRole(eventId, userInfo.roles[0]);
        console.log('setEventUserLoggedIn debug...');
        console.log(userInfo);
    };
    EventAuthProvider.prototype.isEventUserLoggedIn = function (eventId) {
        if (eventId in this.userLoggedInEvents) {
            return this.userLoggedInEvents[eventId];
        }
        else {
            return null;
        }
        //return this.userLoggedInEvents[eventId]!=null&&this.userLoggedInEvents[eventId]!=undefined;
    };
    EventAuthProvider.prototype.setEventRole = function (eventId, role) {
        this.userEventRoles[eventId] = role;
    };
    EventAuthProvider.prototype.getRoleName = function (eventId) {
        if (eventId in this.userEventRoles) {
            return this.userEventRoles[eventId].event_role_name;
        }
        else {
            return null;
        }
    };
    EventAuthProvider = __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_1__angular_core__["A" /* Injectable */])(),
        __metadata("design:paramtypes", [__WEBPACK_IMPORTED_MODULE_0__angular_common_http__["a" /* HttpClient */]])
    ], EventAuthProvider);
    return EventAuthProvider;
}());

//# sourceMappingURL=event-auth.js.map

/***/ }),

/***/ 126:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return TitleServiceProvider; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_common_http__ = __webpack_require__(59);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__angular_core__ = __webpack_require__(0);
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};


/*
  Generated class for the TitleServiceProvider provider.

  See https://angular.io/guide/dependency-injection for more info on providers
  and Angular DI.
*/
var TitleServiceProvider = (function () {
    function TitleServiceProvider(http) {
        this.http = http;
        this.title = undefined;
        console.log('Hello TitleServiceProvider Provider');
        this.title = 'aiton';
    }
    TitleServiceProvider.prototype.setTitle = function (newTitle) {
        this.title = newTitle;
    };
    TitleServiceProvider.prototype.getTitle = function () {
        return this.title;
    };
    TitleServiceProvider = __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_1__angular_core__["A" /* Injectable */])(),
        __metadata("design:paramtypes", [__WEBPACK_IMPORTED_MODULE_0__angular_common_http__["a" /* HttpClient */]])
    ], TitleServiceProvider);
    return TitleServiceProvider;
}());

//# sourceMappingURL=title-service.js.map

/***/ }),

/***/ 137:
/***/ (function(module, exports) {

function webpackEmptyAsyncContext(req) {
	// Here Promise.resolve().then() is used instead of new Promise() to prevent
	// uncatched exception popping up in devtools
	return Promise.resolve().then(function() {
		throw new Error("Cannot find module '" + req + "'.");
	});
}
webpackEmptyAsyncContext.keys = function() { return []; };
webpackEmptyAsyncContext.resolve = webpackEmptyAsyncContext;
module.exports = webpackEmptyAsyncContext;
webpackEmptyAsyncContext.id = 137;

/***/ }),

/***/ 181:
/***/ (function(module, exports, __webpack_require__) {

var map = {
	"../pages/event-select/event-select.module": [
		400,
		7
	],
	"../pages/home/home.module": [
		401,
		1
	],
	"../pages/login/login.module": [
		402,
		0
	],
	"../pages/menu/menu.module": [
		403,
		6
	],
	"../pages/quick-links/quick-links.module": [
		404,
		5
	],
	"../pages/results/results.module": [
		405,
		4
	],
	"../pages/success/success.module": [
		406,
		3
	],
	"../pages/tabs/tabs.module": [
		407,
		2
	]
};
function webpackAsyncContext(req) {
	var ids = map[req];
	if(!ids)
		return Promise.reject(new Error("Cannot find module '" + req + "'."));
	return __webpack_require__.e(ids[1]).then(function() {
		return __webpack_require__(ids[0]);
	});
};
webpackAsyncContext.keys = function webpackAsyncContextKeys() {
	return Object.keys(map);
};
webpackAsyncContext.id = 181;
module.exports = webpackAsyncContext;

/***/ }),

/***/ 242:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return PssApiProvider; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_common_http__ = __webpack_require__(59);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__angular_core__ = __webpack_require__(0);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2_rxjs_operators__ = __webpack_require__(277);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2_rxjs_operators___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_2_rxjs_operators__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3_rxjs_observable_of__ = __webpack_require__(97);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3_rxjs_observable_of___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_3_rxjs_observable_of__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_4_ionic_angular__ = __webpack_require__(50);
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};






/*
  Generated class for the PssApiProvider provider.

  See https://angular.io/guide/dependency-injection for more info on providers
  and Angular DI.
*/
var PssApiProvider = (function () {
    function PssApiProvider(http, loadingCtrl, toastCtrl) {
        this.http = http;
        this.loadingCtrl = loadingCtrl;
        this.toastCtrl = toastCtrl;
        this.basePssUrl = 'http://localhost:8000';
        this.loading_instance = null;
        this.loginUser = this.generate_api_call('loginUser', this.basePssUrl + "/auth/pss_event_user/login/:arg", 'post');
        console.log('Hello PssApiProvider Provider');
    }
    PssApiProvider.prototype.generate_api_call = function (apiName, url, method) {
        var _this = this;
        return function () {
            var restOfArgs = [];
            for (var _i = 0; _i < arguments.length; _i++) {
                restOfArgs[_i] = arguments[_i];
            }
            var localUrl = url;
            var postObject = null;
            if (method == "post" || method == "put") {
                postObject = restOfArgs.shift();
            }
            if (localUrl.match(/\:arg/g).length != restOfArgs.length) {
                throw new Error("Oops - number of args in url and args given do not match");
            }
            _this.loading_instance = _this.loadingCtrl.create({
                content: 'Please wait...'
            });
            _this.loading_instance.present();
            while (localUrl.indexOf(':arg') >= 0) {
                var newUrl = localUrl.replace(":arg", restOfArgs.shift());
                localUrl = newUrl;
            }
            var result_observable = _this.http[method](localUrl, postObject)
                .pipe(Object(__WEBPACK_IMPORTED_MODULE_2_rxjs_operators__["catchError"])(_this.handleError(apiName, null)));
            result_observable.subscribe(function () { _this.loading_instance.dismiss(); });
            return result_observable;
        };
    };
    // loginUser(eventId, user_info) {
    //     this.loading_instance = this.loadingCtrl.create({
    //         content: 'Please wait...'
    //     });
    //     this.loading_instance.present();        
    //     let result_observable = this.http.post(this.basePssUrl+"/auth/pss_event_user/login/"+eventId,
    //                                        user_info)
    //         .pipe(                
    //             catchError(this.handleError('loginUser', null))
    //         );
    //     result_observable.subscribe(()=>{this.loading_instance.dismiss()});
    //     return result_observable;
    // }
    PssApiProvider.prototype.handleError = function (operation, result) {
        var _this = this;
        if (operation === void 0) { operation = 'operation'; }
        //this.loading.dismiss();
        var debouncer = false;
        return function (error) {
            if (debouncer == false) {
                debouncer = true;
                console.log('error handling in progress...');
                console.error(error); // log to console instead
                var toast = _this.toastCtrl.create({
                    message: error.error.message,
                    duration: 99000,
                    position: 'top',
                    showCloseButton: true,
                    cssClass: "dangerToast"
                });
                toast.present();
            }
            // Let the app keep running by returning an empty result.
            return Object(__WEBPACK_IMPORTED_MODULE_3_rxjs_observable_of__["of"])(result);
            //throw Observable.throw(result);  
        };
    };
    PssApiProvider = __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_1__angular_core__["A" /* Injectable */])(),
        __metadata("design:paramtypes", [__WEBPACK_IMPORTED_MODULE_0__angular_common_http__["a" /* HttpClient */], __WEBPACK_IMPORTED_MODULE_4_ionic_angular__["f" /* LoadingController */],
            __WEBPACK_IMPORTED_MODULE_4_ionic_angular__["l" /* ToastController */]])
    ], PssApiProvider);
    return PssApiProvider;
}());

//# sourceMappingURL=pss-api.js.map

/***/ }),

/***/ 243:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
Object.defineProperty(__webpack_exports__, "__esModule", { value: true });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_platform_browser_dynamic__ = __webpack_require__(244);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__app_module__ = __webpack_require__(253);


Object(__WEBPACK_IMPORTED_MODULE_0__angular_platform_browser_dynamic__["a" /* platformBrowserDynamic */])().bootstrapModule(__WEBPACK_IMPORTED_MODULE_1__app_module__["a" /* AppModule */]);
//# sourceMappingURL=main.js.map

/***/ }),

/***/ 253:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return AppModule; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_platform_browser__ = __webpack_require__(41);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__angular_core__ = __webpack_require__(0);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2_ionic_angular__ = __webpack_require__(50);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3__ionic_native_splash_screen__ = __webpack_require__(238);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_4__ionic_native_status_bar__ = __webpack_require__(241);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_5__angular_common_http__ = __webpack_require__(59);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_6__app_component__ = __webpack_require__(399);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_7__providers_title_service_title_service__ = __webpack_require__(126);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_8__providers_event_auth_event_auth__ = __webpack_require__(125);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_9__providers_pss_api_pss_api__ = __webpack_require__(242);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_10__angular_forms__ = __webpack_require__(23);
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};











//import { ComponentsModule } from '../components/components.module'
//import { CustomHeaderComponent } from '../components/custom-header/custom-header';
var AppModule = (function () {
    function AppModule() {
    }
    AppModule = __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_1__angular_core__["I" /* NgModule */])({
            declarations: [
                __WEBPACK_IMPORTED_MODULE_6__app_component__["a" /* MyApp */] //,
                //CustomHeaderComponent
            ],
            imports: [
                __WEBPACK_IMPORTED_MODULE_0__angular_platform_browser__["a" /* BrowserModule */],
                __WEBPACK_IMPORTED_MODULE_2_ionic_angular__["d" /* IonicModule */].forRoot(__WEBPACK_IMPORTED_MODULE_6__app_component__["a" /* MyApp */], {}, {
                    links: [
                        { loadChildren: '../pages/event-select/event-select.module#EventSelectPageModule', name: 'EventSelectPage', segment: 'event-select', priority: 'low', defaultHistory: [] },
                        { loadChildren: '../pages/home/home.module#HomePageModule', name: 'HomePage', segment: 'HomePage/:eventId', priority: 'low', defaultHistory: [] },
                        { loadChildren: '../pages/login/login.module#LoginPageModule', name: 'LoginPage', segment: 'login/:eventId', priority: 'low', defaultHistory: [] },
                        { loadChildren: '../pages/menu/menu.module#MenuPageModule', name: 'MenuPage', segment: 'menu', priority: 'low', defaultHistory: [] },
                        { loadChildren: '../pages/quick-links/quick-links.module#QuickLinksPageModule', name: 'QuickLinksPage', segment: 'quick-links', priority: 'low', defaultHistory: [] },
                        { loadChildren: '../pages/results/results.module#ResultsPageModule', name: 'ResultsPage', segment: 'results', priority: 'low', defaultHistory: [] },
                        { loadChildren: '../pages/success/success.module#SuccessPageModule', name: 'SuccessPage', segment: 'Success/:eventId', priority: 'low', defaultHistory: [] },
                        { loadChildren: '../pages/tabs/tabs.module#TabsPageModule', name: 'TabsPage', segment: 'tabs', priority: 'low', defaultHistory: [] }
                    ]
                }),
                __WEBPACK_IMPORTED_MODULE_5__angular_common_http__["b" /* HttpClientModule */],
                __WEBPACK_IMPORTED_MODULE_10__angular_forms__["a" /* FormsModule */] //,
                //ComponentsModule
            ],
            bootstrap: [__WEBPACK_IMPORTED_MODULE_2_ionic_angular__["b" /* IonicApp */]],
            entryComponents: [
                __WEBPACK_IMPORTED_MODULE_6__app_component__["a" /* MyApp */]
            ],
            providers: [
                __WEBPACK_IMPORTED_MODULE_4__ionic_native_status_bar__["a" /* StatusBar */],
                __WEBPACK_IMPORTED_MODULE_3__ionic_native_splash_screen__["a" /* SplashScreen */],
                { provide: __WEBPACK_IMPORTED_MODULE_1__angular_core__["u" /* ErrorHandler */], useClass: __WEBPACK_IMPORTED_MODULE_2_ionic_angular__["c" /* IonicErrorHandler */] },
                __WEBPACK_IMPORTED_MODULE_7__providers_title_service_title_service__["a" /* TitleServiceProvider */],
                __WEBPACK_IMPORTED_MODULE_8__providers_event_auth_event_auth__["a" /* EventAuthProvider */],
                __WEBPACK_IMPORTED_MODULE_9__providers_pss_api_pss_api__["a" /* PssApiProvider */]
            ]
        })
    ], AppModule);
    return AppModule;
}());

//# sourceMappingURL=app.module.js.map

/***/ }),

/***/ 399:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return MyApp; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__(0);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1_ionic_angular__ = __webpack_require__(50);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__ionic_native_status_bar__ = __webpack_require__(241);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3__ionic_native_splash_screen__ = __webpack_require__(238);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_4__providers_title_service_title_service__ = __webpack_require__(126);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_5__providers_event_auth_event_auth__ = __webpack_require__(125);
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};






var MyApp = (function () {
    function MyApp(platform, statusBar, splashScreen, titleService, eventAuth) {
        this.titleService = titleService;
        this.eventAuth = eventAuth;
        platform.ready().then(function () {
            // Okay, so the platform is ready and our plugins are available.
            // Here you can do any higher level native things you might need.
            statusBar.styleDefault();
            splashScreen.hide();
        });
    }
    MyApp = __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["m" /* Component */])({template:/*ion-inline-start:"/Users/agoldma/git/github/TD/front_v2/src/app/app.html"*/'<ion-menu [content]="content">\n  <ion-header>\n    <ion-toolbar>\n      <ion-title>Menu</ion-title>\n    </ion-toolbar>\n  </ion-header>\n \n  <ion-content>\n    <ion-list>\n      <button ion-item menuClose>\n        hi there\n      </button>\n    </ion-list>\n  </ion-content>\n</ion-menu>\n<!-- main navigation -->\n<!--\n<ion-header hideWhen="mobile">\n  <ion-navbar>\n    <ion-title>Pss</ion-title>\n    <ion-buttons end>\n      <button icon-only ion-button [navPush]="\'LoginPage\'" [navParams]="getEventIdName()" >Login</button>\n      <button icon-only ion-button>Results</button>\n      <button icon-only ion-button>Queues</button>\n      <button *ngIf="eventAuth.getRoleName(eventId)" icon-only ion-button (click)="menuNav(getRolePage())">{{eventAuth.getRoleName(eventId)}}</button>\n    </ion-buttons>\n  </ion-navbar>\n</ion-header>\n-->\n\n<ion-nav [root]="\'EventSelectPage\'" [rootParams]="{eventId:eventId,eventName:eventName}" #content swipeBackEnabled="false">\n</ion-nav>\n'/*ion-inline-end:"/Users/agoldma/git/github/TD/front_v2/src/app/app.html"*/
        }),
        __metadata("design:paramtypes", [__WEBPACK_IMPORTED_MODULE_1_ionic_angular__["i" /* Platform */], __WEBPACK_IMPORTED_MODULE_2__ionic_native_status_bar__["a" /* StatusBar */],
            __WEBPACK_IMPORTED_MODULE_3__ionic_native_splash_screen__["a" /* SplashScreen */], __WEBPACK_IMPORTED_MODULE_4__providers_title_service_title_service__["a" /* TitleServiceProvider */],
            __WEBPACK_IMPORTED_MODULE_5__providers_event_auth_event_auth__["a" /* EventAuthProvider */]])
    ], MyApp);
    return MyApp;
}());

//# sourceMappingURL=app.component.js.map

/***/ })

},[243]);
//# sourceMappingURL=main.js.map