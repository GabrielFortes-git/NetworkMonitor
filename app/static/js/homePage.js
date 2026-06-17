const numberDevices = document.querySelector("#numberOfDevices");
const downlaod = document.querySelector("#downloadSpeed");
const  upload = document.querySelector("#uploadSpeed");
const  ping = document.querySelector("#ping");
const  packetsSend = document.querySelector("#packetsSend");
const packetsReceived  = document.querySelector("#packetsReceived");
const devicesContainer = document.querySelector("#devicesContainer");
const alertsContainer = document.querySelector("#alertsContainer");


function displayDevices(data){

    data.forEach(device =>{
        let divContainer = document.createElement("div");
        let div1 = document.createElement("div");
        let div2 = document.createElement("div");
        let divIp = document.createElement("div");
        let divMac = document.createElement("div");
        let divModel = document.createElement("div");
        let img = document.createElement("img");
        let spanIpLabel = document.createElement("span");
        let spanIpData = document.createElement("span");
        let spanMacLabel = document.createElement("span");
        let spanMacData = document.createElement("span");
        let spanModelLabel = document.createElement("span");
        let spanModelData = document.createElement("span");

        div1.classList.add("icon");
        div2.classList.add("details");
        divIp.classList.add("ip-address");
        divMac.classList.add("mac-address");
        divModel.classList.add("model");

        spanIpLabel.textContent = "IP:";
        spanMacLabel.textContent = "MAC:";
        spanModelLabel.textContent = "Model:";
        spanIpData.textContent = device[0];
        spanMacData.textContent = device[1];
        spanModelData.textContent = device[2];

        img.src = "../static/resources/Images/laptop.png";

        div1.appendChild(img)

        divIp.appendChild(spanIpLabel);
        divIp.appendChild(spanIpData);
        divMac.appendChild(spanMacLabel);
        divMac.appendChild(spanMacData);
        divModel.appendChild(spanModelLabel);
        divModel.appendChild(spanModelData);

        div2.appendChild(divIp);
        div2.appendChild(divMac);
        div2.appendChild(divModel);

        divContainer.appendChild(div1)
        divContainer.appendChild(div2)

        devicesContainer.appendChild(divContainer)
        
    });

}
function displayAlerts(data){
    data.forEach(alert =>{

        let divContainer = document.createElement("div");
        let div1 = document.createElement("div");
        let span = document.createElement("span");
        let div2 = document.createElement("div");
        let div2Child = document.createElement("div");

        switch(alert[0]){
            case 6:
                div2Child.classList.add("alertLevel6Color");
            case 8:
                div2Child.classList.add("alertLevel8Color");
            case 10:
                div2Child.classList.add("alertLevel10Color");
        }

        span.textContent = alert[1]
        div1.appendChild(span);

        div2.appendChild(div2Child);

        divContainer.appendChild(div1)
        divContainer.appendChild(div2)

        alertsContainer.appendChild(divContainer);

    });
}


// div><span>Uso do processador muito alto!</span></div>
//                             <div><div></div></div>

const monitoringPageLink = document.querySelector("#monitoringPageLink");

monitoringPageLink.addEventListener("click", function(){
    window.location.href = "{{ url_for('monitoring') }}";
});


fetch("/api/homePageData")
  .then(res => res.json())
  .then(data => {
    console.log(data);
    
    numberDevices.textContent = data[1] ;
    downlaod.textContent = Math.round(data[0][0], 1) ;
    upload.textContent = Math.round(data[0][1], 1) ;
    ping.textContent = Math.round(data[0][2], 1) ;
    packetsSend.textContent = data[2][0] ;
    packetsReceived.textContent = data[2][1] ;
    displayDevices(data[3])
    displayAlerts(data[4])
    console.log(typeof(data[4][0][0]))

});