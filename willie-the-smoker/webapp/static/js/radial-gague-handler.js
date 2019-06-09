class TemperatureGauge {

/* public: */
    constructor({destCanvasId, fahrenheit=true, title=""}={}) {
        this.fahrenheit = fahrenheit;
        this.gauge = new RadialGauge({
        renderTo: destCanvasId,
        width: 300,
        height: 300,
        units: this.units(fahrenheit),
        minValue: this.minValue(fahrenheit),
        maxValue: this.maxValue(fahrenheit),
        majorTicks: this.majorTicks(fahrenheit),
        minorTicks: 2,
        strokeTicks: true,
        title:title,
        highlights: this.highlights(fahrenheit),
        colorPlate: "#fff",
        borderShadowWidth: 0,
        borders: false,
        needleType: "arrow",
        needleWidth: 2,
        needleCircleSize: 7,
        needleCircleOuter: true,
        needleCircleInner: false,
        animationDuration: 1500,
        animationRule: "linear"
        });

        TemperatureGauge.activeGauges.push(this);
    }

    draw(destId) {
        this.gauge.draw();
    }

    static unitsChanged(fahrenheit) {
        TemperatureGauge.activeGauges.forEach(function(e) {
            e.changeUnits(fahrenheit);
            e.majorTicks(fahrenheit);
        });
    }

    static updateTemp(id, temp) {
        TemperatureGauge.activeGauges.forEach(function(gauge) {
            if (gauge.gauge.options.renderTo == id) {
                gauge.gauge.value = temp;
                console.log("Updating temp");
                return;
            }
        })
    }

/* private: */
    changeUnits(fahrenheit) {
        this.gauge["options"]["highlights"] = this.highlights(fahrenheit);
        this.gauge["options"]["majorTicks"] = this.majorTicks(fahrenheit);
        this.gauge["options"]["minValue"] = this.minValue(fahrenheit);
        this.gauge["options"]["maxValue"] = this.maxValue(fahrenheit);
        this.gauge["options"]["units"] = this.units(fahrenheit);
        this.gauge.update();
    }

    // Properties
    highlights(fahrenheit) /* const */ {
        var idealTemp = fahrenheit ? TemperatureGauge.IDEAL_TEMP_F :
                                     TemperatureGauge.toC(
                                         TemperatureGauge.IDEAL_TEMP_F);

        var goodDelta = 0;
        if (fahrenheit) {
            goodDelta = TemperatureGauge.IDEAL_TEMP_F_HIGHLIGHT_DELTA;
        } else {
            var end = TemperatureGauge.toC(
                TemperatureGauge.IDEAL_TEMP_F + TemperatureGauge.IDEAL_TEMP_F_HIGHLIGHT_DELTA)
            var start = TemperatureGauge.toC(
                TemperatureGauge.IDEAL_TEMP_F - TemperatureGauge.IDEAL_TEMP_F_HIGHLIGHT_DELTA)
            goodDelta = Math.round((end - start) / 2);
        }

        return [
            {
            "from": (idealTemp - goodDelta),
            "to": (idealTemp + goodDelta),
            "color": "rgb(0, 204, 64, .75)"
            },
            {
            "from": (idealTemp + goodDelta),
            "to": this.maxValue(fahrenheit),
            "color": "rgb(255, 0, 0, .75)"
            },
        ]
    }

    majorTicks(fahrenheit) /* const */ {
        var range = this.maxValue(fahrenheit) - this.minValue(fahrenheit);
        var inc = Math.floor(range / TemperatureGauge.NUM_TICKS);
        var cur = this.minValue(fahrenheit);
        var res = [];
        for (var i = 0; i < TemperatureGauge.NUM_TICKS; i++) {
            res.push(String(cur));
            cur += inc;
        }

        // Make sure to get the last bit or it won't go that high
        res.push(this.maxValue(fahrenheit));
        return res;
    }

    maxValue(fahrenheit) /* const */ {
        return fahrenheit ? TemperatureGauge.MAX_TEMP_F :
                            TemperatureGauge.toC(TemperatureGauge.MAX_TEMP_F);
    }

    minValue(fahrenheit) /* const */ {
        return fahrenheit ? TemperatureGauge.MIN_TEMP_F :
                            TemperatureGauge.toC(TemperatureGauge.MIN_TEMP_F);
    }

    static toC(deg_f) {
        return Math.round(((deg_f - 32 ) * 5) / 9);
    }

    units(fahrenheit) /* const */ {
        return fahrenheit ? "°F" : "°C";
    }
}

// The C++ guy in me needs this shit to stay sane
// private:
    /* static */ TemperatureGauge.activeGauges = [];
    /* const static */ TemperatureGauge.IDEAL_TEMP_F = 225;
    /* const static */ TemperatureGauge.IDEAL_TEMP_F_HIGHLIGHT_DELTA = 10;
    /* const static */ TemperatureGauge.MAX_TEMP_F = 300;
    /* const static */ TemperatureGauge.MIN_TEMP_F = 70;
    /* const static */ TemperatureGauge.NUM_TICKS = 12;
