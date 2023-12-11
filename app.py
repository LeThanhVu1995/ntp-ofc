
from flask import  Flask ,session, request, jsonify
from datetime import datetime
from database.database import *
from flask_cors import CORS
import jwt

app = Flask(__name__)
app.secret_key = 'CLINNAT_API_REST'
CORS(app, resources={r"/api/*": {"origins": "*"}})

BLACKLISTED_TOKENS = set()
JWT_MINUTES = 60

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
            count = 0
        elif documentStatus is None:
            count = dem_danh_sach_cong_van_van_ban_khoa_phong_nhan(departmentId)
        else:
            count = dem_danh_sach_cong_van_van_ban_khoa_phong_nhan_theo_trang_thai(departmentId, documentStatus)
        return responseSuccess(count)
    except Exception as e:
        return responseError(e) 

@app.route('/api/getTimelineOfficalDocument', methods=(['GET']))
def getTimelineOfficalDocument():
    try:
        STT_PHIEUDX = request.args.get('documentId')
        data=Find_myquery({'STT_PHIEUDX':STT_PHIEUDX},STT_PHIEUDX[:2])
        return responseSuccess(data)
    except Exception as e:
        return responseError(e) 

@app.route('/api/getOfficialDocument', methods=(['GET']))
def getOfficialDocument():
    try:
        departmentId = request.args.get('departmentId')
        documentStatus = request.args.get('documentStatus', None)
        fullname = request.args.get('fullname')
        officalId = request.args.get('officalId')
        startDate = request.args.get('startDate')
        endDate = request.args.get('endDate')
        page = int(request.args.get('page', 1))
        abstract = request.args.get('abstract', None)
        pageSize = int(request.args.get('pageSize', 10))
        skipCount = (page - 1) * pageSize

        if documentStatus == '':
            documentStatus = None

        if documentStatus is not None:
            documentStatus = documentStatus.split(',')

        officalDocuments = danh_sach_cong_van_phan_trang(departmentId, fullname, documentStatus,  officalId, startDate, endDate, abstract, pageSize, skipCount)
        return responseSuccess(officalDocuments)
    except Exception as e:
        return responseError(e) 
    

@app.route('/api/getOfficialDocumentTotal', methods=(['GET']))
def getOfficialDocumentTotal():
    try:
        departmentId = request.args.get('departmentId')
        documentStatus = request.args.get('documentStatus', None)
        fullname = request.args.get('fullname')
        officalId = request.args.get('officalId')
        startDate = request.args.get('startDate')
        endDate = request.args.get('endDate')
        abstract = request.args.get('abstract', None)

        if documentStatus == '':
            documentStatus = None

        if documentStatus is not None:
            documentStatus = documentStatus.split(',')

        count = dem_tong_danh_sach_cong_van_phan_trang(departmentId, fullname, documentStatus, officalId, startDate, endDate, abstract)

        return responseSuccess(count)
    except Exception as e:
        return responseError(e) 

@app.route('/api/getOfficialDocumentDashBoard', methods=(['GET']))
def getOfficialDocumentDashBoard():
    try:
        departmentId = request.args.get('departmentId')
        limit = int(request.args.get('pageSize', 4))

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
        count = 0
        
        if not years:
            years = list_nam_tim_kiem()

        if departmentId is None:
            count= 0
        elif submissionStatus is not None:
            for year in years:
                total = dem_danh_sach_phieu_theo_trang_thai(departmentId, fullname, year[2:], submissionStatus)
                count = count + total
        else:
            for year in years:
                total = dem_danh_sach_phieu_theo_trang_thai(departmentId, fullname, year[2:], None)
                count = count + total
            
        return responseSuccess(count)
    except Exception as e:
        return responseError(e) 

@app.route('/api/getSubmissionDashBoard', methods=(['GET']))
def getSubmissionDashBoard():
    try:
        departmentId = request.args.get('departmentId')
        fullname = request.args.get('fullName')
        years = request.args.get('years')
        officalDocuments = []
        take = 4
        
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

        if username==False:
            fullName=MANHANVIEN_HOTEN(userId)
            logging(userId, departmentId, fullName, IP, 'Mật khẩu không đúng')
            return response(False, "Đăng nhập thất bại", userId)
        else:
            fullName=MANHANVIEN_HOTEN(userId)
            logging(userId, departmentId, fullName, IP,'Đăng nhập thành công')
            user = doc_thong_tin_nhan_vien(userId)

            userToken = {}
            userToken['IP']=IP
            userToken['DATE']=datetime.now().strftime('%d/%m/%Y %H:%M:%S')
            userToken['departmentId']=departmentId
            userToken['userId']=userId
            userToken['hashPassword']=hashPassword
            userToken['dateOfBirth']=user['NGAYSINH']
            userToken['position']=user['CHUCVU']
            userToken['fullName']=fullName
            userToken['username']=username
            token = jwt.encode({'user': userToken, 'exp': datetime.now() + timedelta(minutes=JWT_MINUTES)}, app.config['SECRET_KEY'], algorithm='HS256')

            return responseSuccess({"token": token, "user": userToken})
        
    except Exception as e:
        return responseError(e)
    

def getToken():
    token = request.headers.get('Authorization')
    if not token or not token.startswith('Bearer '):
        return None

    token = token.split()[1]

    if token in BLACKLISTED_TOKENS:
        return None

    try:
        token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return token
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
    
@app.route('/api/getUserActionLogs',methods=['GET'])      
def getUserActionLogs():
    try:
        # token = getToken()
        # if token is None:
        #     return response(False, "Bạn chưa đăng nhập", None)
        
        # user = token['user']
        # userId = user['userId']
        userId = request.args.get('userId')
        userActionLogs=Find_myquery_sort({'MANHANVIEN':userId},'STT_PHIEUDX','logging')
        return responseSuccess(userActionLogs)
    except Exception as e:
        return responseError(e)
    

@app.route("/api/logout", methods=['POST'])
def logout():
    try:
        token = request.headers.get('Authorization')
        if not token or not token.startswith('Bearer '):
           return response(False, "Bạn chưa đăng nhập", None)

        token = token.split()[1]

        BLACKLISTED_TOKENS.add(token)
        return responseSuccess(token)
       
    except Exception as e:
        return responseError(e)
  

def response(success, message, data):
     return jsonify({"success": success, "message": message, "data": data }), 200

def responseSuccess(data):
     return jsonify({"success": True, "message": "success", "data": data }), 200

def responseError(error):
    message = f"An unexpected error occurred: {str(error)}"
    return jsonify({"success": False, "message": message, "data": None }), 500

if __name__ == '__main__':
    app.run(debug=True)
