async function loadHobbies() {
    let response = await fetch('https://hobby-hub.azurewebsites.net/api/fetch_hobbies', {
        method: "POST"
    });
    if(response.status == 200) {
        let data = await response.json()
        document.getElementById("hobbies-list").innerHTML = "";
        data.hobbies.forEach(element => {
            document.getElementById("hobbies-list").innerHTML += `
                <li>
                    <button onclick="openHobby(${element.id})">${element.name}</button>
                </li>
            `;
            if(element.id == sessionStorage.getItem("hobbyId")) {
                document.getElementById("hobby-name").innerHTML = element.name;
            }
        });
    }
}

async function openHobby(hobbyId) {
    if(hobbyId != undefined) {
        sessionStorage.setItem("hobbyId", hobbyId);
    }
    loadHobbies();
    let response = await fetch('https://hobby-hub.azurewebsites.net/api/fetch_channels', {
        method: "POST",
        body: JSON.stringify({
            hobby_id: sessionStorage.getItem("hobbyId")
        })
    });
    if(response.status == 200) {
        let data = await response.json()
        let first = "active";
        document.getElementById("nav-tab").innerHTML = "";
        data.channels.forEach(element => {
            document.getElementById("nav-tab").innerHTML += `
                <button class="col-lg-2 nav-link fs-3 ${first}" id="${first}tab" data-bs-toggle="tab" data-bs-target="#general" type="button" role="tab" aria-controls="nav-general" aria-selected="true" onclick="loadMessages(${element.id})">${element.name}</button>
            `;
            if(first != "") {
                sessionStorage.setItem("channelId", element.id)
            }
            first = "";
        });
        document.getElementById("activetab").click();
        document.getElementById("close-button").click();
    }
}