function deleteCustomer(customerId){
    fetch("/delete-customer", {
        method:'POST',
        body: JSON.stringify({customerId: customerId}),
    }).then((_res) =>{
        window.location.href = "/";
    });
}