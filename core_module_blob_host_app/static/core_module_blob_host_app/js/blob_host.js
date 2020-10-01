/** Blob Host module script */
let saveBlobHostData = function() {
    return new FormData($($("#modal-" + moduleElement[0].id)[0]).find(".blob-host-form")[0]);
};

let blobHostPopupOptions = {
    title: "Upload File",
    getData: saveBlobHostData
}

// FIXME: update url?
configurePopUp('module-blob-host', blobHostPopupOptions);
$(".custom-file span input[type=file]").on('change',function(event){
    //get the file name
    let filePath = $(this).val();
    // get the file name from the path
    let fileName = filePath.split('\\');
    // some browser use the path substitution to hide the true file path
    if(fileName.length > 0) {
        fileName = fileName.splice(-1).pop();
    } else {
        fileName = filePath;
    }

    //replace the "Choose a file" label
    $(this).parent().next('.custom-file-label').html(fileName);
});
