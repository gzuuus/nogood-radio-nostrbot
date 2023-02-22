import ssl,time, schedule
from nostr.event import Event
from nostr.relay_manager import RelayManager
from nostr.key import PrivateKey

nsec_key= 'Your-nsec-priv-key'
relay_list=['wss://nostr.mutinywallet.com', 'wss://nproxy.cc']#add relays separated by commas
msg_to_nostr='PV! Have a productive day ☀️\n\nTune in to NoGood Radio | 24/7 LoFi for builders in #bitcoin and #NOSTR ⚡️\n\n https://www.youtube.com/live/h69snvlGLXU'

def send_nostr_event(relay_list, message, privk):
  relay_manager = RelayManager()
  for i in relay_list:
      relay_manager.add_relay(i)
  relay_manager.open_connections({"cert_reqs": ssl.CERT_NONE}) # NOTE: This disables ssl certificate verification
  time.sleep(1.25) # allow the connections to open
  private_key = PrivateKey.from_nsec(nsec_key)
  event = Event(private_key.public_key.hex(), message)
  private_key.sign_event(event)
  print(event.to_message(), len(event.to_message()))
  relay_manager.publish_event(event)
  time.sleep(1) # allow the messages to send
  while relay_manager.message_pool.has_notices():
    notice_msg = relay_manager.message_pool.get_notice()
    print(notice_msg.content)
  relay_manager.close_connections()
  print('sended!')

if __name__=='__main__':
    schedule.every().day.at('15:00').do(send_nostr_event, relay_list=relay_list, message=msg_to_nostr, privk=nsec_key)
    #send_nostr_event(relay_list, 'your-message', nsec_key)
    while True:
        schedule.run_pending()
        time.sleep(1)
