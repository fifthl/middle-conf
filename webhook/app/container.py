import json
import requests
import datetime
import re
from flask import Flask
from flask import request
app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def send():
    if request.method == 'POST':
        post_data = request.get_data()
        send_alert(bytes2json(post_data))
        return 'success'
    else:
        return 'weclome to use prometheus alertmanager dingtalk webhook server!'


def bytes2json(data_bytes):
    data = data_bytes.decode('utf8').replace("'", '"')
    return json.loads(data)


def send_alert(data):
    url = 'https://oapi.dingtalk.com/robot/send?access_token=796ce7902d67eadae99c1a073786d92a052581f17c456f0b40d030d714c4b2cc'

    for alerts in data['alerts'][:]:
        print("告警转换前: ",alerts)

        alert_label = alerts['labels']
        alerts_group = alert_label['alertgroup']
        alerts_name = alert_label['alertname']
        alert_severity = alert_label['severity']
        alert_cluster = alerts['annotations']['cluster']
        alert_summary = alerts['annotations']['summary']
        start_time = alerts['startsAt'].split('T')
        alert_hour = start_time[1].split('.')[0]
        alert_year = start_time[0]
        alert_data = alert_year + ' ' + alert_hour

        send_data = {
            "msgtype": "markdown",
            "markdown": {
                "title": "prometheus 告警",
                "text": "## 发生 %s 级 %s \n" % (alert_severity, alerts_group) +
                        "**事件名称**:   %s \n\n" % alerts_name +
                        "**事件集群**:   %s \n\n" % alert_cluster +
                        "**事件摘要**:   %s \n\n" % alert_summary +
                        "**告警时间**:   %s \n\n" % alert_data

            }
        }
        print("转换成功：", send_data)
        req = requests.post(url, json=send_data)
        result = req.json()
        if result['errcode'] != 0:
            print('notify dingtalk error: %s' % result['errcode'])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8061)