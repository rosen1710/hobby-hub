myUserId = 52;
myName = "You";

otherSenderName = "Ivan";

function loadMessages(sectionId){

    fetchMessages(sectionId);

    setInterval(() => {
        fetchMessages(sectionId)
    }, 2000);
}

function fetchMessages(sectionId) {
    fetch('http://localhost:5000/fetch_messages', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            channel_id: 23
        })
    })
    .then(response => response.json())
    .then(data => {
        //console.log(data);
        console.log(data.response);

        section = document.getElementById(sectionId);

        try {
            prev_value = document.getElementById(`${sectionId}-message`).value;
        } catch (error) {
            prev_value = "";
        }
        section.innerHTML="";
        let messageHtml =`<div class="container lg-6 pt-2" id="${sectionId}-message-container">`;

        data.response.forEach(row => {
            let fullName = otherSenderName,
            message = row[1],
            createdAt=row[4].split(".")[0];
            let isMine = false;
            if(row[2] == myUserId) {
                isMine = true;
                fullName = myName;
            }
            messageHtml="";
            messageHtml += prepareMessageHtml(fullName, message, createdAt, isMine);
            messageHtml +='</div>';
            section.innerHTML+=messageHtml;
        });
        section.innerHTML+=addMessageForm(sectionId);
        document.getElementById(`${sectionId}-message`).value = prev_value;
        document.getElementById(`${sectionId}-message`).focus();
    });
}

function prepareMessageHtml(fullName, message, createdAt, isMine) {
    let textStart="start";
    if(isMine){
        textStart = "end"
    }
    return `<div id="general-message-container" class="fs-3 text-${textStart} displayed-message">
        <span class="text-decoration-underline" name="msgAuthor">${fullName} <br></span>
        <span class="fs-2" name="msg">${message} <br></span>
        <span class="fs-6 font-italic" name="msgDate">${createdAt} <br></span>
        </div>`;
}

function addMessageForm(sectionId){
    return `<div name="${sectionId}-form">
        <div class="row pb-2 pt-5">
            <div class="col-9 col-lg-10">
                <input name="${sectionId}-message" type="text" id="${sectionId}-message" class="container-fluid form-control" autofocus>
            </div>
            <div class="col-2 col-lg-1">
                <button type="button" id="send-btn" class="col container-fluid form-control" onclick="insertMessage('${sectionId}')">Send</button>
            </div>
        </div>
    </div>`;
}

function insertMessage(sectionId){
    let messageContainer;
    let distance = 0;
    collection = document.getElementsByClassName("displayed-message");
    for (let i = 0; i < collection.length; i++) {
        if(collection[i].getBoundingClientRect().top>distance){
            messageContainer = collection[i];
            distance = collection[i].getBoundingClientRect().top;
        }
    }
    let messageInput=document.getElementById(sectionId+"-message");
    let newMessage=messageInput.value;
    messageInput.value="";
    let date = new Date().toJSON().split(".")[0];
    date = date.split("T")[0] + " " + date.split("T")[1];
    messageContainer.innerHTML += prepareMessageHtml(myName, newMessage, date, true);

    fetch('http://localhost:5000/create_message', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            text: newMessage,
            user_id: myUserId,
            channel_id: 23
        })
    });
}