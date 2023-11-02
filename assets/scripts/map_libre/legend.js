import { formatData } from './utils.js'

export default class Legend {
    constructor(_options = {}, _source) {
        this.mapLibre = window.mapLibre
        this.map = this.mapLibre.map

        this.title = _options.title
        this.subtitle = _options.subtitle
        this.data = _options.data
        this.formatter = _options.formatter
        this.source = _source

        this.setLegendBox()
    }

    // Setters
    setLegendBox() {
        this.legendBoxNode = document.createElement('div')
        this.legendBoxNode.id = `legend-box-${this.source}`
        this.legendBoxNode.classList.add('legend-box', 'visible')

        this.legendTitleNode = document.createElement('div')
        this.legendTitleNode.classList.add('legend-box__title')
        this.legendTitleNode.innerHTML = `<strong>${this.title}</strong><i class='bi bi-info-circle'></i>`
        this.legendBoxNode.appendChild(this.legendTitleNode)
        
        this.legendSubtitleNode = document.createElement('div')
        this.legendSubtitleNode.classList.add('legend-box__subtitle')
        this.legendSubtitleNode.innerHTML = this.subtitle
        this.legendBoxNode.appendChild(this.legendSubtitleNode)

        this.data.map((_obj, index) => {
            let legendText
            if (this.formatter)
            {
                legendText = index === 0 ? `0 &ndash; ${formatData(this.formatter[0], this.formatter[1], _obj.value)}` : `${formatData(this.formatter[0], this.formatter[1], this.data[index-1].value)} &ndash; ${formatData(this.formatter[0], this.formatter[1], _obj.value)}`
            }
            else
            {
                legendText = index === 0 ? `0 &ndash; ${_obj.value}` : `${this.data[index-1].value} &ndash; ${_obj.value}`
            }
            let legendNode = document.createElement('div')
            legendNode.classList.add('legend-box__legend')
            legendNode.innerHTML = `<svg class="me-2" width="18" height="18" xmlns="http://www.w3.org/2000/svg" version="1.1"><rect x="0" y="0" width="18" height="18" fill="${_obj.color}"/></svg><div>${legendText}</div>`
            this.legendBoxNode.appendChild(legendNode)
        })

        this.mapLibre.infosBoxNode.appendChild(this.legendBoxNode)
    }
}