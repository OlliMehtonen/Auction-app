
"use strict"

let currencyTable = {}

//Initialize page
window.addEventListener("load", async () => {

        initCurrencies()

        let form = document.getElementById('biddingform')
        let bidButton = document.getElementById('bidbutton')
        let topBid = parseFloat(document.getElementById('hideTopBid').textContent)
        let itemId = document.getElementById('hiddenid').textContent.trim()
        let minimumPrice = parseInt(document.getElementById("hidePrice").textContent)
        let deleteButton = document.getElementById('delete')
        console.log("bb", bidButton)
        console.log("db", deleteButton)
        
        //Handle button click and bid adding

        if (bidButton !== null ){

                bidButton.addEventListener('click', async (e) =>{
                        e.preventDefault()
                        let newBidCur = parseFloat(document.getElementById('newbid').value)
                        let newBidEur = newBidCur / currencyTable[localStorage.getItem('currencyChosen')]['rate']

                        if ( newBidEur > topBid && newBidEur >=minimumPrice){ 
                                let bidData = {
                                        item_id: itemId.trim(),
                                        bid_price: newBidEur
                                }
                                let newBidReq = {
                                        method: 'POST',
                                        headers: {
                                                'Content-Type': 'application/json',
                                                "Authorization": `Bearer ${localStorage.getItem('13jwtstore')}`
                                        },
                                        body: JSON.stringify(bidData)
                                }
                                let url = "/bid"
                                let response = await fetch(url, newBidReq)
                                location.reload()


                        } else {
                                console.log("BID HIGHER!")
                        }


                })
        }

        if (deleteButton !== null) {

                deleteButton.addEventListener('click', async (e) =>{
                        e.preventDefault()
                                let newDelReq = {
                                        method: 'DELETE',
                                        headers: {
                                                'Content-Type': 'application/json',
                                                "Authorization": `Bearer ${localStorage.getItem('13jwtstore')}`
                                        }
                        }
                        let url = "/auction_item/".concat(itemId)
                        let response = await fetch(url, newDelReq)
                        console.log(response)
                        window.location = '/'




                })
        }



        
})



//Currency related functions
//

const initCurrencies = async  () => {
        currencyTable = await getExchangeRates() 

        //Add currency options
        //First nonseelctable option


        let op =document.createElement('option')
        op.setAttribute('value', '')
        op.textContent = "Choose currency"
        op.setAttribute('disabled', "")
        op.setAttribute('hidden', "")
        
        //get parent tag
        let currSel = document.getElementById("aafCurr")
        console.log(currSel)
        addOptions(currSel, Object.values(currencyTable), 'cur', 'code', op, localStorage.getItem('currencyChosen') )

        console.log(currSel)
        
        //Update currency texts
        onCurrencyUpdate(localStorage.getItem('currencyChosen'))

        //Event listener for change of currency 
        currSel.addEventListener('change', ()=>{
                let val = currSel.value
                localStorage.setItem('currencyChosen', val)
                onCurrencyUpdate(val)






        })
        



}

const onCurrencyUpdate = (val) =>{

                updateCurrencyText(val)
                updateCurrencyValues(val, 'hidePrice' , 'startingprice')
                updateCurrencyValues(val, 'hideTopBid' , 'topbid')
}

const updateCurrencyText = (cur) =>{
        let tagList = document.getElementsByClassName('curtag')

        for ( let t of tagList){
                t.textContent = cur
        }

}


const updateCurrencyValues = (val, from, to) => {
        let price = parseFloat(document.getElementById(from).textContent)
        console.log(price)

        console.log(document.getElementById(from))
        console.log("now")
        console.log(typeof price, typeof currencyTable[val]['rate'])
        console.log(price)
        console.log(currencyTable[val]['rate'])
        console.log(` ${price*currencyTable[val]['rate']}`)
        document.getElementById(to).textContent = ` ${price*currencyTable[val]['rate']} ` 



        
}


const getExchangeRates = async () => {
        
        //Check if rates are saved in local storage
        let curObj = localStorage.getItem('currencies')
        if (curObj === null){
                
                let rateReq = await fetch("https://sdw-wsrest.ecb.europa.eu/service/data/EXR/D..EUR.SP00.A?startPeriod=2023-01-01&lastNObservations=1&format=jsondata")
                console.log("rates")
                let data = await rateReq.json()
                console.log(data)
                let rates = Object.values(data.dataSets[0].series)
                let currencyNames = data.structure.dimensions.series[1].values
                curObj = {'EUR': {'cur': 'European Euro', 'code': 'EUR',  'rate':1}}
                for (let i in rates){
                        curObj[currencyNames[i]['id']] = {'code':currencyNames[i]['id'], 'cur': currencyNames[i]['name'], 'rate':rates[i]['observations'][0][0]}
                }
                //Put currencies to localStorage to use them on item page too
                localStorage.setItem('currencies', JSON.stringify(curObj))
                console.log(curObj)
                console.log("dollari", curObj)
        } else {
                console.log("PARSING")
                curObj = JSON.parse(curObj)
                console.log(curObj)
        }
        return curObj 
}



//Reusable function to add options to select fields
//parent = parent node
//list = list of objects that are made to options
//textTag :string = object key for option field textContent
//valueTag :string = object key for option field value field
//headerOption :option tag = option tag used as first option for giving input which is not automatically generated 
const addOptions = (parent, list, textTag, valueTag, headerOption = null, defaultValue = null  ) => {
        if (Array.isArray(headerOption)  ){
                parent.append(...headerOption)


        } else if (headerOption !== null){
                parent.appendChild(headerOption)

        }
        for (let ob of list){
                let op = document.createElement("option")
                op.setAttribute('value', ob[valueTag])
                //if (ob[valueTag] === defaultValue ){
                        //op.setAttribute('selected', 'selected')
                //}
                op.textContent=ob[textTag]
                parent.appendChild(op)
        }
        parent.value = defaultValue

}

