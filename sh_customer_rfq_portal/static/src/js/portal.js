$(document).ready(function (e) {
    var rowIdx = 0;

    $("#addBtn").on("click", function () {
        var rowCount = $(document).find("#tbody tr").length + 1;
        var rowIdx = rowIdx + 1;
        var productSelectName = "product_id_" + String(rowCount);
        var productqty = "pack_qty_" + String(rowCount);
        var totalqty = "total_qty_" + String(rowCount);
        var productOptioons = '<option value="">Select Product</option>';
        var productOptioons = $(document).find("#js_id_product_list").html();
        var text =
            '<tr id="R' +
            String(rowIdx) +
            '">' +
            '<td class="text-center"><img class="img img-fluid js_product_img" src="/web/static/src/img/placeholder.png" alt="Product" style="width:100px;height:100px;"></img></td>' +
            '<td class="row-index text-center">' +
            '<div t-attf-class="form-group #{error and "product_id" in error and "has-error" or ""}>' +
            '<select class="form-control form-field o_website_form_required_custom js_product_id" name="' +
            productSelectName +
            '"' +
            ' required="True">' +
            productOptioons +
            "</select></div></td>" +
            '<td class="text-center"><input class="form-control js_total_pack_qty" type="number" value="1" name="' +
            totalqty +
            '"' +
            "></td>" +
            '<td class="text-center"><button class="btn btn-danger remove" type="button"><i class="fa fa-trash"/></button></td></tr>';
        $("#tbody").append(text);
    });
    $("#tbody").on("click", ".remove", function () {
        var child = $(this).closest("tr").nextAll();
        child.each(function () {
            var id = $(this).attr("id");
            var idx = $(this).children(".row-index").children("p");
            var dig = parseInt(id.substring(1));
            idx.html(`Row ${dig - 1}`);
            $(this).attr("id", `R${dig - 1}`);
        });
        $(this).closest("tr").remove();
        rowIdx--;
    });
    $("#tbody").on("change", ".js_product_id", function (ev) {
        var $product = $(ev.currentTarget);
        var product_id = $product.find("option:selected").val();
        var $productImg = $product.closest("tr").find(".js_product_img");
        $productImg.attr("src", '/web/static/src/img/placeholder.png');
        $.ajax({
            url: "/pack-qty-data",
            data: { product_id: product_id },
            type: "post",
            cache: false,
            success: function (result) {
                var datas = JSON.parse(result);
                $productImg.attr("src", datas.image);
            },
        });
    });
});
