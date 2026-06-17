/**------------------- Page Elements ---------------------------- */

const bytesEnviados = document.querySelector("#bytesEnviados");
const bytesRecebidos  = document.querySelector("#bytesRecebidos");
const pacotesEnviados  = document.querySelector("#pacotesEnviados");
const pacotesRecebidos  = document.querySelector("#pacotesRecebidos");
const erros = document.querySelector("#erros");
const descartes = document.querySelector("#descartes");
const download  = document.querySelector("#download");
const upload  = document.querySelector("#upload");
const ping = document.querySelector("#ping");
const bandwidth = document.querySelector("#bandwidth");
const networkDevicesContainer = document.querySelector("#networkDevicesContainer");



function insertNetworkDevicesIntoContainer(datas){

    datas.forEach(data =>{

        let divContainer = document.createElement("div");
        let divIcon = document.createElement("div");
        let divName = document.createElement("div");
        let divIp = document.createElement("div");
        let divMac = document.createElement("div");
        let divState = document.createElement("div");
        let spanIcon = document.createElement("span");
        let spanName = document.createElement("span");
        let spanIp = document.createElement("span");
        let spanMac = document.createElement("span");
        let spanState = document.createElement("span");
        let img = document.createElement("img");


        divIcon.classList.add("icon");
        divName.classList.add("name");
        divIp.classList.add("ip-address");
        divMac.classList.add("mac-address");
        divState.classList.add("state");

        img.src = "../static/resources/icons/laptop.svg";

        spanIcon.appendChild(img);
        spanName.textContent = data[2];
        spanIp.textContent = data[0];
        spanMac.textContent = data[1];
        spanState.textContent = data[3];

        divIcon.appendChild(spanIcon);
        divName.appendChild(spanName);
        divIp.appendChild(spanIp);
        divMac.appendChild(spanMac);
        divState.appendChild(spanState);

        divContainer.appendChild(divIcon);
        divContainer.appendChild(divName);
        divContainer.appendChild(divIp);
        divContainer.appendChild(divMac);
        divContainer.appendChild(divState);

        networkDevicesContainer.appendChild(divContainer);

    });
    
}



fetch("/api/monitoringPageData")
  .then(res => res.json())
  .then(data => {
    console.log(data);

    bytesEnviados.textContent = Math.round((data[2][0] / (1024 * 1024))) ;
    bytesRecebidos.textContent = Math.round((data[2][1] / (1024 * 1024))) ;
    pacotesEnviados.textContent = Math.round(data[2][2]/1000);
    pacotesRecebidos.textContent = Math.round(data[2][3]/1000);
    erros.textContent = data[2][4];
    descartes.textContent = data[2][5];
    download.textContent = data[0][0].toFixed(1);
    upload.textContent = data[0][1].toFixed(1);
    ping.textContent = data[0][2].toFixed(1);
    bandwidth.textContent = (data[0][0]/8).toFixed(1);
    insertNetworkDevicesIntoContainer(data[1]);
    

});


 // Enable pusher logging - don't include this in production
    Pusher.logToConsole = true;

    var pusher = new Pusher('883a684e6a32327da427', {
      cluster: 'eu'
    });

    var channel = pusher.subscribe('my-channel');

    channel.bind('my-event', function(data) {

        console.log(data);
        console.log(typeof(data));

        download.textContent = data["message"][0].toFixed(1);
        upload.textContent = data["message"][1].toFixed(1);
        ping.textContent = data["message"][2].toFixed(1);
        ping.textContent = (data["message"][0]/8).toFixed(1);

    });

    channel.bind('IOCountersData', function(data) {

        bytesEnviados.textContent = Math.round(data["message"][0]/ (1024 * 1024));
        bytesRecebidos.textContent = Math.round(data["message"][1]/ (1024 * 1024));
        pacotesEnviados.textContent = Math.round(data["message"][2]/1000);
        pacotesRecebidos.textContent = Math.round(data["message"][3]/1000);
        erros.textContent = data["message"][4];
        descartes.textContent = data["message"][5];

    });