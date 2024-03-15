let msgSend = document.getElementById('msgSend');
msgSend.addEventListener('submit', message);
function message(event){
    event.preventDefault();
    let formData = new FormData(event.target);
    let newMessage=formData.get("message");
    let formName = event.target.name;
    let messageContainerId = formName.replace("-form", "-message-container");
    let container = document.getElementById(messageContainerId);

    container.innerHTML += prepareMessageHtml("test", newMessage, "test", true);
    debugger;
}

function prepareMessageHtml(fullName, message, createdAt, isMine) {
    let textStart="start";
    if(isMine){
        textStart = "end"
    }
    return `<div name="msgOther" class="fs-3 text-${textStart}">
        <span class="text-decoration-underline" name="msgAuthor">${fullName} <br></span>
        <span class="fs-2" name="msg">${message} <br></span>
        <span class="fs-6 font-italic" name="msgDate">${createdAt} <br></span>
        </div>`;
}