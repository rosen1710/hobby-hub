validationMessage = "Inbalid age"
function registerFunction() {
var inpObj = document.getElementById("age");
  if (inpObj<14){
    document.getElementById("val_msg").innerHTML = inpObj.validationMessage;
  } else {
    document.getElementById("val_msg").innerHTML = "Input OK";
  }
}

function loginFunction() {
    var inpObj = document.getElementById("id1");
      if (!inpObj.checkValidity()) {
        document.getElementById("demo").innerHTML = inpObj.validationMessage;
      } else {
        document.getElementById("demo").innerHTML = "Input OK";
      }
    }

function feedbackFunction() {
var inpObj = document.getElementById("id1");
  if (!inpObj.checkValidity()) {
    document.getElementById("demo").innerHTML = inpObj.validationMessage;
  } else {
    document.getElementById("demo").innerHTML = "Input OK";
  }
}

