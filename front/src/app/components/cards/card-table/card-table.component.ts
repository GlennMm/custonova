import { Component, OnInit, Input, ChangeDetectorRef } from "@angular/core";
import { MatSnackBar } from "@angular/material/snack-bar";
import { Papa } from 'ngx-papaparse';
import { HttpService } from "src/app/services/http.service";

@Component({
  selector: "app-card-table",
  templateUrl: "./card-table.component.html",
})
export class CardTableComponent implements OnInit {
  
  file: File = null
  headings = []
  csvData: Array<any[]> = []
  arrayLen = []

  loading = false

  @Input()
  get color(): string {
    return this._color;
  }
  set color(color: string) {
    this._color = color !== "light" && color !== "dark" ? "light" : color;
  }
  private _color = "light";

  constructor(
    private cdr: ChangeDetectorRef,
    private papa: Papa, 
    private http: HttpService, 
    private snackbar: MatSnackBar) {}

  ngOnInit(): void {}

  onFileChange(event) {
    this.loading = true
    this.file = event.target.files[0]
    this.papa.parse(this.file, {
      complete: (result) => {
        this.headings = result.data[0];
        this.csvData = result.data;
        this.csvData.shift()
        this.csvData.forEach(x => this.arrayLen.push(0))
        this.loading = false
      },
      error: (error) => {
        this.loading = false;
        console.log(error)
      }
    });
  }

  clear() {
    this.file = null
    this.headings = []
    this.csvData = []
    this.arrayLen = []
  }

  setTextColor(value: number) {
    if ( 0.0 <= value && value < 0.50) {
      return 'text-emerald-500'
    } else if (0.50 <= value && value < 0.70) {
      return 'text-orange-500'
    } else if (0.70 <= value && value < 1.00) {
      return 'text-red-500'
    } else {
      return 'text-blueGray-500'
    }
  }

  uploadDataset() {
    if (this.file == null) {
      return this.snackbar.open('Please select dataset.', null, { duration: 5000 })
    }
    this.loading = true
    const form = new FormData()
    form.append('dataset', this.file)
    this.http.predict_logositic(form).subscribe(
      (data) => {
        let predictions = data['data']['predictions']
        let probability = data['data']['probability']
        
        for (let i = 0; i < this.csvData.length; i++) {
          this.csvData[i].push(predictions[i].toString())
          this.csvData[i].push(probability[i])
        }
        
        console.log(this.csvData)
        this.loading = false
        this.cdr.detectChanges()
      },
      (err) => {
        this.loading = false
        console.log(err)
      },
      () => {
        this.loading = false
      }
    )
  }

}
