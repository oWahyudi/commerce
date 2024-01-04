
// Shared function for navigating through pages within a Django template form.

//get the current URL without query parameters
var baseUrl=window.location.origin

function GoToPage(routePath,pageNumber) {
    //get the current URL without query parameters
    var newUrl = `${baseUrl}${routePath}?page=${pageNumber}`;
    window.location.href = newUrl;
}

function GoDetailPage(routePath,id) {
    var newUrl = `${baseUrl}/${routePath}/${id}`;
    window.location.href = newUrl
}
