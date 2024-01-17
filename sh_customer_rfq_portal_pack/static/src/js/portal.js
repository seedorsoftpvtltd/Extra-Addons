$(document).ready(function (e) {
    $("#addBtn").on("click", function (ev) {
        var rowCount = $(document).find("#tbody tr").length;
        var productqty = "pack_qty_" + String(rowCount);
        $('<td class="text-center"><input class="form-control js_pack_qty" type="number" value="1" name="' + productqty + '"/></td>').insertBefore($("#rfq_table tbody tr:last").find(".js_total_pack_qty").closest("td"));
    });
    $("#tbody").on("change", ".js_pack_qty", function (ev) {
        var $packtQty = $(ev.currentTarget);
        var product_id = $packtQty.closest("tr").find(".js_product_id option:selected").val();
        var $total_qty = $packtQty.closest("tr").find(".js_total_pack_qty");
        $.ajax({
            url: "/pack-qty-data",
            data: { product_id: product_id, packtQty: $packtQty.val() },
            type: "post",
            cache: false,
            success: function (result) {
                var datas = JSON.parse(result);
                $total_qty.val(datas.total_qty);
            },
        });
    });
    $("#tbody").on("change", ".js_product_id", function (ev) {
        var $product = $(ev.currentTarget);
        var product_id = $product.find("option:selected").val();
        var $total_qty = $product.closest("tr").find(".js_total_pack_qty");
        var $packtQty = $product.closest("tr").find(".js_pack_qty");
        $.ajax({
            url: "/pack-qty-data",
            data: { product_id: product_id, packtQty: $packtQty.val() },
            type: "post",
            cache: false,
            success: function (result) {
                var datas = JSON.parse(result);
                $total_qty.val(datas.total_qty);
            },
        });
    });
});
