"""Special service request data."""

class SsrData(object):

    rqst_sequence_no = None
    indicator = None
    rqst_code = None
    action_code = None
    actn_number = None
    request_text = None
    all_itinerary_flag = None
    all_pax_flag = None

    def __init__(self, rqst_sequence_no,
                 indicator, rqst_code,
                 action_code, actn_number,
                 request_text, all_itinerary_flag,
                 all_pax_flag):
        """Initialize special service request data."""
        self.rqst_sequence_no = rqst_sequence_no
        self.indicator = indicator
        self.rqst_code = rqst_code
        self.action_code = action_code
        self.actn_number = int(actn_number)
        self.request_text = request_text
        self.all_itinerary_flag = all_itinerary_flag
        self.all_pax_flag = all_pax_flag

    def display(self):
        """Display special service request data."""
        print("No %2d indicator %s request %s action %s%s itinerary %s pax %s : %s"
              % (self.rqst_sequence_no,
                 self.indicator, self.rqst_code,
                 self.action_code, self.actn_number, self.all_itinerary_flag,
                 self.all_pax_flag,
                 self.request_text))
