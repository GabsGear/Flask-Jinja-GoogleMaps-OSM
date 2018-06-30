# coding: utf-8

from flask import Flask, render_template
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map, icons
import tratamento

app = Flask(__name__, template_folder="templates")
app.config['GOOGLEMAPS_KEY'] = "AIzaSyALZI01uvpbpHjBzEVZPdsCcjXdRyK2NEU"
GoogleMaps(app, key="AIzaSyALZI01uvpbpHjBzEVZPdsCcjXdRyK2NEU")
opg = tratamento.OpenStreetGabs()

@app.route('/')
def map_view():

    lati, loni = opg.getCoord(opg.getInicial())
    latf, lonf = opg.getCoord(opg.getFinal())
    estradas = opg.createZipPath()
    locations = estradas

    polyline = {
        'stroke_color': '#0AB0DE',
        'stroke_opacity': 1.0,
        'stroke_weight': 3,
    }

    plinemap = Map(
        identifier="plinemap",
        varname="plinemap",
        lat=lati,
        lng=loni,
        polylines=[polyline, estradas],
        markers={
            icons.dots.green: [(lati, loni, "Inicio")],
            icons.dots.blue: [(latf, lonf, "Fim")],
        }
    )
    
    init = Map(
        identifier="init",
        varname="init",
        lat=lati,
        lng=loni,
        markers={
            icons.dots.green: [(lati, loni, "Inicio")],
            icons.dots.blue: [(latf, lonf, "Fim")]
        }
    )

    bestWay = Map(
        identifier="bestWay",
        varname="bestWay",
        lat=locations[0][0],
        lng=locations[0][1],
        markers=[(loc[0], loc[1]) for loc in locations],
        fit_markers_to_bounds = True
    )
    return render_template('plot.html', init = init, bestWay=bestWay, plinemap=plinemap)

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)