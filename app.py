from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json, re
app = Flask(__name__)

app.config.from_object("config.DevConfig")
app.config.from_object("config.Defaults")
db = SQLAlchemy(app)

CORS(app)

import models

@app.route("/")
def hello():
    return "Back end is up and running."

@app.route("/getAllTests")
def getAllTests():
    try:
        tests = db.session.query(models.Tests).all()
        return jsonify([result.serialize() for result in tests])

    except Exception as e:
	    return(str(e), 500)

@app.route("/getPassed")
def getPassed():
    try:
        passed = db.session.query(models.Tests).filter_by(test_result = "Pass").all()
        return jsonify([p.serialize() for p in passed])

    except Exception as e:
	    return(str(e), 500)

@app.route("/getFailed")
def getFailed():
    try:
        failed = db.session.query(models.Tests).filter_by(test_result = "Fail").all()
        return jsonify([f.serialize() for f in failed])

    except Exception as e:
	    return(str(e), 500)

@app.route("/getLimited")
def getLimited():
    try:
        limited = db.session.query(models.Tests) \
            .filter(models.Tests.limits_used.isnot(None)) \
            .filter(models.Tests.limits_used != "") \
            .all()
        ls = []
        for l in limited:
            if len(l.limits_used.split()) == 3:
                adding = {"id": l.id,
                    "sn": l.sn,
                    "s_no": l.s_no,
                    "test_name": l.test_name,
                    "test_field": l.tets_field,
                    "test_value": l.test_value,
                    "test_result": l.test_result,
                    "spec_name": l.spec_name,
                    "limits_used": l.limits_used,
                    "start_time": l.start_time,
                    "stop_time": l.stop_time,
                    "comments": l.comments}

                if l.limits_used.split()[1] == ">=" or l.limits_used.split()[1] == ">":
                    adding["limits_min"] = l.limits_used.split()[2]
                    adding["warning"] = assessWarning(val = float(l.test_value), minVal = float(l.limits_used.split()[2]))
                else:
                    adding["limits_max"] = l.limits_used.split()[2]
                    adding["warning"] = assessWarning(val = float(l.test_value), maxVal = float(l.limits_used.split()[2]))
                ls.append(adding)

            elif len(l.limits_used.split()) == 5:
                adding = {"id": l.id,
                    "sn": l.sn,
                    "s_no": l.s_no,
                    "test_name": l.test_name,
                    "test_field": l.tets_field,
                    "test_value": l.test_value,
                    "test_result": l.test_result,
                    "spec_name": l.spec_name,
                    "limits_used": l.limits_used,
                    "limits_min": l.limits_used.split()[0],
                    "limits_max": l.limits_used.split()[4],
                    "start_time": l.start_time,
                    "stop_time": l.stop_time,
                    "comments": l.comments,
                    "warning": assessWarning(val = float(l.test_value), minVal = float(l.limits_used.split()[0]), maxVal = float(l.limits_used.split()[4]))}
                ls.append(adding)
        return jsonify(ls)

    except Exception as e:
	    return(str(e), 500)

@app.route("/getSerialNos")
def getSerialNos():
    try: 
        serials = db.session.query(models.Tests.sn).group_by(models.Tests.sn).all()
        return jsonify([s.sn for s in serials])

    except Exception as e:
	    return(str(e), 500)

@app.route("/getTestNames")
def getTestNames():
    try: 
        names = db.session.query(models.Tests.test_name).group_by(models.Tests.test_name).all()
        return jsonify([name.test_name for name in names])

    except Exception as e:
	    return(str(e), 500)

@app.route("/getTestFields")
def getTestFields():
    try: 
        fields = db.session.query(models.Tests.tets_field).group_by(models.Tests.tets_field).all()
        return jsonify([field.tets_field for field in fields])

    except Exception as e:
	    return(str(e), 500)

