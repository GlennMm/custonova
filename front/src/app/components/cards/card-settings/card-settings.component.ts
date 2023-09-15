import { Component, OnInit } from "@angular/core";
import { FormBuilder, FormControl, FormGroup, Validators } from "@angular/forms";
import { MatSnackBar } from "@angular/material/snack-bar";
import { Papa } from "ngx-papaparse";
import { HttpService } from "src/app/services/http.service";

@Component({
  selector: "app-card-settings",
  templateUrl: "./card-settings.component.html",
})
export class CardSettingsComponent implements OnInit {
  
  file: File
  form: FormGroup;
  loading: boolean = false

  elbow_diagram = ''
  data_visualization = ''
  clusters = ''
  data: any

  constructor(
    private papa: Papa,
    private http: HttpService, private fb: FormBuilder, private snackbar: MatSnackBar) {
    this.form = this.fb.group({
      clusters: new FormControl("", Validators.compose([Validators.required, Validators.min(1)])),
      x_axis: new FormControl("", Validators.compose([Validators.required])),
      y_axis: new FormControl("", Validators.compose([Validators.required])),
    })
  }

  selectOptions = [
    'Gender', 'Age', 'Annual Income (k$)', 'Spending Score (1-100)'
  ]

  ngOnInit(): void {}

  selectFile(event) {
    this.file = event.target.files[0]
  }

  uploadDataset() {
    if (this.form.invalid) {
      console.log(this.form.value)
      return this.snackbar.open('form is invalid', null, { duration: 5000 })
    }
    this.loading = true
    const form = new FormData();
    form.append('clusters', this.form.controls['clusters'].value)
    form.append('x_axis', this.form.controls['x_axis'].value)
    form.append('y_axis', this.form.controls['y_axis'].value)
    form.append('dataset',this.file)
    this.http.train_clustering(form).subscribe(
      (data) => {
        this.elbow_diagram = data['elbow']
        this.data_visualization = data['data_visualisation']
        this.clusters = data['clustering_diagram']
        // this.data = data['data']
        // this.table_heading = Object.keys(data['data'])
        // console.log(this.table_heading)
        // for (let i = 0; 1 < 200;i++) {
        //   const row = []
        //   this.table_heading.forEach(col => {
        //     row.push(data['data'][col][i])
        //   })
        //   this.table_data.push(row)
        // }
      },
      (err) => {
        console.log(err)
        this.loading = false
        this.snackbar.open(err.message, null, { duration: 5000 })
      },
      () => this.loading = false
    )
  }

}
