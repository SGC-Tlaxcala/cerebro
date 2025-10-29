var size = 0;
var placement = 'point';

var style_SECCION_0 = function(feature, resolution){
    var context = {
        feature: feature,
        variables: {}
    };
    var value = ""
    var labelText = "";
    size = 0;
    var labelFont = "12px \'Arial Nova Cond Light\', sans-serif";
    var labelFill = "#ff0101";
    var bufferColor = "#ffffff";
    var bufferWidth = 1.0;
    var textAlign = "center";
    var offsetX = 8;
    var offsetY = 3;
    var placement = 'point';
    if (feature.get("SECCION") !== null) {
        if (feature.get("SECCION") < 10 ) {
            labelText = String("000" + feature.get("SECCION"));    
        }
        if ((feature.get("SECCION") > 9) && (feature.get("SECCION") < 100)) {
            labelText = String("00" + feature.get("SECCION"));    
        } 
        if (feature.get("SECCION") > 99){
            labelText = String("0" + feature.get("SECCION"));
        }
        //labelText = String(feature.get("SECCION"));
    }
    var style = [ new ol.style.Style({
        stroke: new ol.style.Stroke({color: 'rgba(255,0,0,1.0)', lineDash: null, lineCap: 'butt', lineJoin: 'miter', width: 0}),fill: new ol.style.Fill({color: 'rgba(145,82,45,0.0)'}),
        text: createTextStyle(feature, resolution, labelText, labelFont,
                              labelFill, placement, bufferColor,
                              bufferWidth)
    })];

    return style;
};
