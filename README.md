# Leaflet, D3/Crossfilter, jQuery, and African-American Residence Populations

## Demos
[Interactive Mapping Chart](https://hopetambala.github.io/Bentley-Mapping-Project/)

![screencap](resources/project_gif.gif)

## Description
The goal of this project is to use mapping technologies such as Leaflet to understand African American residence populations from 1853 to 1973. Through the use 

The data was queried into a Pandas to allow for easier data manipulation. CSVs of the data were generated and placed into the Aframe folder. Using python to clean and manipuate the data we received, we present markers using Crossfilter/D3 to represent markers that demonstrate the residences over time. 

## Libraries
[Leaflet](https://leafletjs.com/)

[Cross Filter](https://square.github.io/crossfilter/)

[D3.js](https://d3js.org/)

## Project Layout
    ├── data                # Folder for data that's been aggregated and manipulated for the map
    ├── photos              # Folder for even markers on the Leaflet map 
    ├── resources           # Resources for reference   
    ├── index.html          # Main fil
    └── README.md

## Build and run

### Server 
Run the following in the main/root folder of this project to start your own server
```
python -m SimpleHTTPServer
```

## Development

### HTML
We have three key HTMl elements to recognize 

1) Leaflet Map
```
<div id="map"></div>
```

2) Crossfilter for the markers on the map
```
<svg width=400 height=90 id="slider-range"></svg>
```

3) jQuery Slider for the opacity of the two maps we're comparing
```
<div id="slider-opaque"></div>
```

### JavaScript

We have various functions to programmatically generate markers(using leaflet's `icon` ) for our leaflet map

#### Custom Markers
```
function customizeMarker(color){
    """
    ...Styling Stuff
    """

    var icon = L.divIcon({
        className: "my-custom-pin",
        iconAnchor: [0, 24],
        labelAnchor: [-6, 0],
        popupAnchor: [0, -36],
        html: `<span style="${markerNarrativeHtmlStyles}" />`
    })

    return icon;
}
```

#### Marker Clustering
For [marker clustering](https://github.com/Leaflet/Leaflet.markercluster), we create a function to separate Residence marker clusters and Events marker clusters. Case 1 is for Residence Markers and Case 2 is for Event Markers.
```
function initialMarkerClusters(type){
    var uniqueClass;

    var groupToReturn = new L.markerClusterGroup({
        spiderfyOnMaxZoom: true,
        showCoverageOnHover: true,
        zoomToBoundsOnClick: true,
        singleMarkerMode: false,
        iconCreateFunction: function(cluster){
            count = 0;
            cluster.getAllChildMarkers().forEach(function(child){
                count = (type == 1) ? (count + parseInt(child.feature.properties.Count)) : (count + 1);
            });
            return L.divIcon({
                className:`marker-cluster ${uniqueClass}`,
                iconSize: new L.Point(40,40),
                html: `<div><span >` + count + '</span></div>'
            });
        }
    })

    switch (type) {
        case 1:
            uniqueClass = "marker-cluster-large";
            groupToReturn.options.maxClusterRadius = 120;
            break;
        case 2:
            uniqueClass = "marker-cluster-large_nav";
            groupToReturn.options.maxClusterRadius = 1;
    }

    return groupToReturn;
}
```

#### Pins and Narratives
In order to display actual information on custom markers we create, we bind popups to each icon. Accomodations/residences and events have different types of information we want to display so we have different popups(i.e. different functions) for each popup.

Accomodations and Residences
```
function renderPins(accommodation_markers, geoJson){
        customizedIcon = customizeMarker(markColors['residence']); //Here we use the customizeMarker() funciton we created earier 

        /* 
        ...
        Code to create popups
        ...
        */
        
        map.addLayer(accommodation_markers); //add a layer to our map
    }
```

Events Function
```
function renderNarrativePins(event_markers, geoJsonURL){
    customizedIcon = customizeMarker(markColors['event']);
    $.getJSON(geoJsonURL, function(data){
        /* 
        ...
        Code to create popups
        ...
        */
        
        event_markers.addLayer(geojson);
        map.addLayer(event_markers);
    });
}
```

#### Crossfilter Data
In order to manage the markers on the map, we created a crossfilter slider that also displays the number of students per year.
Here we used [dc.js](http://dc-js.github.io/dc.js/) specifically its [filtering](http://dc-js.github.io/dc.js/examples/filtering.html) example.

Here we create a barchart and attach it to the id `slider-range`.
```
var geoChart  = dc.barChart("#slider-range");
```

We access the `GEOJSON` file we prepared separately and change the counts from strings to numbers.
```
var geoData = GEOJSON["features"]

geoData.forEach(function(d) {
    d.properties.Count = +d.properties.Count
});
```

We set up our crossfilter and create filters based on values we need for the barchart. We need to 1) get the year from date and 2) reduce and group the sum of students per year
```
var ndx = crossfilter(geoData),
    yearDim  = ndx.dimension(function(d) {return +d.properties.Date;}),
    countPerYear = yearDim.group().reduceSum(function(d) {return +d.properties.Count;}),
```

After manually capping the extent of years of data we want to access, we create a barchart and render it with a brush ontop of it that filters by year.
```
min = 1853 
max = 1973 

geoChart
    .height(100)
    .dimension(yearDim)
    .group(countPerYear)
    .x(d3.scaleLinear().domain([min,max]))
    .elasticY(true)
    .controlsUseVisibility(true)
    .on('renderlet',function(){
        ///Logic for re-rendering markers for map
        var newGeoJson = {
            "type" : "Feature Collection",
            "features": []
        };

        //Check if that data is updating
        console.log(yearDim.top(Infinity))
        console.log(GEOJSON["features"])

        //Add new pins based on data created from the crossfilter
        for(let i=0; i < yearDim.top(Infinity).length;i++){
            newGeoJson["features"].push(yearDim.top(Infinity)[i])
        }
        renderPins(accommodation_markers,newGeoJson);
    });

geoChart.xAxis().tickFormat(function(d) {return d}); // convert back to base unit
geoChart.yAxis().ticks(2);

dc.renderAll();
```

#### Setting up the map
