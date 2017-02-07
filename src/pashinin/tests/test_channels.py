from channels import Channel
from channels.tests import ChannelTestCase

from pashinin.consumers import send_lead


class MyTests(ChannelTestCase):
    def test_a_thing(self):
        # This goes onto an in-memory channel, not the real backend.
        Channel("send-me-lead").send({
            "name": "1",
            "phone": "2",
            "message": "3",
        })
        # Run the consumer with the new Message object
        send_lead(self.get_next_message("send-me-lead", require=True))
        # Verify there's a result and that it's accurate
        self.get_next_message("result")
        # result =
        # self.assertEqual(result['value'], 1089)
        # assert result['value'] == 1089
