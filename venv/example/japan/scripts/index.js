let km  = document.querySelectorAll('.fnd');
let arrKm = [];
let arrDate = [];
let i = 0;


for(let prop of km) {
    let res = prop.querySelector('span');
    arrKm[i] = +[res.textContent.replace(/\D+/g, '')];
    i++;
}

console.log(arrKm);


i = 0;

for(let prop of km) {
    let res = prop.querySelectorAll('span');
    arrDate[i] = [res[res.length - 1].textContent];
    i++;
}

console.log(arrDate);


let row = document.querySelectorAll('.ow-ow');
console.log(row);
let arrOwn = [];





// Our labels and three data series

  
  // All you need to do is pass your configuration as third parameter to the chart function
  var chart = new Chartist.Line('.ct-chart' , {
    labels: arrDate,
    // Naming the series with the series object array notation
    series: [ {
      name: 'series-3',
      data: arrKm
    }]
  }, {
    width: 300,
    height: 400 ,
    //fullWidth: true,
    // Within the series options you can use the series names
    // to specify configuration that will only be used for the
    // specific series.
    series: {
      'series-1': {
        lineSmooth: Chartist.Interpolation.step()
      },
      'series-2': {
        lineSmooth: Chartist.Interpolation.simple(),
        showArea: true
      },
      'series-3': {
        lineSmooth: Chartist.Interpolation.simple(),
        showPoint: true
      }
    }
  }, [
    // You can even use responsive configuration overrides to
    // customize your series configuration even further!
    ['screen and (max-width: 320px)', {
      series: {
        'series-1': {
          lineSmooth: Chartist.Interpolation.none()
        },
        'series-2': {
          lineSmooth: Chartist.Interpolation.none(),
          showArea: false
        },
        'series-3': {
          lineSmooth: Chartist.Interpolation.none(),
          showPoint: true
        }
      }
    }]
  ]);
  

 am4core.ready(function() {

// Themes begin
am4core.useTheme(am4themes_animated);
// Themes end

// Create chart instance
var chart = am4core.create("chartdiv", am4charts.XYChart);

// Add data
chart.data = [{
  "category": "",
  "from": 0,
  "to": 3,
  "name": "Физическое лицо",
  "fill": am4core.color("#0ca948")
}, {
  "category": "",
  "from": 3,
  "to": 5,
  "name": "Физическое лицо",
  "fill": am4core.color("#93da49")
},];

// Create axes
var yAxis = chart.yAxes.push(new am4charts.CategoryAxis());
yAxis.dataFields.category = "category";
yAxis.renderer.grid.template.disabled = true;
yAxis.renderer.labels.template.disabled = true;

var xAxis = chart.xAxes.push(new am4charts.ValueAxis());
xAxis.renderer.grid.template.disabled = true;
xAxis.renderer.grid.template.disabled = true;
xAxis.renderer.labels.template.disabled = false;
xAxis.min = 0;
xAxis.max = 5;

// Create series
var series = chart.series.push(new am4charts.ColumnSeries());
series.dataFields.valueX = "to";
series.dataFields.openValueX = "from";
series.dataFields.categoryY = "category";
series.columns.template.propertyFields.fill = "fill";
series.columns.template.strokeOpacity = 5;
series.columns.template.height = am4core.percent(100);

// Ranges/labels
chart.events.on("beforedatavalidated", function(ev) {
  var data = chart.data;
  for(var i = 0; i < data.length; i++) {
    var range = xAxis.axisRanges.create();
    range.value = data[i].to;
    range.label.text = data[i].to + "%";
    range.label.horizontalCenter = "right";
    range.label.paddingLeft = 5;
    range.label.paddingTop = 5;
    range.label.fontSize = 10;
    range.grid.strokeOpacity = 0.2;
    range.tick.length = 18;
    range.tick.strokeOpacity = 0.2;
  }
});

// Legend
var legend = new am4charts.Legend();
legend.parent = chart.chartContainer;
legend.itemContainers.template.clickable = false;
legend.itemContainers.template.focusable = false;
legend.itemContainers.template.cursorOverStyle = am4core.MouseCursorStyle.default;
legend.align = "right";
legend.data = chart.data;

}); // end am4core.ready()