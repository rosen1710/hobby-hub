let loginForm = document.getElementById('loginForm');
loginForm.addEventListener('submit', login);
function login(event){
    //event.preventDefault();
    let formData = new FormData(event.target);
    formData.forEach((value, key) => {
        console.log(`${key}: ${value}`)
    });
    debugger;
}