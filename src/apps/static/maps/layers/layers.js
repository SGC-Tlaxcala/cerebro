var wms_layers = [];

var format_SECCION_0 = new ol.format.GeoJSON();
var features_SECCION_0 = format_SECCION_0.readFeatures(json_SECCION_0,
            {dataProjection: 'EPSG:4326', featureProjection: 'EPSG:3857'});
var jsonSource_SECCION_0 = new ol.source.Vector({
    attributions: ' ',
});
jsonSource_SECCION_0.addFeatures(features_SECCION_0);
var lyr_SECCION_0 = new ol.layer.Vector({
                declutter: true,
                source:jsonSource_SECCION_0,
                style: style_SECCION_0,
                interactive: true,
                title: '<img src="/static/maps/styles/legend/SECCION_0.png" /> SECCION'
            });
var format_LIMITE_LOCALIDAD_1 = new ol.format.GeoJSON();
var features_LIMITE_LOCALIDAD_1 = format_LIMITE_LOCALIDAD_1.readFeatures(json_LIMITE_LOCALIDAD_1,
            {dataProjection: 'EPSG:4326', featureProjection: 'EPSG:3857'});
var jsonSource_LIMITE_LOCALIDAD_1 = new ol.source.Vector({
    attributions: ' ',
});
jsonSource_LIMITE_LOCALIDAD_1.addFeatures(features_LIMITE_LOCALIDAD_1);
var lyr_LIMITE_LOCALIDAD_1 = new ol.layer.Vector({
                declutter: true,
                source:jsonSource_LIMITE_LOCALIDAD_1,
                style: style_LIMITE_LOCALIDAD_1,
                interactive: true,
                title: '<img src="/static/maps/styles/legend/LIMITE_LOCALIDAD_1.png" /> LIMITE_LOCALIDAD'
            });
var format_MUNICIPIO_2 = new ol.format.GeoJSON();
var features_MUNICIPIO_2 = format_MUNICIPIO_2.readFeatures(json_MUNICIPIO_2,
            {dataProjection: 'EPSG:4326', featureProjection: 'EPSG:3857'});
var jsonSource_MUNICIPIO_2 = new ol.source.Vector({
    attributions: ' ',
});
jsonSource_MUNICIPIO_2.addFeatures(features_MUNICIPIO_2);
var lyr_MUNICIPIO_2 = new ol.layer.Vector({
                declutter: true,
                source:jsonSource_MUNICIPIO_2,
                style: style_MUNICIPIO_2,
                interactive: true,
                title: '<img src="/static/maps/styles/legend/MUNICIPIO_2.png" /> MUNICIPIO'
            });
var format_DISTRITO_LOCAL_3 = new ol.format.GeoJSON();
var features_DISTRITO_LOCAL_3 = format_DISTRITO_LOCAL_3.readFeatures(json_DISTRITO_LOCAL_3,
            {dataProjection: 'EPSG:4326', featureProjection: 'EPSG:3857'});
var jsonSource_DISTRITO_LOCAL_3 = new ol.source.Vector({
    attributions: ' ',
});
jsonSource_DISTRITO_LOCAL_3.addFeatures(features_DISTRITO_LOCAL_3);
var lyr_DISTRITO_LOCAL_3 = new ol.layer.Vector({
                declutter: true,
                source:jsonSource_DISTRITO_LOCAL_3,
                style: style_DISTRITO_LOCAL_3,
                interactive: true,
                title: '<img src="/static/maps/styles/legend/DISTRITO_LOCAL_3.png" /> DISTRITO_LOCAL'
            });
var format_DISTRITO_FEDERAL_4 = new ol.format.GeoJSON();
var features_DISTRITO_FEDERAL_4 = format_DISTRITO_FEDERAL_4.readFeatures(json_DISTRITO_FEDERAL_4,
            {dataProjection: 'EPSG:4326', featureProjection: 'EPSG:3857'});
var jsonSource_DISTRITO_FEDERAL_4 = new ol.source.Vector({
    attributions: ' ',
});
jsonSource_DISTRITO_FEDERAL_4.addFeatures(features_DISTRITO_FEDERAL_4);
var lyr_DISTRITO_FEDERAL_4 = new ol.layer.Vector({
                declutter: true,
                source:jsonSource_DISTRITO_FEDERAL_4,
                style: style_DISTRITO_FEDERAL_4,
                interactive: true,
                title: '<img src="/static/maps/styles/legend/DISTRITO_FEDERAL_4.png" /> DISTRITO_FEDERAL'
            });
var format_ENTIDAD_5 = new ol.format.GeoJSON();
var features_ENTIDAD_5 = format_ENTIDAD_5.readFeatures(json_ENTIDAD_5,
            {dataProjection: 'EPSG:4326', featureProjection: 'EPSG:3857'});