@app.route("/getLimits", methods = ["POST"])
def getLimits():
    dic = json.loads(request.get_data())
    serialNo = dic['sn']
    tName = dic['test_name']
    tField = dic['test_field']

    try:
        result = db.session.query(models.Tests) \
                        .filter(models.Tests.limits_used.isnot(None)) \
                        .filter(models.Tests.limits_used != "") \
                        .filter_by(sn = serialNo, test_name = tName, tets_field = tField) \
                        .first()

        if len(result.limits_used.split()) == 3:
            return jsonify({"id": result.id,
                            "sn": result.sn,
                            "s_no": result.s_no,
                            "test_name": result.test_name,
                            "test_field": result.tets_field,
                            "test_value": result.test_value,
                            "test_result": result.test_result,
                            "spec_name": result.spec_name,
                            "limits_used": result.limits_used,
                            "limits_min": result.limits_used.split()[2] \
                                            if result.limits_used.split()[1] == ">=" or \
                                                result.limits_used.split()[1] == ">" \
                                            else result.limits_used.split()[0],
                            "limits_max": result.limits_used.split()[2] \
                                            if result.limits_used.split()[1] == "<=" or \
                                                result.limits_used.split()[1] == "<" \
                                            else result.limits_used.split()[0],
                            "start_time": result.start_time,
                            "stop_time": result.stop_time,
                            "comments": result.comments})
        
        if len(result.limits_used.split()) == 5:
            return jsonify({"id": result.id,
                            "sn": result.sn,
                            "s_no": result.s_no,
                            "test_name": result.test_name,
                            "test_field": result.tets_field,
                            "test_value": result.test_value,
                            "test_result": result.test_result,
                            "spec_name": result.spec_name,
                            "limits_used": result.limits_used,
                            "limits_min": result.limits_used.split()[0],
                            "limits_max": result.limits_used.split()[4],
                            "start_time": result.start_time,
                            "stop_time": result.stop_time,
                            "comments": result.comments})

    except Exception as e:
	    return(str(e), 500)

@app.route("/getBySerial", methods = ['POST'])
def getBySerial():
    dic = json.loads(request.get_data())
    serialNo = dic['sn']
    try:
        results = db.session.query(models.Tests).filter_by(sn = serialNo).all()
        return jsonify([result.serialize() for result in results])

    except Exception as e:
	    return(str(e), 500)

@app.route("/getByField", methods = ['POST'])
def getByField():
    dic = json.loads(request.get_data())
    field = dic['test_field']
    try:
        results = db.session.query(models.Tests).filter_by(tets_field = field).all()
        return jsonify([result.serialize() for result in results])

    except Exception as e:
	    return(str(e), 500)

@app.route("/addXlsx", methods = ['POST'])
def addXlsx():
    dic = json.loads(request.get_data())
    node_array = dic['node_array']

    try:
        count = 0

        for i in node_array:
            count += 1

            if "Limits Used" not in i:
                i["Limits Used"] = ""

            if "Comments" not in i:
                i["Comments"] = ""

            if "Test Name" not in i:
                i["Test Name"] = "Not Recorded"

            if "Test Field" not in i:
                i["Test Field"] = ""

            if "Test Value" not in i:
                i["Test Value"] = ""

            if "Test Result" not in i:
                i["Test Result"] = ""

            if "Spec Name" not in i:
                i["Spec Name"] = ""
                
            if "Start Time" not in i:
                i["Start Time"] = ""

            if "Stop Time" not in i:
                i["Stop Time"] = ""
            
            new = models.Tests(
                sn = i["SN"],
                s_no = i["S_NO"],
                test_name = i["Test Name"],
                tets_field = i["Test Field"],
                test_value = i["Test Value"],
                test_result = i["Test Result"],
                spec_name = i["Spec Name"],
                limits_used = i["Limits Used"],
                start_time = i["Start Time"],
                stop_time = i["Stop Time"],
                comments = i["Comments"])

            db.session.add(new)

        db.session.commit()
        return json.dumps({"Success Count": count})

    except Exception as e:
	    return(str(e), 500)

