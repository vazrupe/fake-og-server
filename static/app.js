$(document).ready(function(){
    var urlTester = new RegExp("^http(s|)://.+$");

    var sourceInput = $('#source_url');
    var targetInput = $('#target_url');

    var fakeResult = $('#fake_url');

    var goToAnchor = $('#go_to_url');

    var changeUrls = function(_) {
        var sourceUrl = sourceInput.val().toLowerCase();
        var targetUrl = targetInput.val().toLowerCase();

        var validSourceUrl = urlTester.test(sourceUrl);
        var validTargetUrl = urlTester.test(targetUrl);
        if (validSourceUrl && validTargetUrl) {
            var encodedSourceUrl = window.btoa(sourceUrl);
            var encodedTargetUrl = window.btoa(targetUrl);

            var fakeUrl = location.origin + '/fog/' + encodedSourceUrl + '/' + encodedTargetUrl;

            fakeResult.val(fakeUrl);
            goToAnchor.attr('href', fakeUrl);
            fakeResult.css({"cursor": "pointer"});
            goToAnchor.css({"display": "inline"});
        } else {
            if (!validSourceUrl && !validTargetUrl) {

                fakeResult.attr('placeholder', 'Invalid `Source Url` and `Target Url`');
            } else {
                fakeResult.attr('placeholder', 'Invalid `' + (validSourceUrl?'Target Url':'Source Url') + '`');
            }
            fakeResult.css({"cursor": "not-allowed"});
            goToAnchor.css({"display": "none"});
        }
    };

    fakeResult.click(function() {
        fakeResult.select();
    });

    sourceInput.change(changeUrls);
    targetInput.change(changeUrls);
});