import { Component, OnInit } from "@angular/core";
import { FormBuilder, FormControl, FormGroup, Validators } from "@angular/forms";
import { MatSnackBar } from "@angular/material/snack-bar";
import { Router } from "@angular/router";
import { AuthService } from "src/app/services/auth.service";

@Component({
  selector: "app-register",
  templateUrl: "./register.component.html",
})
export class RegisterComponent implements OnInit {

  registerForm: FormGroup;
  loading = false

  constructor(
    private fb: FormBuilder,
    private router: Router, 
    private authSer: AuthService, 
    private snackbar: MatSnackBar) {
    this.registerForm = this.fb.group({
      'username': new FormControl('', Validators.required),
      'email': new FormControl('', Validators.required),
      'password': new FormControl('', Validators.required),
      'agree': new FormControl(false, Validators.required),
    })
  }

  ngOnInit(): void {}

  register() {
    if (this.registerForm.invalid) {
      return this.snackbar.open('form is invalid', null, { duration: 5000 })
    } else if (this.registerForm.controls['agree'].value == false) {
      return this.snackbar.open('you have to agree to our term and conditions of use', null, { duration: 5000 })
    } else {
      const form = new FormData()
      form.append('username', this.registerForm.controls['username'].value)
      form.append('email', this.registerForm.controls['email'].value)
      form.append('password', this.registerForm.controls['password'].value)
      this.authSer.newUser(form).subscribe(
        (data) => {
          this.loading = false
          this.snackbar.open('You have successfully registered you', null, { duration: 5000 })
          return this.router.navigate(['/auth/login']);
        },
        (err) => {
          this.loading = false
          return this.snackbar.open('Signup failed. Try again.', null, { duration: 5000 })
        },
        () => {
          this.loading = false
        }
      )
    }
  }
}
