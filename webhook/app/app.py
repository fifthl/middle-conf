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

    for alert in data['alerts'][:]:

        utc = alert['startsAt']
        UTC_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
        utc_time = datetime.datetime.strptime(utc, UTC_FORMAT)
        local_timems = utc_time + datetime.timedelta(hours=8)
        local_time = local_timems.replace(microsecond=0)

        alert_content = alert['annotations']['summary'].split(':', 1)
        pattern = re.compile(r"\d{3,5} (.*)")
        alert_info = pattern.findall(alert_content[1])
        details_list = ''.join(alert_info)
        message = alert_content[0] + ' ' + details_list

        send_data = {
            "msgtype": "markdown",
            "markdown": {
                "title": "prometheus 告警",
                "text": "## 主机告警 \n" +
                        "**[告警名称]**:   %s \n\n" % alert['labels']['alertname'] +
                        "**[告警实例]**:   %s \n\n" % alert['labels']['instance'].split(':')[0] +
                        "**[告警级别]**:   %s \n\n" % alert['labels']['severity'] +
                        "**[告警时间]**:   %s \n\n" % local_time +
                        "**[告警详情]**:   %s \n\n" % message


            }
        }
        req = requests.post(url, json=send_data)
        result = req.json()
        if result['errcode'] != 0:
            print('notify dingtalk error: %s' % result['errcode'])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8060)