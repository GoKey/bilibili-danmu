#coding:utf8
import websocket
import threading
import time
import json
import struct

def on_message(ws, message):
    a=message
    unpack(ws,a)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")


def run():
    ws = websocket.WebSocketApp("ws://broadcastlv.chat.bilibili.com:2244/sub",on_message=on_message,on_error=on_error,on_close=on_close)
    ws.on_open = on_open
    print(u"开始监听弹幕")
    ws.run_forever()
def on_open(ws):
    def run(*args):
        data = "\x00\x00\x00\x35\x00\x10\x00\x01\x00\x00\x00\x07\x00\x00\x00\x01{\"uid\":0,\"roomid\":23058,\"protover\":1}"
        ws.send(data, opcode=websocket.ABNF.OPCODE_BINARY)

    def heart():
        while 1:
            try:
                ws.send("\x00\x00\x00\x1f\x00\x10\x00\x01\x00\x00\x00\x02\x00\x00\x00\x01[Object object]",
                        opcode=websocket.ABNF.OPCODE_BINARY)
            except:
                break
            time.sleep(20)

    __threads__ = []
    run()
    __threads__.append(threading.Thread(target=heart))
    for t in __threads__:
        t.setDaemon(True)
        t.start()





def unpack(ws, data):
    ret = []
    len_data = len(data)
    if (not data) or len_data == 0:
        ws.close()
        return ret
    if len_data == 16 or len_data == 20:
        return ret
    start = 0
    end = 4
    while len(data[end:]) > 0:
        # for i in range(4):
        # print "%02X" % ord(data[start:end][i]),
        end = start + struct.unpack("!I", data[start:end])[0]
        try:
            ret.append(json.loads(data[(start + 16):end]))
        except Exception:
            pass
        start = end
        end = start + 4
        print(ret)
        print("************************************************************")
    return ret
run()
