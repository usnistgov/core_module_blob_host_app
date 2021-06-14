/** Blob Host module script */
let saveBlobHostData = function() {
    return new FormData(
        $($("#modal-" + moduleElement[0].id)[0]).find(".blob-host-form")[0]
    );
};

let blobHostPopupOptions = {
    title: "Upload File",
    getData: saveBlobHostData
}

// FIXME: update url?
configurePopUp('module-blob-host', blobHostPopupOptions);
