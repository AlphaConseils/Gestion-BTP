/** @odoo-module **/

import { registry } from "@web/core/registry";
import { usePopover } from "@web/core/popover/popover_hook";
import { useService } from "@web/core/utils/hooks";
import { localization } from "@web/core/l10n/localization";
import { parseDate, formatDate } from "@web/core/l10n/dates";

import { formatMonetary } from "@web/views/fields/formatters";

const { Component, onWillUpdateProps } = owl;

export class SaleAttachment extends Component {
    setup() {
        this.orm = useService("orm");
        this.action = useService("action");
        this.formatData(this.props);
        onWillUpdateProps((nextProps) => this.formatData(nextProps));

    }

    formatData(props) {
        const info = props.value || {
            content: [],
            title: "",
            date_ref: 'sale_attachment_date',
            sale_id: this.props.record.data.id,
        };
//        for (let [key, value] of Object.entries(info.content)) {
//            value.price_subtotal_formatted = formatMonetary(value.price_subtotal, { currencyId: value.currency_id });
//            value.price_anterior_formatted = formatMonetary(value.price_anterior, { currencyId: value.currency_id });
//            value.price_current_formatted = formatMonetary(value.price_current, { currencyId: value.currency_id });
//
//        }

        this.lines = info.content;
        this.title = info.title;
        this.date_ref = info.date_ref;
        this.sale_id = info.sale_id;
    }
    async onValidatePercent(event) {
        if (event.key !== 'Enter') {
            return;
        }
        var $target = $(event.target);
        var line_id = $target.attr('line_id');
        var date_object = this.props.record.data[this.date_ref].c;
        if(!date_object){
            return ;
        }
        var value = parseFloat($target.val());
        await this.orm.call(this.props.record.resModel, 'update_sale_attachment', [this.sale_id, line_id, date_object,value ], {});
        await this.props.record.model.root.load();
        this.props.record.model.notify();

    }
    getTotalCumuls(){
        var total_cumuls = 0;
        for(var i=0; i<this.lines.length;i++){
            total_cumuls += this.lines[i].price_anterior + this.lines[i].price_current
        }
        return total_cumuls
    }
    getTotalAnterior(){
        var total_anterior = 0;
        for(var i=0; i<this.lines.length;i++){
            total_anterior += this.lines[i].price_anterior
        }
        return total_anterior

    }
    getTotalCurrent(){
        var total_current = 0;
        for(var i=0; i<this.lines.length;i++){
            total_current += this.lines[i].price_current
        }
        return total_current
    }
    _formatMonetary(amount){
        return formatMonetary(amount, { currencyId: this.lines[0].currency_id });
    }
}
SaleAttachment.template = "oti_sale.SaleAttachment";
SaleAttachment.supportedTypes = ["char"];


registry.category("fields").add("sale_attachment", SaleAttachment);
