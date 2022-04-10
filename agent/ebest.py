import configparser
from dataclasses import Field
from statistics import mode
import win32com.client
import pythoncom
import time
from datetime import datetime


class XASession:

    login_state = 0
    QUERY_LIMIT_10MIN = 200
    LIMIT_SECONDS = 600

    def OnLogin(self, code, msg):
        """
        0000 is success to connect 
        """
        if code == "0000":
            print(code, msg)
            XASession.login_state = 0
        else:
            print(code, msg)

    def OnDisconnect(self):
        print("Session Disconnected")
        XASession.login_state = 0
        

class EBest:

    def __init__(self, mode=None):
        
        self.query_cnt = []
        """
        모의서버 DEMO
        실서버   PROD
        """
        if mode not in ["DEMO", "PROD"]:
            raise Exception("Need to run_mode(PROD or DEMO)")

        run_mode = "EBEST_" + mode
        config = configparser.ConfigParser()
        config.read("conf\\config.ini")
        self.user = config[run_mode]['user']
        self.password = config[run_mode]['password']
        self.cert_passwd = config[run_mode]['cert_passwd']
        self.host = config[run_mode]['host']
        self.port = config[run_mode]['port']
        self.account = config[run_mode]['account']

        self.xa_session_client = win32com.client.DispatchWithEvents("XA_Session.XASession", XASession)

    
    def _execute_query(self, res, in_block_name, out_block_name, *out_fields, **set_fields):
        """
        :param res:str 리소스 이름(TR)
        :param in_block_name:str    in block name
        :param out_block_name:str   out block name
        :param out_params:list      output fields list
        :param in_params:dict       fields dict for set in 'in block'
        :return result:list         result return in list
        """

        time.sleep(1)
        print("current query cnt:", len(self.query_cnt))
        print(res, in_block_name, out_block_name)
        while len(self.query_cnt) >= EBest.QUERY_LIMIT_10MIN:
            time.sleep(1)
            print("waiting for execute query... current query cnt:", len(self.query_cnt))
            self.query_cnt = list(filter(lambda x: (datetime.today() - x).total_seconds() < \
                EBest.LIMIT_SECONDS, self.query_cnt))
        
        xa_query = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", XAQuery)
        xa_query.LoadFromResFile(XAQuery.RES_PATH + res+".res")

        #in_block name setting
        for key, value in set_fields.items():
            xa_query.SetFieldData(in_block_name, key, 0, value)
            errorCode = xa_query.Request(0)

        # wait after request
        waiting_cnt = 0
        while xa_query.tr_run_state == 0:
            waiting_cnt += 1
            if waiting_cnt % 100000 == 0:
                print("Waiting.....", self.xa_session_client.GetLastError())
            pythoncom.PumWaitingMessage()

        # result block
        result = []
        count = xa_query.GetBlockCount(out_block_name)

        for i in range(count):
            item = {}
            for field in out_fields:
                value = xa_query.GetFieldData(out_block_name, field, i)
                item[field] = value
            result.append(item)

        # check time limit
        XAQuery.tr_run_state = 0
        self.query_cnt.append(datetime.today())

        # Substitute Eng to Kor
        for item in result:
            for field in list(item.keys()):
                if getattr(Field, res, None):
                    res_field = getattr(Field, res, None)
                    if out_block_name in res_field:
                        field_hname = res_field[out_block_name]
                        if field in field_hname:
                            item[field_hname[field]] = item[field]
                            item.pop(field)
        return result

    def login(self):
        self.xa_session_client.ConnectServer(self.host, self.port)
        self.xa_session_client.Login(self.user, self.passwd, self.cert_passwd, 0, 0)
        while XASession.login_state == 0:
            pythoncom.PumpWaitingMessages()


    def logout(self):
        result = self.xa_session_client.Logout()
        if result:
            XASession.login_state = 0
            self.xa_session_client.DisconnectServer()

    
class XAQuery:
    RES_PATH = "C:\\eBEST\\xingAPI\\Res\\"
    tr_run_state = 0

    def OnReceiveData(self, code):
        print("OnReceiveData", code)
        XAQuery.tr_run_state = 1

    def OnReceiveMessage(self, error, code, message):
        print("OnreceiveMessage", error, code, message)





