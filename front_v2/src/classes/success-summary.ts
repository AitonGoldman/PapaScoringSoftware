export class SuccessSummary  {    
    //title:string = null;
    //firstLine:string = null;
    //secondLine:string = null;
    summaryTable=[]
    attentionString:string=null;
    constructor(public title:string,
                public firstLine:string,
                public secondLine:string) {        
    }
    setSummaryTable(table){
        this.summaryTable=table;
    }
    
    setAttentionString(attentionString){
        this.attentionString=attentionString;
    }
    
    getSummaryTable(){
        return this.summaryTable;
    }
    getTitle():string {
        return this.title;
    }
    getFirstLine():string {
        return this.firstLine;
    }
    getSecondLine():string {
        return this.secondLine;
    }    
}
