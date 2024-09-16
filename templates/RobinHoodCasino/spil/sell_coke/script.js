var numberCustomer = 5;
for(let i = 0; i < numberCustomer;i++){
    addCustomer(i);
}

window.addEventListener('keydown', (event) => {
    let seller = document.getElementById("seller");

    // Get the current left and top values as numbers
    let currentX = parseInt(seller.style.left) || 0;
    let currentY = parseInt(seller.style.top) || 0;
    //console.log(currentX,currentY);
    let stepSize = 20;

    if (event.key == 'ArrowLeft'){
        if(isInsideCanvas(currentX-stepSize,currentY))
        seller.style.left = currentX - stepSize + "px";
    }
    else if (event.key == 'ArrowRight'){
        if(isInsideCanvas(currentX+stepSize,currentY))
            seller.style.left = currentX + stepSize + "px";
    }
    else if (event.key == 'ArrowUp'){
        if(isInsideCanvas(currentX,currentY-stepSize))
        seller.style.top = currentY - stepSize + "px";
    }
    else if (event.key == 'ArrowDown'){
        if(isInsideCanvas(currentX,currentY+stepSize))
        seller.style.top = currentY + stepSize + "px";
        } 
    else if (event.key == 's' ){
        if(sell()){
            console.log("Congratz, you have sold coke");
        } else {
            console.log("Too far away from a customer");
        }
    }
});



function isInsideCanvas(x,y){
    let canvas = document.getElementById("canvas");
    let canvasWidth = canvas.offsetWidth;
    let canvasHeight = canvas.offsetHeight;
    let sellerWidth = seller.offsetWidth;
    let sellerHeight = seller.offsetHeight;
    // console.log(sellerWidth,sellerHeight);
    // console.log(canvasWidth,canvasHeight,x,y);
    //right
    if(canvasWidth < x+sellerWidth){
        // console.log("right");
        return false;
    } 
    //left
    if(0 > x){
        // console.log("left");
        return false;
    } 
    //button
    if(canvasHeight < y+sellerHeight){
        // console.log("button");
        return false;
    } 
    //top
    if(0 > y){
        // console.log("top");
        return false;
    } 
    return true;
}

function ranX(){
    let canvasWidth = canvas.offsetWidth;
    return Math.floor(Math.random()*canvasWidth);
}
function ranY(){
    let canvasHeight = canvas.offsetHeight;
   return Math.floor(Math.random()*canvasHeight);
}

function addCustomer(id){
    let randomX = ranX();
    let randomY = ranY();
    if(isInsideCanvas(randomX,randomY)){
        let customer = document.getElementById("customer"+id);
        if(customer === null){
            customer = document.createElement("img");
            customer.src="https://i.pinimg.com/736x/4d/8f/ce/4d8fcea1a8efb1d2389859dbbe3514de.jpg";
            customer.id="customer"+id;
            customer.className="customer";
            customer.style.backgroundColor="green";
            customer.style.top = randomY + "px";
            customer.style.left = randomX + "px";
            let canvasDiv = document.getElementById("canvas");
            canvasDiv.appendChild(customer);
        } else {
            customer.style.top = randomY + "px";
            customer.style.left = randomX + "px";
        }
        isSameLocation(randomX,randomY,id);

    } else {
        addCustomer(id);
    }
    
}

function sell(){
    for(let i = 0; i < numberCustomer; i++){
        let customerID = document.getElementById("customer"+i);
        let customerWidth = customerID.offsetLeft;
        let customerHeight = customerID.offsetTop;
        let sellerWidth = seller.offsetLeft;
        let sellerHeight = seller.offsetTop;
        console.log(sellerWidth,sellerHeight);
        console.log(i, Math.abs(sellerWidth-customerWidth), Math.abs(sellerHeight-customerHeight))
        if(Math.abs(sellerWidth-customerWidth) <= 30 && Math.abs(sellerHeight-customerHeight) <= 30){
            addCustomer(i);
            return true;
        }
    }    
}



function isSameLocation(x,y,id){
    for(let i = 0; i < id; i++){
        let customerID = document.getElementById("customer"+i);
        if(customerID !== null){
            let customerWidth = customerID.offsetLeft;
            let customerHeight = customerID.offsetTop;
            // console.log(i,Math.abs(x-customerWidth),Math.abs(y-customerHeight));
            if(Math.abs(x-customerWidth) <= 100 && Math.abs(y-customerHeight) <= 100){
                let customer = document.getElementById("customer"+id);
                let randomX = ranX();
                let randomY = ranY();
                customer.style.top = randomY + "px";
                customer.style.left = randomX + "px";
                isSameLocation(randomX,randomY,id);
            }
        }         
    }
}