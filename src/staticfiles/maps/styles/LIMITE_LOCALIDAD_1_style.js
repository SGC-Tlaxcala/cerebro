var size = 0;
var placement = 'point';

var style_LIMITE_LOCALIDAD_1 = function(feature, resolution){
    var context = {
        feature: feature,
        variables: {}
    };
    var value = ""
    var labelText = "";
    size = 0;
    var labelFont = "10.4px \'Arial Nova Cond Light\', sans-serif";
    var labelFill = "#000000";
    var bufferColor = "#ffffff";
    var bufferWidth = 1.0;
    var textAlign = "center";
    var offsetX = 8;
    var offsetY = 3;
    var placement = 'point';
    if (feature.get("NOMBRE") !== null) {
        if (feature.get("LOCALIDAD") < 10) {
            labelText = String("(000" + feature.get("LOCALIDAD") + ") " + feature.get("NOMBRE"));  
        } 
        if ((feature.get("LOCALIDAD") > 9) && (feature.get("LOCALIDAD") < 100)) {
            labelText = String("(00" + feature.get("LOCALIDAD") + ") " + feature.get("NOMBRE"));  
        }
        if (feature.get("LOCALIDAD") > 99) {
            labelText = String("(0" + feature.get("LOCALIDAD") + ") " + feature.get("NOMBRE"));  
        }
        //labelText = String(feature.get("NOMBRE"));
    }
    var style = [ new ol.style.Style({
        stroke: new ol.style.Stroke({color: 'rgba(0, 158, 137,1.0)', lineDash: null, lineCap: 'butt', lineJoin: 'miter', width: 2}),fill: new ol.style.Fill({color: 'rgba(175,239,184,0.5)'}),
        text: createTextStyle(feature, resolution, labelText, labelFont,
                              labelFill, placement, bufferColor,
                              bufferWidth)
    })];

    return style;
};
