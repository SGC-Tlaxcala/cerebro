var size = 0;
var placement = 'point';

var style_DISTRITO_FEDERAL_4 = function(feature, resolution){
    var context = {
        feature: feature,
        variables: {}
    };
    var value = ""
    var labelText = "";
    size = 0;
    var labelFont = "20px \'Arial Nova Cond Light\', sans-serif";
    var labelFill = "#000000";
    var bufferColor = "";
    var bufferWidth = 0;
    var textAlign = "center";
    var offsetX = 8;
    var offsetY = 3;
    var placement = 'point';
    if (feature.get("DISTRITO") !== null) {
        labelText = String("DISTRITO FEDERAL" + "\n" + "0" + feature.get("DISTRITO"));
    }
    var style = [ new ol.style.Style({
        stroke: new ol.style.Stroke({color: 'rgba(1,103,255,1.0)', lineDash: null, lineCap: 'butt', lineJoin: 'miter', width: 3}),fill: new ol.style.Fill({color: 'rgba(1,103,255,0.0)'}),
        text: createTextStyle(feature, resolution, labelText, labelFont,
                              labelFill, placement, bufferColor,
                              bufferWidth)
    })];

    return style;
};
