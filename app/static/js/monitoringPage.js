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



/**============================================ CHARTS =========================================== */




/*---------------------------------------------------- CHART - BATTERY ---------------------------------------------------------------*/

var options1 = {
  series: [0],
  chart: {
    height: 220,
    type: 'radialBar',
  },
  plotOptions: {
    radialBar: {
      startAngle: -90,
      endAngle: 90,
      track: {
        background: '#e7e7e7',
        strokeWidth: '97%',
        margin: 5,
      },
      dataLabels: {
        name: { show: false },
        value: {
          offsetY: -2,
          fontSize: '32px',
          formatter: function (val) {
            return val + '%'
          },
        },
      },
    },
  },
  fill: {
    type: 'gradient',
    gradient: {
      shade: 'light',
      shadeIntensity: 0.4,
      inverseColors: false,
      opacityFrom: 1,
      opacityTo: 1,
      stops: [0, 50, 53, 91],
    },
  },
  labels: ['Score'],
}



/*---------------------------------------------------- CHART - CPU ---------------------------------------------------------------*/

let cpuData = [];
var cpuLabels = [];

var options2 = {
   chart: {
        id: 'chartCPU',
        type: 'area',
        height: 250,
        animations: {
            enabled: false
        }
    },
  series: [
    {
      name: 'CPU',
      data: [], 
    },
  ],
  dataLabels: {
    enabled: false,
  },
  stroke: {
    curve: 'smooth',
  },
  // CONFIGURAÇÃO DO EIXO Y PARA 0-100%
  yaxis: {
    min: 0,
    max: 100,
    type: 'category',
    categories : [],
    tickAmount: 5, 
    labels: {
      formatter: function (value) {
        return value + "%";
      }
    }
  },
  xaxis: {
    type: 'datetime',
    categories: [
      '2018-09-19T00:00:00.000Z',
      '2018-09-19T01:30:00.000Z',
      '2018-09-19T02:30:00.000Z',
      '2018-09-19T03:30:00.000Z',
      '2018-09-19T04:30:00.000Z',
      '2018-09-19T05:30:00.000Z',
      '2018-09-19T06:30:00.000Z',
    ],
  },
  tooltip: {
    x: {
      format: 'dd/MM/yy HH:mm',
    },
    y: {
      formatter: function (value) {
        return value + "%";
      }
    }
  },
}



/*---------------------------------------------------- CHART - RAM ---------------------------------------------------------------*/

let ramData = [];
let ramLabels = [];


var options3 = {
  chart: {
        id: 'chartRAM',
        type: 'area',
        height: 250,
        animations: {
            enabled: false 
        }
    },
  series: [
    {
      name: 'RAM',
      data: [],
    },
  ],
  colors: ['#64be58'], 
  dataLabels: {
    enabled: false,
  },
  stroke: {
    curve: 'smooth',
  },
   yaxis: {
    min: 0,
    max: 100,
    type: 'category',
    categories : [],
    tickAmount: 5, 
    labels: {
      formatter: function (value) {
        return value + "%";
      }
    }
  },
  xaxis: {
    type: 'datetime',
    categories: [
      '2018-09-19T00:00:00.000Z',
      '2018-09-19T01:30:00.000Z',
      '2018-09-19T02:30:00.000Z',
      '2018-09-19T03:30:00.000Z',
      '2018-09-19T04:30:00.000Z',
      '2018-09-19T05:30:00.000Z',
      '2018-09-19T06:30:00.000Z',
    ],
  },
  tooltip: {
    x: {
      format: 'dd/MM/yy HH:mm',
    },
    y: {
      formatter: function (value) {
        return value + "%";
      }
    }
  },
}


/*---------------------------------------------------- CHART - SWAP ---------------------------------------------------------------*/


