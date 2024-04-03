let registerForm = document.getElementById('registerForm');
registerForm.addEventListener('submit', register);

async function register(event) {
    event.preventDefault();
    let formData = new FormData(event.target);

    response = await fetch('https://hobby-hub.azurewebsites.net/api/create_user', {
        method: 'POST',
        body: JSON.stringify({
            email: formData.get('email'),
            password: formData.get('password'),
            fullname: formData.get('fullname'),
            age: Number(formData.get('age')),
            description: formData.get('description')
        })
    });
    // console.log(response);

    // console.log(response.status);

    data = await response.json();

    if(response.status == 400) {
        alert(data.message);
    }
    else if(response.status == 200) {
        window.location.replace("login.html");
    }
}