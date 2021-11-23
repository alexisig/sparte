var info = L.control()
var legend = L.control({position: 'bottomright'});

///// HELPER FUNCTIONS

// cast "True" or "False" to true or false
function cast(value){
    return (value == "True")  ? true  :
           (value == "False") ? false :
                                value
}

// equivalent of dict().get(field, default_value) from python
function get(object, key, default_value) {
    let result = object[key]
    if (typeof result !== "undefined")
        return cast(result)
    else
        return default_value
}

/////////////////////////////////////////////////
// Styling function according to properties
/////////////////////////////////////////////////

// used by legend
function getColor(d) {
    return d > 90 ? '#800026' :
           d > 70 ? '#BD0026' :
           d > 50 ? '#E31A1C' :
           d > 40 ? '#FC4E2A' :
           d > 30 ? '#FD8D3C' :
           d > 20 ? '#FEB24C' :
           d > 10 ? '#FED976' :
                    '#FFEDA0'
}

function emprise_style(feature) {
    return {
        // background options
        fill: false,
        // border (or stoke) options
        weight: 2,
        opacity: 1,
        color: 'red',
        dashArray: '10',
        fillOpacity: 0
    }
}

/////////////////////////
// INITIALISATION
/////////////////////////

function Carto (map_center, default_zoom)
{
    this.map_center = map_center
    this.default_zoom = default_zoom

    //this.layerControl = L.control.layers(null, null)
    this.info = L.control({position: 'bottomleft'})
    this.legend = L.control({position: 'bottomright'});
    this.map = L.map('mapid')

    // contains all added geolayer (see add_geolayer function)
    this.geolayers = []

    // contains all panes. Usefull to ordering the geolayer
    // Each panes has a specific z-index
    this.panes = []

    this.init = (geolayers) => {
        // Initialize map
        this.map.setView(this.map_center, this.default_zoom)

        for (i=0; i<10; i++)
        {
            let pane_name = `level_${i}`
            let pane = this.map.createPane(pane_name)
            pane.style.zIndex = 505 + 10 * i
            this.panes.push(pane_name)
        }

        // Choix du fond de carte
        L.tileLayer( 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>- Beta Gouv.',
            subdomains: ['a','b','c']
        }).addTo( this.map )
        // add info div
        this.info.addTo(this.map);
        // Add layer control div
        //this.layerControl.addTo(this.map)
        // add legend div
        this.legend.addTo(this.map)

        geolayers.forEach(layer => this.add_geolayer(layer))
    }

    this.add_geolayer = (geolayer) => {
        let layer = new GeoLayer(geolayer.name, geolayer.url)

        // set the property containing the information to choose the color
        // could be the color itself
        layer.color_property_name = get(geolayer, "color_property_name", "surface")

        // set an eventlistner to load only visible data if we don't load
        // everything upfront (which is better)
        layer.load_full_data = get(geolayer, "load_full_data", false)

        // displayer the layer immediatly after data loading or wait the user
        // to make it visible
        layer.display = get(geolayer, "display", false)

        // center the map on this layer
        // todo : check that there is only one layer with this activated
        layer.fit_map = get(geolayer, "fit_map", false)

        // Change layer style to use one specific for project emprise
        if (get(geolayer, "use_emprise_style", false))
            layer.style = emprise_style

        // set the correct panes according to required level
        // level can be set from 0 to 9
        // 9 is on top, 0 is the most lowest
        let pane = `level_${get(geolayer, "level", "5")}`
        if (this.panes.includes(pane))  // check the layer is known
            layer.pane = pane

        // set the url to retrieve the scale
        layer.scale_url = get(geolayer, "gradient_url", undefined)

        // if switch is OCSGE, replace building form function
        is_ocsge_switch = get(geolayer, "switch", undefined)
        if (is_ocsge_switch == "ocsge")
            layer.create_switch = layer.create_switch_for_ocsge

        layer.add_to_map(this)
    }

    this.info.onAdd = (map) => {
        // create a div with a class "info"
        this._info_div = L.DomUtil.create('div', 'info');
        return this._info_div;
    }

    // method that we will use to update the control
    this.info.update = (html_content) => {
        this._info_div.innerHTML = html_content
    }

    this.legend.onAdd = (map) => {
        // create a div with a class "legend"
        this._info_legend = L.DomUtil.create('div', 'info legend');
        return this._info_legend;
    }

    this.legend.update = (html_content) => {
        this._info_legend.innerHTML = html_content
    }
}


