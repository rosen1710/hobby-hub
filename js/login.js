let loginForm = document.getElementById('loginForm');
loginForm.addEventListener('submit', login);

async function login(event) {
    event.preventDefault();
    let formData = new FormData(event.target);

    response = await fetch('https://hobby-hub.azurewebsites.net/api/login_user', {
        method: 'POST',
        body: JSON.stringify({
            email: formData.get('email'),
            password: formData.get('password')
        })
    });
    // console.log(response);

    // console.log(response.status);

    data = await response.json();

    // console.log(data);

    if(response.status == 400) {
        alert(data.message);
    }
    else if(response.status == 200) {
        localStorage.setItem("id", data.user.id);
        localStorage.setItem("password", formData.get('password'));
        sessionStorage.setItem("hobbyId", "1");
        sessionStorage.setItem("channelId", "1");
        // alert(data.message);
        window.location.replace("hobby.html");
    }
}