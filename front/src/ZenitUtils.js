import _ from 'lodash'
import persianDate from "persian-jdate"

import { dom, Notify, debounce } from 'quasar'
const { ready } = dom

// Execute a Function when DOM is ready:
ready(function () {
    document.getElementById('loader').remove()
})

const limitInput_en_message = debounce(function() {
    Notify.create({
        type: 'info' , message: 'لطفا صفحه کلید خود را انگلیسی کنید' 
    })
}, 10*1000, true)

const limitInput_int_message = debounce(function() {
    Notify.create({
        type: 'info' , message: 'لطفا فقط عدد وارد کنید' 
    })
}, 10*1000, true)

export default {
    parseIntNum: (v) => parseInt(v.toString().replaceAll(',', '')),

    limitInput_en: (e) => {
        if (/^\W$/.test(e.key)) {
            e.preventDefault();
            limitInput_en_message()
        }
    },

    limitInput_int: (e) => {
        if (/^\D$/.test(e.key)) {
            e.preventDefault();
            limitInput_int_message()
        }
    },

    boolFormat: (v) => v ? 'بله': 'خیر',

    nano: (template, data) => {
        return template.replace(/\{([\w\.]*)\}/g, function(str, key) {
            if(typeof(data) === "undefined" || data == null )
                return ''; 
            var keys = key.split("."), v = data[keys.shift()];
            for (var i = 0, l = keys.length; i < l; i++) {
            if(typeof(v) === "undefined" || v == null )
                break; 
            v = v[keys[i]];
            }
            return (typeof v !== "undefined" && v !== null) ? v : "";
        });
        },
    
    date2sh: (v)=>{
        if(!v) return ""

        var d = new persianDate(new Date(v))
        d.toCalendar('persian')
        d.toLocale('en')
        return d.format('YYYY/MM/DD')
    },

    datetime2sh: (v) => {
        if(!v) return ""

        var d = new persianDate(new Date(v))
        d.toCalendar('persian')
        d.toLocale('en')
        return d.format('YYYY/MM/DD HH:mm')
    },

    dateFormat: (v)=>{
        var d = (new persianDate(v))
        d.toCalendar('gregorian')
        d.toLocale('en')
        return d.format('YYYY-MM-DD')
    },

    sh2date: (v)=>{
        var v = v.split('/')
        for(var i=0; i<v.length; i++){
          v[i] = parseInt(v[i])
        }
        var d = (new persianDate(v))
        d.toCalendar('gregorian')
        d.toLocale('en')
        return d.format('YYYY-MM-DD')
    },
}