/////////////////////////////////
//  Add layer
/////////////////////////////////

function GeoLayer (name, url) {
    // name of the layer, to be displayed in layercontrol div
    this.name = name
    // url where to fetch GeoJson data
    this.url = url
    // will contain the built GeoJsonLayer
    this.geojsonlayer = null
    // will contain fetched data
    this.data = null

    this.info_txt = null

    // define if the layer is to be displayed as soon data are retrieved
    this.display = true

    // reférence à l'objet carto qui contient map
    this.carto = null

    // indicates if all the data have to be loaded at once or if we reload data on each user map movement
    // when loading the data we will use bbox information to get data only on visible part of the map
    this.load_full_data = true

    // contains the name of the pane in which add this layer
    // by default, we add the layer in pane level_5
    this.pane = 'level_5'

    // Initialiser avec un objet permettant une colorisation personnalisée
    // this.scale = [
    //     {value: 100, color: '#ff0000'},  //   0 -> 100
    //     {value: 150, color: '#ff3300'},  // 101 -> 150
    //     {value: 230, color: '#ff6600'},  // 151 -> 230
    // ]
    this.scale = null
    // Define the url to get data for initialise the scale
    this.scale_url = undefined

    // Set to true to center the map on layer after data has been loaded
    this.fit_map = false

    // Define which property to use to set color of a feature
    this.color_property_name = "surface"

    // DOM element containing the loading image for the filter widget
    this.loading_img = undefined

    // a surcharger pour changer la façon dont la couleur est choisie
    // if this.scale is defined, it will use a property value (like surface) to
    // match against a scale to find the value
    // il no scale are defined, it will look in a property to find a color
    this.get_color = (feature) => {
        // get the property that will decide the color
        property_value = this.get_color_property_value(feature)

        // default color if scale is not set
        if (this.scale == null){
            return property_value
        }
        else
        {
            // use provided scale and color
            // return gray in case of unset
            let item = this.scale.find((item) => property_value < item.value)
            // si on a pas trouvé, on doit être sur la dernière valeur de scale
            // donc le find n'est jamais vrai, on va donc récupérer la dernière
            // valeur pour initialiser item
            item = item ? item : this.scale[this.scale.length - 1]
            // finalement, on renvoit la couleur
            return item.color
        }
    }

    // set which property must be used to set the color
    this.get_color_property_name = (feature) => {
        return this.color_property_name
    }

    // return the value of the feature's property defined in function
    // this.get_color_property_name
    // this could return any value to use with a scale
    // or directly a color like #ff0055
    this.get_color_property_value = (feature) => {
        property_name = this.get_color_property_name(feature)
        if (property_name == null)
        {
            return '#FFEDA0'
        }
        else
        {
            return feature.properties[property_name]
        }
    }

    // A surcharger pour changer le styling par défault d'une feature
    this.style = (feature) => {
        return {
            fillColor: this.get_color(feature),
            fillOpacity: 0.7,
            weight: 1,
            opacity: 0.1,
            color: 'white',
        }
    }

    // A surcharger pour changer le style de mise en avant
    this.highlight_style = {
        weight: 3,
        color: '#777',
        dashArray: '',
        fillOpacity: 0.7
    }

    // surcharge to update content of info div (return empty string to not show info)
    this.info_txt = (properties) => {
        let info = '<h4>' + this.name + '</h4>'
        let properties_names = Object.getOwnPropertyNames(properties)
        for (i=0; i<properties_names.length; i++)
        {
            let property_name = properties_names[i]
            let property_value = properties[property_name]
            info = info + `<b>${property_name}</b>: ${property_value}<br/>`
        }
        return info
    }

    // surcharge to update content of legend div (return empty string to not show info)
    this.legend_txt = (feature) => {
        if (this.scale == null)
            return null
        let property = this.get_color_property_name(feature)
        let property_value = this.get_color_property_value(feature)
        let legend = '<h4>' + this.name + '</h4>'
        let bold = false
        legend = legend + `Property used: ${property} (${property_value})<br\>`

        for (i=0; i<this.scale.length; i++)
        {
            let color = this.scale[i].color
            let value = this.scale[i].value
            let next_value = i+1 < this.scale.length ? this.scale[i+1].value : '+'
            if ((bold == false) && (i+1 == this.scale.length || property_value < next_value)){
                legend = legend + `<i style="background:${color}"></i> <b>${value} &ndash; ${next_value}</b></br>`
                bold = true
            }else{
                legend = legend + `<i style="background:${color}"></i> ${value} &ndash; ${next_value}</br>`
            }
        }
        return legend
    }

    // set the layer appearance, fetch the data and display it on the map
    this.add_to_map = (carto) => {

        this.carto = carto
        this.create_switch()

        // define appearance
        this.geojsonlayer = L.geoJson(
            null,
            {
                style: this.style,
                onEachFeature: (feature, layer) => {
                    layer.on({
                        // Highlight on mouse hover
                        mouseover: (e) => {
                            e.target.setStyle(this.highlight_style)

                            if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
                                layer.bringToFront();
                            }

                            // mets à jour le div d'information
                            carto.info.update(this.info_txt(feature.properties))
                            carto.legend.update(this.legend_txt(feature))
                        },
                        // on mousse out
                        mouseout: (e) => {
                            e.target.setStyle(this.style(feature))
                            carto.info.update('')
                        }

                    })
                },
                pane: this.pane,
            }
        )

        this.geojsonlayer.addTo(carto.map)

        // if a scale_url is defined, we retrieve the scale data before
        // retrieving the layer data
        if (this.scale_url != undefined)
            $.getJSON(this.scale_url, (data) => {
                this.scale = data
                this._add_to_map_step_2()
            })  // TODO faire un point d'arrêt pour récupérer les données
        else
            this._add_to_map_step_2()
    }

    this._add_to_map_step_2 = () => {
        this.refresh_data()

        // Add this layer into the layercontrol div (checkbox to display it)
        // carto.layerControl.addOverlay(this.geojsonlayer, this.name)

        if (this.load_full_data == false)
            // add an eventlistner on user moving the map
            carto.map.on('moveend', this.refresh_data)
    }

    this.get_url = () => {
        return this.url
    }

    this.refresh_data = () => {

        // if the layer is not displayed, we do not refresh it
        if (this.display == false)
            return

        //display loading image
        this.loading_img.setAttribute("style", "display: inline;")

        // full: indicate if we have to load everything (true) or if we have to get only data visible on the map (false)

        let url = this.get_url()
        if (this.load_full_data == false)
        {
            if (url.includes("?"))
                url = url + '&'
            else
                url = url + '?'
            url = url + `in_bbox=${this.carto.map.getBounds().toBBoxString()}`
        }

        // get the data and display the layer
        $.getJSON(url, (data) => {
            /* best solution to add new data to a geojson layer would be to filter new data to remove data already
            loaded before (those in this.data). I choose to clear completly the data to avoid getting caught on
            difficult js stuff but this is definitely need to be improved. Current tactic create a flicker UI very
            displeasant. */
            this.data = data
            this.geojsonlayer.clearLayers()
            this.geojsonlayer.addData(data)

            if (this.fit_map){
                // TODO : move this in carto object
                // center the layer on the center of the map
                this.fit_map = false  // do not recenter after first loading
                bounds = this.geojsonlayer.getBounds()
                console.log(bounds)
                carto.map.fitBounds(bounds);
            }

            // hide loading image
            this.loading_img.setAttribute("style", "display: none;")
        })
    }

    this.create_switch = () => {
        // create wrapper div
        let outer_div = document.createElement("div")
        outer_div.setAttribute("class", "form-check form-switch")
        document.getElementById("layer_list").appendChild(outer_div)
        // add switch
        let input = document.createElement("input")
        input.setAttribute("class", "form-check-input")
        input.setAttribute("type", "checkbox")
        // input.setAttribute("index", index)
        input.checked = this.display // == "True" ? true : false
        let id = `${this.name}_switch`
        input.setAttribute("id", id)
        outer_div.appendChild(input);
        // add label
        let label = document.createElement("label")
        label.setAttribute("class", "form-check-label")
        label.setAttribute("for", id)
        label.innerHTML = this.name
        outer_div.appendChild(label)

        this.create_loading_image(label)

        input.addEventListener('click', (event, state) => {
            let checked = event.target.checked
            if (checked){
                this.activate_layer()
            }else{
                this.deactivate_layer()
            }
        })
    }

    this.create_loading_image = (container) => {
        let img = document.createElement("img")
        img.setAttribute("src", "/static/carto/img/loading-buffering.gif")
        img.setAttribute("class", "ms-1")
        img.setAttribute("style", "display: none;")
        img.setAttribute("width", "12")
        img.setAttribute("height", "12")
        this.loading_img = img
        container.appendChild(this.loading_img)
    }

    this.activate_layer = () => {
        this.display = true
        this.refresh_data()
    }

    this.deactivate_layer = () => {
        this.display = false
        this.geojsonlayer.clearLayers()
    }

    this.create_switch_for_ocsge = () => {
        // create wrapper div
        let outer_div = document.createElement("div")
        outer_div.setAttribute("class", "form-check form-switch")
        document.getElementById("layer_list").appendChild(outer_div)
        //document.getElementById("layer_ocsge").appendChild(outer_div)
        // add input button
        let input = document.createElement("input")
        input.setAttribute("class", "form-check-input")
        input.setAttribute("type", "checkbox")
        // input.setAttribute("index", index)
        input.checked = this.display // == "True" ? true : false
        let id = `${this.name}_switch`
        input.setAttribute("id", id)
        outer_div.appendChild(input);
        // add label
        let label = document.createElement("label")
        label.setAttribute("class", "form-check-label")
        label.setAttribute("for", id)
        //label.innerHTML = this.name
        outer_div.appendChild(label)

        // <div class="input-group">
        let input_div = document.createElement("div")
        input_div.setAttribute("class", "input-group")
        label.appendChild(input_div)

        // <div class="input-group-text">@</div>
        let text_div = document.createElement("div")
        text_div.setAttribute("class", "input-group-text")
        text_div.innerHTML = "OCSGE : "
        input_div.appendChild(text_div)

        let select_year = get_select("ocsge_years", {"2015": "2015", "2018": "2018"})
        select_year.addEventListener('click', (e, s) => this.click(input))
        input_div.appendChild(select_year)

        let select_sol = get_select("ocsge_sol", {
            "usage": "Usage du sol",
            "couverture": "Couverture du sol"
        })
        select_sol.addEventListener('click', (e, s) => this.click(input))
        input_div.appendChild(select_sol)

        this.create_loading_image(label)

        this.get_url = () => {
            let url = this.url
            if (url.includes("?"))
                url = url + '&'
            else
                url = url + '?'
            //?year=2015&color=couverture
            url = url + `year=${document.getElementById("ocsge_years").value}`
            url = url + `&color=${document.getElementById("ocsge_sol").value}`
            return url
        }

        input.addEventListener('click', (e, s) => this.click(e.target))
    }

    this.click = (target) => {
        if (target.checked){
            this.activate_layer()
        }else{
            this.deactivate_layer()
        }
    }

}

function get_select(id, options){
    let select = document.createElement("select")
    select.setAttribute("class", "form-select form-select-sm")
    select.setAttribute("aria-label", "form-select")
    select.setAttribute("id", id)
    for (const [key, value] of Object.entries(options)) {
        let option = document.createElement("option")
        option.setAttribute("value", key)
        option.innerHTML = value
        select.appendChild(option)
    }
    return select
}

function get_loading_gif(id){
    let img = document.createElement("img")
    img.setAttribute("src", "/static/carto/img/loading-buffering.gif")
    img.setAttribute("id", id)
    img.setAttribute("width", "12")
    img.setAttribute("height", "12")
}
