
function foo() {
    var selObj = window.getSelection(); 
    alert(selObj);
    var selRange = selObj.getRangeAt(0);
    // do stuff with the range
}