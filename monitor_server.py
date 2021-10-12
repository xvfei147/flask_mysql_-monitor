from flask import Flask
from flask import request
from flask import render_template
from service import *
import json

app = Flask(__name__)


@app.route('/')
def monitor_page():
    source_list = monitor_source.get_all()['rows']
    return render_template('monitor.html', source_list=source_list)


@app.route('/monitor/get_all')
def monitor_get_all():
    return json.dumps(monitor.get_all())


@app.route('/monitor/save', methods=['POST'])
def monitor_save():
    return monitor.save(request.form)


@app.route('/monitor/delete', methods=['GET'])
def monitor_delete():
    ids = request.args['ids']
    print(ids)
    return monitor.delete(ids)


@app.route('/monitor/execute/<_id>', methods=['GET'])
def monitor_execute(_id):
    return monitor.execute(_id)


# 德鸿报警数据源配置页
@app.route('/monitor/source')
def monitor_source_page():
    return render_template('monitor_source.html')


@app.route('/monitor/source/get_all')
def monitor_get_all_source():
    return json.dumps(monitor_source.get_all())


@app.route('/monitor/source/save', methods=['POST'])
def monitor_save_source():
    return monitor_source.save(request.form)


@app.route('/monitor/source/test_conn', methods=['POST'])
def monitor_test_conn():
    return monitor_source.test_conn(request.form)


@app.route('/monitor/source/delete/<_id>', methods=['GET'])
def monitor_delete_source(_id):
    return monitor_source.delete(_id)


if __name__ == '__main__':
    monitor.restart()
    app.run(port=5001, debug=False, host='0.0.0.0', threaded=True)
