export class SuccessSummary  {    
    //title:string = null;
    //firstLine:string = null;
    //secondLine:string = null;
    summaryTable=[]
    constructor(public title:string,
                public firstLine:string,
                public secondLine:string) {        
    }
    setSummaryTable(table){
        this.summaryTable=table;
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
