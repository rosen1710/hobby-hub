function insertMessage(sectionId){
    let messageContainer=document.getElementById(sectionId+"-message-container");
    let messageInput=document.getElementById(sectionId+"-message");
    let newMessage=messageInput.value;
    messageInput.value="";
    messageContainer.innerHTML += prepareMessageHtml("test", newMessage, "test", true);

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

