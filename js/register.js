let registerForm = document.getElementById('registerForm');
registerForm.addEventListener('submit', register);
function register(event){
    //event.preventDefault();
    let formData = new FormData(event.target);
    formData.forEach((value, key) => {
        console.log(`${key}: ${value}`)
    });

    debugger;
}