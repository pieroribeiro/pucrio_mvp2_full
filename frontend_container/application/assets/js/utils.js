function showAlert(message, type) {
    if (! $("#alert").length) {
        $('#alertContainer').prepend(`<div id="alert" class="alert alert-${type} fade show" role="alert"><strong>Atenção!</strong> <span class="message">${message}</span></div>`)

        setTimeout(() => {
            $('#alertContainer').empty()
        }, 5000)
    }
}

const formatCurrency = (lang = 'pt-BR', coin= 'BRL', value = 0) => {
    return new Intl.NumberFormat(lang, { style: "currency", currency: coin, minimumFractionDigits: 2, maximumFractionDigits: 2}).format(value)
}

const formatPercent = (val) => {
    return new Intl.NumberFormat('pt-BR', { style: "percent", minimumFractionDigits: 2, maximumFractionDigits: 2, signDisplay: "exceptZero" }).format(val)    
}

const formatDatetime = (val) => {
    const d = new Date(val)
    return `${d.getDate()}/${d.getMonth()}/${d.getFullYear()} às ${d.getHours()}:${d.getMinutes()}`
}

const calculateIncrement = (valueBefore, valueAfter) => {
    valueBefore = parseFloat(valueBefore)
    valueAfter = parseFloat(valueAfter)
    return ((valueAfter - valueBefore) / valueBefore)
}

const objectifyForm = (formArray) => {
    var returnArray = {};
    for (var i = 0; i < formArray.length; i++){
        returnArray[formArray[i]['name']] = formArray[i]['value'];
    }
    return returnArray;
}