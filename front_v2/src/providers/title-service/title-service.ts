import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

/*
  Generated class for the TitleServiceProvider provider.

  See https://angular.io/guide/dependency-injection for more info on providers
  and Angular DI.
*/
@Injectable()
export class TitleServiceProvider {
  title:any = undefined;
  
  constructor(public http: HttpClient) {
    console.log('Hello TitleServiceProvider Provider');
    this.title='aiton';
  }
  setTitle(newTitle:string){
   this.title=newTitle;
  }
  getTitle():string{
   return this.title;
  }
}
