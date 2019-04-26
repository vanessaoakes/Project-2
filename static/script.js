var map;
function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: 37.7749, lng: -122.42},
        zoom: 12


    });
    var transitLayer = new google.maps.TransitLayer();
    transitLayer.setMap(map);
    populate_markers()
}
function populate_markers(){
    d3.json("/houses", function(info){
        for (var i=0; i <info.length; i++){
            var house = info[i]
            
            var myLatlng = new google.maps.LatLng(house["latitude"],house["longitude"])
            let marker = new google.maps.Marker({
                position: myLatlng,
                title: house["address"]

            });     
            
            var contentString = "Address: " +house["address"] +
            "<br/>" +
            "Sold Price: $" + house["sold_price"]+
            "<br/>" +
            "Bedroom Count: " + house["bedroom"] +
            "<br/>" +
            "Bathroom Count: " +house["bathroom"] +
            "<br/>" +
            "Square Feet: " + house["sq_ft"] +
            "<br/>" +
            "Days On Market: " + house["days_on_market"] +
            "<br/>"

            let infowindow = new google.maps.InfoWindow({
                content: contentString
            });

            marker.addListener('click', function(){
                infowindow.open(map,marker);
            });marker.setMap(map);  
        }
    console.log(info)
    })
}

d3.json("/bar", function(info){

    console.log(info)
    
    var trace1 = {
        x:info["x"],
        y:info["y"],
        name: 'Average Sold Price by Neighborhood',
        type: 'bar'        
    };
    var layout = {
        barmode: 'group',
        xaxis: {type: "category"},
        title: "Average Sold Price by Neighborhood",

};
    Plotly.newPlot('bar', [trace1], layout);
})


d3.json("/percentage", function(info){

    console.log(info)
    
    var trace1 = {
        x:info["x"],
        y:info["y"],
        name: 'Percentage Over Asking by Neighborhood',
        type: 'bar'        
    };
    var layout = {
        barmode: 'group',
        xaxis: {type: "category"},
        title: "Percentage Over/Under Asking by Neighborhood",

    };
    Plotly.newPlot('percentage', [trace1], layout);
})