var options4 = {
  series: [
    {
      name: 'SWAP',
      data: [0, 0, 0,0 ,0 , 0, 0],
    },
  ],
  colors: ['#daa161'], 
  chart: {
    height: 250,
    type: 'area',
  },
  dataLabels: {
    enabled: false,
  },
  stroke: {
    curve: 'smooth',
  },
   yaxis: {
    min: 0,
    max: 100,
    tickAmount: 5,
    labels: {
      formatter: function (value) {
        return value + "%";
      }
    }
  },
  xaxis: {
    type: 'datetime',
    categories: [
      '2018-09-19T00:00:00.000Z',
      '2018-09-19T01:30:00.000Z',
      '2018-09-19T02:30:00.000Z',
      '2018-09-19T03:30:00.000Z',
      '2018-09-19T04:30:00.000Z',
      '2018-09-19T05:30:00.000Z',
      '2018-09-19T06:30:00.000Z',
    ],
  },
  tooltip: {
    x: {
      format: 'dd/MM/yy HH:mm',
    },
  },
}



/*---------------------------------------------------- CHART - DISK ---------------------------------------------------------------*/


var options5 = {
  series: [44, 55],
  labels : ["Used","Free"],
  chart: {
    width: 280,
    type: 'donut',
  },
  dataLabels: {
    enabled: false,
  },
  responsive: [
    {
      breakpoint: 480,
      options: {
        chart: {
          width: 200,
        },
        legend: {
          show: false,
        },
      },
    },
  ],
  legend: {
    position: 'right',
    offsetY: 0,
    height: 230,
  },
}





/*---------------------------------------------------- CHART - CPU Frequency ---------------------------------------------------------------*/

var options6 = {
  series: [0],
  chart: {
    height: 250,
    type: 'gauge',
  },
  plotOptions: {
    radialBar: {
      hollow: {
        margin: 15,
        size: '70%',
      },
      dataLabels: {
        name: {
          show: true,
          offsetY: -20,
          fontSize: '16px',
          color: '#999',
        },
        value: {
          show: true,
          fontSize: '40px',
          fontWeight: 700,
          offsetY: 6,
          formatter: function (val) {
            return val + '%'
          },
        },
      },
    },
  },
  fill: {
    type: 'gradient',
    gradient: {
      shade: 'dark',
      type: 'horizontal',
      shadeIntensity: 0.5,
      gradientToColors: ['#ABE5A1'],
      inverseColors: true,
      opacityFrom: 1,
      opacityTo: 1,
      stops: [0, 100],
    },
  },
  stroke: {
    lineCap: 'round',
  },
  labels: ['CPU Frequency'],
}





/*---------------------------------------------------- CHART - AVG SYS LOAD---------------------------------------------------------------*/


var options7 = {
  series: [
    {
      name: 'Average System Load',
      data: [1.61133, 0.708496, 0.425293], // Os seus novos dados decimais pequenos
    },
  ],
  chart: {
    type: 'bar',
    height: 250,
  },
  plotOptions: {
    bar: {
      borderRadius: 4,
      borderRadiusApplication: 'end',
      horizontal: true,
    },
  },
  dataLabels: {
    enabled: false,
  },
  xaxis: {
    categories: [
      '1 min',
      '5 min',
      '15 min',
    ],
  },
  yaxis: {
    min: 0,            // Garante que o gráfico começa no zero
    max: 3,            // Limite superior fixo apropriado para os seus dados
    stepSize: 1,       // Força a escala a andar estritamente de 1 em 1 segundo
    labels: {
      formatter: function (value) {
        return value + "s"; // Adiciona o sufixo de segundos aos inteiros (0s, 1s, 2s, 3s)
      }
    }
  }
}


/*==================================================================================================================================================*/

var chartBattery = new ApexCharts(document.querySelector('#chartContainerBattery'), options1)
chartBattery.render()


var chartCPU = new ApexCharts(document.querySelector('#chartContainerCPU'), options2)
chartCPU.render()

var chartRAM = new ApexCharts(document.querySelector('#chartContainerRAM'), options3)
chartRAM.render()

var chartSWAP = new ApexCharts(document.querySelector('#chartContainerSWAP'), options4)
chartSWAP.render()



var chartDisk = new ApexCharts(document.querySelector('#chartContainerDisk'), options5)
chartDisk.render()

var chartCPUFreq = new ApexCharts(document.querySelector('#chartContainerCPUFreq'), options6)
chartCPUFreq.render()

var chartSysLoad = new ApexCharts(document.querySelector('#chartContainerSysLoad'), options7)
chartSysLoad.render()