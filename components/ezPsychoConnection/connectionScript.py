# ezTrigger system initialization code start.

import asyncore
import socket
import threading


class ezSocketClient(asyncore.dispatcher):
  def __init__(self, host, port, ppyClinet):
    asyncore.dispatcher.__init__(self)
    self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
    self.connect((host, port))
    self.ppyClient = ppyClinet
    self.host = host
    self.port = port
    self.SendData = ""
    self.RecvData = ""

  def handle_connect(self):
    print('[CONN] Connected to the server.')

  def handle_close(self):
    print('[CONN] Disconnected.')
    self.close()

  def handle_read(self):
    self.RecvData = self.recv(8192)
    if len(self.RecvData) > 0:
      self.ppyClient.handle_server_response(self.RecvData, self)

  def handle_write(self):
    self.send(self.SendData)
    print("[SEND] " + self.SendData)

  def send(self, data):
    self.SendData = "%s\r\n" % (data)
    self.handle_write()

  def writable(self):
    return False


class ezTriggerPPyClient(threading.Thread):
  def __init__(self, serverIp, serverPort, clientType='PPY', clientId=''):
    self.client = ezSocketClient(serverIp, serverPort, self)
    self.serverIp = serverIp
    self.serverPort = serverPort
    self.clientType = clientType
    self.clientId = clientId

    threading.Thread.__init__(self)

  def run(self):
    try:
      asyncore.loop()
    except:
      pass

  def handle_server_response(self, data, connection):
    global continueRoutine

    commandString = data.split()
    command = commandString[0]
    parameter = commandString[1:]

    if command == 'SETVAR':
      print('[SVAR] Remote command, set variable `%s` to %s' %
          (parameter[0], parameter[1]))
      globals()[parameter[0]] = str(parameter[1])
    elif command == 'ENDLOOP':
      if parameter[0] in globals():
        globals()[parameter[0]].finished = True
      else:
        connection.send = "!ELOOPNOTEXISTS"
    elif command == 'ENDROUTINE':
      continueRoutine = False
    elif command == 'WHO':
      connection.send = "TP %s" % (self.clientType)
    elif command == 'REGISTERED':
      if self.clientId and self.clientId != '':
        connection.send = "ID %s" % (self.clientId)

    print("[RECV] " + data)

# ezTrigger system initialization code end.
