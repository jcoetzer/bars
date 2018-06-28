"""
Special service request data.
"""

class RequestData(object):

    rqst_sequence_no = 0
    indicator = None
    rqst_code = ''
    action_code = ''
    actn_number = 0
    request_text = ''
    all_pax_flag = '?'
    all_itinerary_flag = '?'

    def __init__(rqst_sequence_no,
                 indicator, rqst_code,
                 action_code, actn_number,
                 request_text,
                 all_pax_flag, all_itinerary_flag):
        """New instance of this class."""
        self.rqst_sequence_no   = rqst_sequence_no
        self.indicator = indicator
        self.rqst_code = rqst_code
        self.action_code = action_code
        self.actn_number = actn_number
        self.request_text = request_text
        self.all_pax_flag = all_pax_flag
        self.all_itinerary_flag = all_itinerary_flag

    def display(self):
        """Print class data."""
        print(2, "Request %2d code %s action %s%d : %s"
                    % (self.rqst_seqn_no, self.rqst_code,
                    self.action_code, self.actn_number,
                    self.request_text))

