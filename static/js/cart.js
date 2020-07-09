var updateBtns = document.getElementsByClassName('update-cart')
var updateOrder = document.getElementsByClassName('update-order')

for (i=0;i< updateOrder.length;i++) {
    updateOrder[i].addEventListener('click',function () {

        print("user is logged,getting data")

    })}
for (i=0;i< updateBtns.length;i++) {
    updateBtns[i].addEventListener('click',function () {
        var product =this.dataset.product
        var action=this.dataset.action
        console.log('USer is :',user)
        if(user=='AnonymousUser'){
            console.log("user not login")
        }else{
            updateUserOrder(product,action)
               console.log("user is logged,getting data")
        }

    })}

function updateUserOrder(product,action) {
    console.log('logged in')
    var url='/updated_item/'
    fetch(url,{
        method:'POST',
        headers:{
            'content-type':'application/json',
            'X-CSRFToken':csrftoken
        },
        body:JSON.stringify({
            'product':product,'action':action
        })

    }).then((response)=>{
        return response.json()
    }).then((data)=>{
        console.log('data',data)
        location.reload()
    })
}
function updateAdminOrder(complete,status) {
    console.log('logged in')

}

