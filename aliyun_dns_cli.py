#!/usr/bin/env python
#coding=utf-8

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkalidns.request.v20150109.UpdateDomainRecordRequest import UpdateDomainRecordRequest
from aliyunsdkalidns.request.v20150109.DescribeDomainRecordsRequest import  DescribeDomainRecordsRequest
from aliyunsdkalidns.request.v20150109.AddDomainRecordRequest import  AddDomainRecordRequest
import json
import os


class DnsClient:
    def __init__(self, domain_name='movekj.com'):
        self.domain_name = domain_name
        access_key_id = os.environ['AliAccessKeyId']
        access_secret = os.environ['AliAccessSecret']
        self.client = AcsClient(access_key_id, access_secret, 'cn-hangzhou')
        
    def decribe_domain_records(self):
        describe_domain_records_req = DescribeDomainRecordsRequest()
        describe_domain_records_req.set_DomainName(self.domain_name)
        describe_domain_records_req.set_accept_format('json')
        describe_domain_records_resp = self.client.do_action_with_exception(describe_domain_records_req)
        domain_records = json.loads(describe_domain_records_resp).get('DomainRecords', None)
        return domain_records

    def get_record(self, record_type, RR):
        domain_records = self.decribe_domain_records()
        if domain_records:
            records = domain_records.get('Record', None)
            for record in records:
                if record['RR' ] == RR and record['Type'] == record_type:
                    return record
            return None
        return None
    
    def update_record(self, record_id, record_type, RR, value):
        update_domain_record_req = UpdateDomainRecordRequest()
        update_domain_record_req.set_RR(RR)
        update_domain_record_req.set_Type(record_type)
        update_domain_record_req.set_RecordId(record_id)
        update_domain_record_req.set_Value(value)
        update_domain_record_resp = self.client.do_action_with_exception(update_domain_record_req)
        return json.loads(update_domain_record_resp)
    
    def add_record(self, record_type, RR, value):
        add_domain_record_req = AddDomainRecordRequest()
        add_domain_record_req.set_DomainName(self.domain_name)
        add_domain_record_req.set_RR(RR)
        add_domain_record_req.set_Value(value)
        add_domain_record_req.set_Type(record_type)
        add_domain_record_resp = self.client.do_action_with_exception(add_domain_record_req)
        return json.loads(add_domain_record_resp)


if __name__ == "__main__":
    dns_client = DnsClient()
    RR = 'huawei_router' 
    record = dns_client.get_record('A', RR)

    if record:
        dns_client.update_record(record['RecordId'], record['Type'], record['RR'], '1.2.3.6')
    else:
        dns_client.add_record('A', 'huawei_router', '1.2.3.5')

