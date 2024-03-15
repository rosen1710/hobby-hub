let contactForm = document.getElementById('contactForm');
contactForm.addEventListener('submit', contact);
function contact(event){
    //event.preventDefault();
    let formData = new FormData(event.target);
    formData.forEach((value, key) => {
        console.log(`${key}: ${value}`)
    });

    debugger;
}