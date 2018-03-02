import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams } from 'ionic-angular';
import { AutoCompleteComponent } from '../../components/auto-complete/auto-complete'

/**
 * Generated class for the AuditLogPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage()
@Component({
  selector: 'page-audit-log',
  templateUrl: 'audit-log.html',
})
export class AuditLogPage extends AutoCompleteComponent {
    auditLogs:any=[];
  onGetAuditLogs() {
      this.pssApi.getAuditLogs(this.eventId,this.selectedPlayer.player_id)
          .subscribe((result)=>{
              this.auditLogs=result.data;
          })
  }
    onFocus(){
        console.log('in onFocus..')
        this.selectedPlayer=null;
        this.showNewScoreForm=false;
        this.newScore={};
    }
    ionViewWillLoad() {
        if(this.eventId==null){
            this.pushRootPage('EventSelectPage')
            return;
        }
        this.autoCompleteProvider.initializeAutoComplete(null,
                                                        null,
                                                        null,
                                                        this.eventId);      
    }
}
