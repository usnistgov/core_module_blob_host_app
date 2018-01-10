var blobHostPopupOptions = {
    title: "Upload File",
}

var saveBlobHostData = function() {
    return new FormData(openPopUp.find('.blob-host-form')[0]);
};

// FIXME: update url?
configurePopUp('module-blob-host', blobHostPopupOptions, saveBlobHostData);