@app.route("/addTestResults", methods = ['POST'])
def addTestResults():
    dic = json.loads(request.get_data())
    sn = dic['sn']
    s_no = dic['s_no']
    test_name = dic['test_name']
    test_field = dic['test_field']
    test_value = dic['test_value']
    test_result = dic['test_result']
    spec_name = dic['spec_name']
    limits_used = dic['limits_used']
    start_time = dic['start_time']
    stop_time = dic['stop_time']
    comments = dic['comments']

    try:
        new = models.NodeTestResult(
            sn = sn,
            s_no = s_no,
            test_name = test_name,
            tets_field = test_field,
            test_value = test_value,
            test_result = test_result,
            spec_name = spec_name,
            limits_used = limits_used,
            start_time = start_time,
            stop_time = stop_time,
            comments = comments)
        
        db.session.add(new)
        db.session.commit()
        return json.dumps({"SN":str(ntr.sn), "S_NO": str(ntr.s_no)})

    except Exception as e:
	    return(str(e), 500)

@app.route("/latestFromSerial", methods=["POST"])
def latestFromSerial():
    dic = json.loads(request.get_data())
    sn = dic['sn']

    try: 
        rs = db.session.query(models.Tests.limits_used,
                                models.Tests.test_name,
                                models.Tests.tets_field,
                                models.Tests.stop_time,
                                models.Tests.test_value) \
                        .filter(models.Tests.limits_used.isnot(None)) \
                        .filter(models.Tests.limits_used != "") \
                        .filter_by(sn = sn) \
                        .order_by(models.Tests.test_name) \
                        .all()
        res = []
        test = ""
        field = ""
        time = []
        test_to_add = {}

        for i in rs:

            if test == "" and field == "" and (len(i.limits_used.split()) == 5 or len(i.limits_used.split()) == 3):
                test = i.test_name
                field = i.tets_field
                time = re.split(r"[ :/-]+", i.stop_time)
                test_to_add = i

            elif (i.test_name != test or i.tets_field != field) and test_to_add != {}:
                res.append(test_to_add)

                if len(i.limits_used.split()) == 5 or len(i.limits_used.split()) == 3:
                    test = i.test_name
                    field = i.tets_field
                    time = re.split(r"[ :/-]+", i.stop_time)
                    test_to_add = i

                else:
                    test = ""
                    field = ""
                    time = []
                    test_to_add = {}

            elif i.test_name == test \
                    and i.tets_field == field \
                    and (len(i.limits_used.split()) == 5 or len(i.limits_used.split()) == 3) \
                    and olderThan(time, re.split(r"[ :/-]+", i.stop_time)):
                time = re.split(r"[ :/-]+", i.stop_time)
                test = i.test_name
                field = i.tets_field
                test_to_add = i

        if test_to_add != {}:
            res.append(test_to_add)

        return jsonify([{"test_name": result.test_name,
                        "test_field": result.tets_field,
                        "limits_used": result.limits_used,
                        "test_value": result.test_value,
                        "stop_time": result.stop_time} for result in res]) #[:2]

    except Exception as e:
	    return(str(e), 500)

def assessWarning(val = False, minVal = False, maxVal = False):
    if not (val and (minVal or maxVal)):
        print("Values not provided")
        return

    if minVal and maxVal:
        rng = maxVal - minVal
        tolerance = rng * 0.025
        return (val <= minVal + tolerance) or (val >= maxVal - tolerance)

    if maxVal:
        tolerance = maxVal * 0.05
        return val >= maxVal - tolerance
    
    tolerance = minVal * 0.05
    return val <= minVal + tolerance

def olderThan(old, new):
    if old == new:
        return True

    elif old[2] < new[2]: # Year comparison
        return True

    elif old[0] < new[0]: # Month comparison
        return True

    elif old[1] < new[1]: # Day comparison
        return True

    elif old[3] < new[3]: # Hour comparison
        return True

    elif old[4] < new[4]: # Minute comparison
        return True
    
    return False

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='4000')