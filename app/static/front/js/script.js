const psw = document.getElementById("password");
const pswIcon = document.getElementById("show-psw-icon");

// show & hide text in password input
let pswVisibility = false;
function showPsw(input, icon,eye,eyeoff) {
  if (pswVisibility) {
    console.log("pswVisibility: ", );
    input.setAttribute("type", "password");
    icon.setAttribute("src", eye);
    pswVisibility = false;
  } else {
    console.log("pswVisibility: ", );
    input.setAttribute("type", "text");
    icon.setAttribute("src", eyeoff);
    pswVisibility = true;
  }
}
