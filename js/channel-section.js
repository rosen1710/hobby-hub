function loadMessages(sectionId){
    let section=document.getElementById(sectionId);
    section.innerHTML="";
    let messageHtml =`<div class="container lg-6 pt-2" id="${sectionId}-message-container">`;
    //load data



    let fullName="ivan",
    message = "moje",
    createdAt="11/11/2015";
    let isMine = false;
    messageHtml += prepareMessageHtml(fullName, message, createdAt, isMine);
    messageHtml +='</div>';
    section.innerHTML+=messageHtml;
    section.innerHTML+=addMessageForm(sectionId);
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

function addMessageForm(sectionId){
    return `<div name="${sectionId}-form">
        <div class="row pb-2 pt-5">
            <div class="col-10">
                <input name="${sectionId}-message" type="text" id="${sectionId}-message" class="container-fluid form-control">
            </div>
            <div class="col-1">
                <button type="button" id="send-btn" class="col container-fluid form-control" onclick="insertMessage('${sectionId}')">Send</button>
            </div>
        </div>
    </div>`;
}




