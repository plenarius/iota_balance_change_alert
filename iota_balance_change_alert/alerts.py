# coding=utf-8

def check_alert_modules(config):
  if config.getboolean('twilio','active'):
    try:
        from twilio.rest import Client
    except ImportError as e:
      print("You have enabled twilio alerts but do not have the module installed.")
      print(e)


def email_alert(config, report_body):
  from smtplib import SMTP
  email_msg = config.get('email', 'subject') + "\n\n" + report_body

  smtp_server = SMTP(config.get('email', 'server'), config.get('email', 'port'))
  smtp_server.ehlo()
  smtp_server.starttls()
  smtp_server.login(config.get('email', 'user'), config.get('email', 'password'))
  smtp_server.sendmail(config.get('email', 'user'), config.get('email', 'to'), email_msg)
  smtp_server.quit()

def twilio_alert(config, txtmsg_body):
  from twilio.rest import Client
  client = Client(config.get('twilio', 'sid'), config.get('twilio', 'token'))
  client.messages.create(to=config.get('twilio', 'to'), 
                        from_=config.get('twilio', 'from'), 
                        body=txtmsg_body)
    
def beep_alert():
  import pyaudio
  import numpy as np

  p = pyaudio.PyAudio()

  volume = 0.5     # range [0.0, 1.0]
  fs = 44100       # sampling rate, Hz, must be integer
  duration = 5.0   # in seconds, may be float
  f = 440.0        # sine frequency, Hz, may be float

  # generate samples, note conversion to float32 array
  samples = (np.sin(2*np.pi*np.arange(fs*duration)*f/fs)).astype(np.float32)

  # for paFloat32 sample values must be in range [-1.0, 1.0]
  stream = p.open(format=pyaudio.paFloat32,
                  channels=1,
                  rate=fs,
                  output=True)

  # play. May repeat with different volume values (if done interactively) 
  stream.write(volume*samples)

  stream.stop_stream()
  stream.close()

  p.terminate()
  
def msgbox_alert(report_body):
  import Tkinter, tkMessageBox
  root = Tkinter.Tk()
  root.withdraw()
  tkMessageBox.showwarning(
      "Balance Change Detected",
      "%s" % (report_body)
  )