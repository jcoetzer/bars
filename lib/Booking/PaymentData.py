

class PaymentData(object):

    payment_form = None
    payment_type = None
    payment_amount = None
    payment_date = None
    document_no = None
    payment_mode = None
    pax_name = None
    pax_code = None
    paid_flag = None
    update_time = None

    def __init__(self, payment_form, payment_type,
                 currency_code, payment_amount, payment_date,
                 document_no, payment_mode, pax_name, pax_code,
                 paid_flag, pay_stat_flag,
                 update_time):
        self.payment_form = payment_form
        self.payment_type = payment_type
        self.currency_code = currency_code
        self.payment_amount = payment_amount
        self.payment_date = payment_date
        self.document_no = document_no
        self.payment_mode = payment_mode
        self.pax_name = pax_name
        self.pax_code = pax_code
        self.paid_flag = paid_flag
        self.pay_stat_flag = pay_stat_flag
        self.update_time = update_time

    def display(self):
        print("Payment type %s amount %s%d document %s date %s"
              % (self.payment_type, self.currency_code, self.payment_amount,
                 self.document_no,
                 self.update_time))
