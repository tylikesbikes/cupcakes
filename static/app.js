$('#new_cupcake_btn').click(addCupcake);

async function addCupcake() {

    let addCupcakeFormData = new FormData();

    addCupcakeFormData.append('flavor', $('#flavor').val());
    addCupcakeFormData.append('size', $('#size').val());
    addCupcakeFormData.append('rating', $('#rating').val());
    addCupcakeFormData.append('image', $('#image').val());
    

    
    await axios.post('/api/cupcakes', data=addCupcakeFormData)
        .then(function (res) {
            let cc = res.data.cupcake
            $('#cupcake_list').append(`<div data-id="{cc.id}" class="cupcake_div grid g-col-4">
            <p>Flavor:  {cc.flavor}</p>
            <p><img src="cc.image" height="200" width="200"></p>
            </div>`);
            
        })
        .catch(function(res) {console.log('fail');console.log(res);})

    
}