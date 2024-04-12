var myName = "You";

var channelId = 1;

function showForm() {
    if(localStorage.getItem("id") != null && localStorage.getItem("password") != null) {
        document.getElementById("message-form").innerHTML = `
            <div class="row pb-2" style="padding-top: 10px;">
                <div class="col-9 col-lg-10">
                    <textarea name="message-text" type="text" id="message-text" style="height: 94px; min-height: 94px;" class="container-fluid form-control" autofocus></textarea>
                </div>
                <div class="col-2 col-lg-1">
                    <button type="button" id="send-btn" style="box-sizing: unset; height: 80px;" class="col container-fluid form-control" onclick="insertMessage()">Send</button>
                </div>
            </div>`;
    }
    else {
        document.getElementById("message-form").innerHTML = `
            <p style="font-size: 24px;">You must log in to send messages!</p>`;
    }
}

function loadMessages() {

    fetchMessages();

    setInterval(() => {
        fetchMessages()
    }, 180000);
}

async function fetchMessages() {
    let response = await fetch('https://hobby-hub.azurewebsites.net/api/fetch_messages', {
        method: 'POST',
        body: JSON.stringify({
            channel_id: channelId
        })
    });
    // console.log(response);

    // console.log(response.status);

    let data = await response.json();

    // console.log(data);

    // console.log(data.messages);

    let section = document.getElementById("messages-container");

    section.innerHTML = "";

    data.messages.forEach(row => {
        let fullName = row.user_fullname;
        let message = row.text;
        let createdAt = row.created_at.split(".")[0];
        let isMine = false;
        if(row.user_id == localStorage.getItem("id")) {
            isMine = true;
            fullName = myName;
        }
        let text = "";
        for(let i = 0; i < message.length; i++) {
            if(message[i] != "\n") {
                text += message[i];
            }
            else {
                text += "<br>";
            }
        }
        section.innerHTML += prepareMessageHtml(fullName, text, createdAt, isMine);
    });
    document.getElementById("content-container").scrollTop = document.getElementById("content-container").scrollHeight;
}

function prepareMessageHtml(fullName, message, createdAt, isMine) {
    let textStart = "start";
    if(isMine) {
        textStart = "end"
    }
    return `<div id = "general-message-container" class = "fs-3 text-${textStart} displayed-message">
        <span class = "text-decoration-underline" name = "msgAuthor"><br>${fullName}<br></span>
        <span class = "fs-2" name = "msg">${message}<br></span>
        <span class = "fs-6 font-italic" name = "msgDate">${createdAt}<br></span>
        </div>`;
}

async function insertMessage() {
    let newMessage = document.getElementById("message-text").value;
    document.getElementById("message-text").value = "";

    if(newMessage == "") {
        return;
    }

    let response = await fetch('https://hobby-hub.azurewebsites.net/api/create_message', {
        method: 'POST',
        body: JSON.stringify({
            text: newMessage,
            user_id: localStorage.getItem("id"),
            password: localStorage.getItem("password"),
            channel_id: channelId
        })
    });
    if(response.status == 200) {
        let messageContainer;
        let distance = 0;
        let collection = document.getElementsByClassName("displayed-message");
        for (let i = 0; i < collection.length; i++) {
            if(collection[i].getBoundingClientRect().top > distance) {
                messageContainer = collection[i];
                distance = collection[i].getBoundingClientRect().top;
            }
        }

        let date = new Date().toJSON().split(".")[0];
        date = date.split("T")[0] + " " + date.split("T")[1];

        let text = "";
        for(let i = 0; i < newMessage.length; i++) {
            if(newMessage[i] != "\n") {
                text += newMessage[i];
            }
            else {
                text += "<br>";
            }
        }
        messageContainer.innerHTML += prepareMessageHtml(myName, text, date, true);
        document.getElementById("content-container").scrollTop = document.getElementById("content-container").scrollHeight;
    }
    fetchMessages();
}