var jsonSource_ENTIDAD_5 = new ol.source.Vector({
    attributions: ' ',
});
jsonSource_ENTIDAD_5.addFeatures(features_ENTIDAD_5);
var lyr_ENTIDAD_5 = new ol.layer.Vector({
                declutter: true,
                source:jsonSource_ENTIDAD_5,
                style: style_ENTIDAD_5,
                interactive: true,
                title: '<img src="/static/maps/styles/legend/ENTIDAD_5.png" /> ENTIDAD'
            });

lyr_SECCION_0.setVisible(true);lyr_LIMITE_LOCALIDAD_1.setVisible(true);lyr_MUNICIPIO_2.setVisible(true);lyr_DISTRITO_LOCAL_3.setVisible(true);lyr_DISTRITO_FEDERAL_4.setVisible(true);lyr_ENTIDAD_5.setVisible(true);
var layersList = [lyr_SECCION_0,lyr_LIMITE_LOCALIDAD_1,lyr_MUNICIPIO_2,lyr_DISTRITO_LOCAL_3,lyr_DISTRITO_FEDERAL_4,lyr_ENTIDAD_5];
lyr_SECCION_0.set('fieldAliases', {'SECCION': 'SECCION', 'TIPO': 'TIPO', 'PRODUCTO': 'PRODUCTO', });
lyr_LIMITE_LOCALIDAD_1.set('fieldAliases', {'LOCALIDAD': 'LOCALIDAD', 'NOMBRE': 'NOMBRE', 'PRODUCTO': 'PRODUCTO', });
lyr_MUNICIPIO_2.set('fieldAliases', {'MUNICIPIO': 'MUNICIPIO', 'NOMBRE': 'NOMBRE', 'PRODUCTO': 'PRODUCTO', });
lyr_DISTRITO_LOCAL_3.set('fieldAliases', {'DISTRITO_LOCAL': 'DISTRITO_LOCAL', 'PRODUCTO': 'PRODUCTO', });
lyr_DISTRITO_FEDERAL_4.set('fieldAliases', {'DISTRITO': 'DISTRITO', 'PRODUCTO': 'PRODUCTO', });
lyr_ENTIDAD_5.set('fieldAliases', {'ENTIDAD': 'ENTIDAD', 'NOMBRE': 'NOMBRE', 'PRODUCTO': 'PRODUCTO', });
lyr_SECCION_0.set('fieldImages', {'SECCION': 'TextEdit', 'TIPO': 'TextEdit', 'PRODUCTO': 'TextEdit', });
lyr_LIMITE_LOCALIDAD_1.set('fieldImages', {'LOCALIDAD': 'Range', 'NOMBRE': 'TextEdit', 'PRODUCTO': 'TextEdit', });
lyr_MUNICIPIO_2.set('fieldImages', {'MUNICIPIO': 'TextEdit', 'NOMBRE': 'TextEdit', 'PRODUCTO': 'TextEdit', });
lyr_DISTRITO_LOCAL_3.set('fieldImages', {'DISTRITO_LOCAL': 'TextEdit', 'PRODUCTO': 'TextEdit', });
lyr_DISTRITO_FEDERAL_4.set('fieldImages', {'DISTRITO': 'TextEdit', 'PRODUCTO': 'TextEdit', });
lyr_ENTIDAD_5.set('fieldImages', {'ENTIDAD': 'Range', 'NOMBRE': 'TextEdit', 'PRODUCTO': 'TextEdit', });
lyr_SECCION_0.set('fieldLabels', {'SECCION': 'header label', 'TIPO': 'no label', 'PRODUCTO': 'no label', });
lyr_LIMITE_LOCALIDAD_1.set('fieldLabels', {'LOCALIDAD': 'header label', 'NOMBRE': 'no label', 'PRODUCTO': 'no label', });
lyr_MUNICIPIO_2.set('fieldLabels', {'MUNICIPIO': 'header label', 'NOMBRE': 'no label', 'PRODUCTO': 'no label', });
lyr_DISTRITO_LOCAL_3.set('fieldLabels', {'DISTRITO_LOCAL': 'header label', 'PRODUCTO': 'no label', });
lyr_DISTRITO_FEDERAL_4.set('fieldLabels', {'DISTRITO': 'header label', 'PRODUCTO': 'no label', });
lyr_ENTIDAD_5.set('fieldLabels', {'ENTIDAD': 'header label', 'NOMBRE': 'no label', 'PRODUCTO': 'no label', });
lyr_ENTIDAD_5.on('precompose', function(evt) {
    evt.context.globalCompositeOperation = 'normal';
});
