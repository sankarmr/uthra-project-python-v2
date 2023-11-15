
var pssword = document.getElementById('password');
var confirmPassword = document.getElementById('repeatPassword');

function validatePassword(){
if (pssword.value != confirmPassword.value){
  confirmPassword.setCustomValidity('Passwords do not match');
  } else {
    confirmPassword.setCustomValidity('');
  }
}

pssword.onchange = validatePassword;
confirmPassword.onkeyup = validatePassword;