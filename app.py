
from flask import  Flask ,session, request, jsonify
from datetime import datetime
from database.database import *
from services.jsonClassEncoder import JsonClassEncoder
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = 'this will be used to cryptograph sensible data like authentication tokens'

CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

jsonClassEncoder = JsonClassEncoder()
jsonClassEncoder.ensure_ascii = False

@app.route('/api/getDapartments', methods=(['GET']))
def getDepartments():
    try:
        departments = danh_sach_khoa_phong('danh_muc_khoa_phong')
        return responseSuccess(departments)
    except Exception as e:
        return responseError(e)

@app.route('/api/getUsersByDepartmentId', methods=(['GET']))
def getUsesByDepartmentId():
    try:
        departmentId = request.args.get('departmentId')
        users = danh_sach_nhan_vien_theo_khoa_phong(departmentId)
        return responseSuccess(users)
    except Exception as e:
        return responseError(e)

@app.route('/api/getClientIP', methods=(['GET']))
def getClientIP():
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        ip=request.environ['REMOTE_ADDR'] 
    else:
        ip=request.environ['HTTP_X_FORWARDED_FOR']
    return ip

@app.route('/api/getUser', methods=(['GET']))
def getUser():
    try:
        userId = request.args.get('userId')
        user = doc_thong_tin_nhan_vien(userId)
        return responseSuccess(user)
    except Exception as e:
        return responseError(e)

@app.route('/api/getUsers', methods=(['GET']))
def getUsers():
    try:
        users = danh_sach_nhan_vien()
        return responseSuccess(users)
    except Exception as e:
        return responseError(e)        

@app.route('/api/getOfficialDocumentCnt', methods=(['GET']))
def getOfficialDocumentCnt():
    try:
        departmentId = request.args.get('departmentId')
        documentStatus = request.args.get('documentStatus')
        if departmentId is None:
            officalDocuments = []
        elif documentStatus is None:
            officalDocuments = danh_sach_cong_van_van_ban_khoa_phong_nhan(departmentId)
        else:
            officalDocuments = danh_sach_cong_van_van_ban_khoa_phong_nhan_theo_trang_thai(departmentId, documentStatus)
        return responseSuccess(officalDocuments)
    except Exception as e:
        return responseError(e) 


@app.route('/api/getOfficialDocument', methods=(['GET']))
def getOfficialDocument():
    try:
        departmentId = request.args.get('departmentId')
        documentStatus = request.args.get('documentStatus')
        fullname = request.args.get('fullname')
        officalId = request.args.get('officalId')
        page = int(request.args.get('page', 1))
        pageSize = int(request.args.get('pageSize', 10))
        skipCount = (page - 1) * pageSize
        officalDocuments = danh_sach_cong_van_phan_trang(departmentId, fullname, documentStatus, officalId, pageSize, skipCount)
        return responseSuccess(officalDocuments)
    except Exception as e:
        return responseError(e) 

@app.route('/api/getOfficialDocumentDashBoard', methods=(['GET']))
def getOfficialDocumentDashBoard():
    try:
        departmentId = request.args.get('departmentId')
        limit = int(request.args.get('pageSize', 10))

        if departmentId is None:
            officalDocuments = []
        else:
            officalDocuments = danh_sach_cong_van_van_ban_khoa_phong_nhan_chua_xu_ly(departmentId, limit)
        return responseSuccess(officalDocuments)
    except Exception as e:
        return responseError(e) 


@app.route('/api/getSubmissionCnt', methods=(['GET']))
def getSubmissionCnt():
    try:
        departmentId = request.args.get('departmentId')
        submissionStatus = request.args.get('submissionStatus')
        years = request.args.get('years')
        fullname = request.args.get('fullName')
        officalDocuments = []
        
        if not years:
            years = list_nam_tim_kiem()

        if departmentId is None:
            officalDocuments = []
        elif submissionStatus is not None:
            for year in years:
                ds = danh_sach_phieu_theo_trang_thai(departmentId, fullname, year[2:], submissionStatus)
                officalDocuments.extend(ds)
        else:
            for year in years:
                officalDocuments.extend(danh_sach_phieu_theo_trang_thai(departmentId, fullname, year[2:], None))
            
        return responseSuccess(officalDocuments)
    except Exception as e:
        return responseError(e) 

@app.route('/api/getSubmissionDashBoard', methods=(['GET']))
def getSubmissionDashBoard():
    try:
        departmentId = request.args.get('departmentId')
        fullname = request.args.get('fullName')
        years = request.args.get('years')
        officalDocuments = []
        take = 10
        
        if not years:
            years = list_nam_tim_kiem()

        if departmentId is None:
            officalDocuments = []
        else:
            for year in years:
                ds = danh_sach_phieu_chua_xu_ly(departmentId, fullname, year[2:])
                for i in ds:
                    if len(officalDocuments) < take:
                        officalDocuments.append(i)
                    else:
                        return responseSuccess(officalDocuments)
            
        return responseSuccess(officalDocuments)
    except Exception as e:
        return responseError(e) 

@app.route('/api/login', methods=(['POST']))
def login():
    try:
        data = request.get_json()
        IP = getClientIP()
        userId = data.get('userId')
        departmentId = data.get('departmentId')
        userPassword = data.get('userPassword')
        hashPassword = hash_mk(userPassword)
        username = kiem_tra_dang_nhap_hop_le(userId, hashPassword)

        if session.get('username') is not None:
            user = doc_thong_tin_nhan_vien(userId)
            return responseSuccess(user)

        if username==False:
            fullName=MANHANVIEN_HOTEN(userId)
            logging(userId, departmentId, fullName, IP, 'MẬT KHẨU KHÔNG ĐÚNG')
            return response(False, "Đăng nhập thất bại", userId)
        else:
            fullName=MANHANVIEN_HOTEN(userId)
            logging(userId, departmentId, fullName, IP,'Đăng nhập thành công')
            user = doc_thong_tin_nhan_vien(userId)

            session['IP']=IP
            session['DATE']=datetime.now().strftime('%d/%m/%Y %H:%M:%S')
            session['departmentId']=departmentId
            session['userId']=userId
            session['hashPassword']=hashPassword
            session['dateOfBirth']=user['NGAYSINH']
            session['position']=user['CHUCVU']
            session['fullName']=fullName
            session['username']=username

            return responseSuccess(user)
    except Exception as e:
        return responseError(e)
    
@app.route('/api/getUserActionLogs',methods=['GET'])      
def getUserActionLogs():
    try:
        userId = session.get('userId')

        if userId is None:
            return response(False, "Bạn chưa đăng nhập", None)

        userActionLogs=Find_myquery_sort({'MANHANVIEN':userId},'STT_PHIEUDX','logging')
        return responseSuccess(userActionLogs)
    except Exception as e:
        return responseError(e)
    

@app.route("/api/logout", methods=['POST'])
def logout():
    try:
        logging(session.get('userId'),session.get('departmentId'),session.get('fullName'),session.get('IP'), 'LOGOUT')
        session.clear()
        return responseSuccess(session.get('userId'))
    except Exception as e:
        return responseError(e)
  

@app.route("/api/hello")
def hellologout():
    return "Hello world"
    
def response(success, message, data):
     return jsonify({"success": success, "message": message, "data": data }), 200

def responseSuccess(data):
     return jsonify({"success": True, "message": "success", "data": data }), 200

def responseError(error):
    message = f"An unexpected error occurred: {str(error)}"
    return jsonify({"success": False, "message": message, "data": None }), 500

if __name__ == '__main__':
    app.run(debug=True)
