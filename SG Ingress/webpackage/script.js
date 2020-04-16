$("#rulesForm").submit(function(e) {
    e.preventDefault();

    const object = {
        'CidrIp': $('#CIPname').val(),
        'Description': $('#Dname').val(),
        'FromPort': $('#FPname').val(),
        'GroupName': $('#Gname').val(),
        'IpProtocol': $('#IPname').val(),
        'ToPort': $('#TPname').val()
    };

    $.ajax({
        method: "POST",
        contentType: 'application/json',
        url: "/save",
        data: JSON.stringify(object),
        success: function (data) {
            console.log('Data', data);
            if (data && data.status === "ok") {
                alert('finished python script');
            }
            else {
                alert('Python script failed');
            }
        },
        error: function (request, status, error) {
            console.log(request);
            console.log(status);
            console.log(error);

            serviceError();
        }
    });
});
