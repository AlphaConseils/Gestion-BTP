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
        console.log(this.props.record);
        this.props.record.model.notify();

    }
    getTotalCumuls(section_index, index){
        var total_cumuls = 0;
        var length = index == false? this.lines.length : index;
        for(var i=section_index; i<=length;i++){
            if(this.lines[i]){
                total_cumuls += this.lines[i].price_anterior + this.lines[i].price_current
            }

        }
        return total_cumuls
    }
    getTotalAnterior(section_index,index){
        var total_anterior = 0;
        var length = index == false? this.lines.length : index;
        for(var i=section_index; i<=length;i++){
            if(this.lines[i]){
                 total_anterior += this.lines[i].price_anterior
            }

        }
        return total_anterior

    }
    getTotalCurrent(section_index,index){
        var total_current = 0;
        var length = index == false? this.lines.length : index;
        for(var i=section_index; i<=length;i++){
            if(this.lines[i]){
                total_current += this.lines[i].price_current
            }

        }
        return total_current
    }
    _formatMonetary(amount){
        return formatMonetary(amount, { currencyId: false });
    }
    _nextLine_type(index){
        return this.lines[index + 1]? this.lines[index + 1].display_type : 'line_section';
    }
}
SaleAttachment.template = "oti_sale.SaleAttachment";
SaleAttachment.supportedTypes = ["char"];


registry.category("fields").add("sale_attachment", SaleAttachment);
