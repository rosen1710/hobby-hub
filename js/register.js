let registerForm = document.getElementById('registerForm');
registerForm.addEventListener('submit', register);
function register(event){
    event.preventDefault();
    let formData = new FormData(event.target);
    
    let headersList = {
        // "Access-Control-Allow-Origin": "http://127.0.0.1:5500",
        "Content-Type": "application/json"
    }
       
    let bodyContent = JSON.stringify({
        "email": formData.get('email'),
        "password": formData.get('password'),
        "fullname": formData.get('fullname'),
        "age": formData.get('age'),
        "description": formData.get('description')
    });
    debugger;
    fetch("https://cors-anywhere.herokuapp.com/https://hobby-hub.azurewebsites.net/api/create_user", { 
    // fetch("https://hobby-hub.azurewebsites.net/api/create_user", { 
        method: "POST",
        body: bodyContent,
        headers: headersList
    }).then(()=> {
        window.location.replace("login.html")
    }).catch((e)=> {
        console.log(e.message);
    });
    debugger;
}
