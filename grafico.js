ctx = document.getElementById('graficoDificultad');
 
const DATA_COUNT = 7;
const NUMBER_CFG = {count: DATA_COUNT, rmin: 1, rmax: 1, min: 0, max: 100};

const data = {
  datasets: [
    {
      label: 'Faciles',
      data: {{ dificultades_distancias }},
      borderColor: 'rgb(150, 220, 150)',
      backgroundColor: 'rgb(150, 220, 150)',
    },
    {
      label: 'Moderados',
      data: [{
          x: -10,
          y: 0
        }, {
          x: 0,
          y: 13
      }],
      borderColor: 'rgb(220, 150, 150)',
      backgroundColor: 'rgb(220, 150, 150)',
    },
    {
      label: 'Dificiles',
      data: [{
          x: -10,
          y: 0
        }, {
          x: 0,
          y: 7
      }],
      borderColor: 'rgb(150, 150, 220)',
      backgroundColor: 'rgb(150, 150, 220)',
    }
  ]
};
  
const config = {
    type: 'scatter',
    data: data,
    options: {
    responsive: true,
    plugins: {
    legend: {
        position: 'top',
    },
    title: {
        display: true,
        text: 'Grafico dificultad'
    }
    }
},
};
    
  
new Chart(ctx, {
    type: 'scatter',
    data: data,
    config: config,
    options: {
        
    }
});
